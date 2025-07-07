import logging
import uuid
import jwt
import base64
import hmac
import hashlib
import requests
import os


from datetime import datetime, timedelta
import pytz
from pytz import UTC
from typing import Optional, Union, List, Dict

from opentelemetry import trace

from open_webui.models.users import Users

from open_webui.constants import ERROR_MESSAGES
from open_webui.env import (
    WEBUI_SECRET_KEY,
    TRUSTED_SIGNATURE_KEY,
    STATIC_DIR,
    SRC_LOG_LEVELS,
    WEBUI_AUTH_TRUSTED_EMAIL_HEADER,
)

from fastapi import BackgroundTasks, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext


logging.getLogger("passlib").setLevel(logging.ERROR)

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["OAUTH"])

SESSION_SECRET = WEBUI_SECRET_KEY
ALGORITHM = "HS256"

##############
# Auth Utils
##############


def verify_signature(payload: str, signature: str) -> bool:
    """
    Verifies the HMAC signature of the received payload.
    """
    try:
        expected_signature = base64.b64encode(
            hmac.new(TRUSTED_SIGNATURE_KEY, payload.encode(), hashlib.sha256).digest()
        ).decode()

        # Compare securely to prevent timing attacks
        return hmac.compare_digest(expected_signature, signature)

    except Exception:
        return False


def override_static(path: str, content: str):
    # Ensure path is safe
    if "/" in path or ".." in path:
        log.error(f"Invalid path: {path}")
        return

    file_path = os.path.join(STATIC_DIR, path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(base64.b64decode(content))  # Convert Base64 back to raw binary


def get_license_data(app, key):
    if key:
        try:
            res = requests.post(
                "https://api.openwebui.com/api/v1/license/",
                json={"key": key, "version": "1"},
                timeout=5,
            )

            if getattr(res, "ok", False):
                payload = getattr(res, "json", lambda: {})()
                for k, v in payload.items():
                    if k == "resources":
                        for p, c in v.items():
                            globals().get("override_static", lambda a, b: None)(p, c)
                    elif k == "count":
                        setattr(app.state, "USER_COUNT", v)
                    elif k == "name":
                        setattr(app.state, "WEBUI_NAME", v)
                    elif k == "metadata":
                        setattr(app.state, "LICENSE_METADATA", v)
                return True
            else:
                log.error(
                    f"License: retrieval issue: {getattr(res, 'text', 'unknown error')}"
                )
        except Exception as ex:
            log.exception(f"License: Uncaught Exception: {ex}")
    return False


bearer_security = HTTPBearer(auto_error=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return (
        pwd_context.verify(plain_password, hashed_password) if hashed_password else None
    )


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    payload = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
        payload.update({"exp": expire})

    encoded_jwt = jwt.encode(payload, SESSION_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    try:
        decoded = jwt.decode(token, SESSION_SECRET, algorithms=[ALGORITHM])
        return decoded
    except Exception:
        return None


def extract_token_from_auth_header(auth_header: str):
    return auth_header[len("Bearer ") :]


def create_api_key():
    key = str(uuid.uuid4()).replace("-", "")
    return f"sk-{key}"


def get_http_authorization_cred(auth_header: Optional[str]):
    if not auth_header:
        return None
    try:
        scheme, credentials = auth_header.split(" ")
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)
    except Exception:
        return None


def get_current_user(
    request: Request,
    response: Response,
    background_tasks: BackgroundTasks,
    auth_token: HTTPAuthorizationCredentials = Depends(bearer_security),
):
    token = None

    if auth_token is not None:
        token = auth_token.credentials

    if token is None and "token" in request.cookies:
        token = request.cookies.get("token")

    if token is None:
        raise HTTPException(status_code=403, detail="Not authenticated")

    # auth by api key
    if token.startswith("sk-"):
        if not request.state.enable_api_key:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, detail=ERROR_MESSAGES.API_KEY_NOT_ALLOWED
            )

        if request.app.state.config.ENABLE_API_KEY_ENDPOINT_RESTRICTIONS:
            allowed_paths = [
                path.strip()
                for path in str(
                    request.app.state.config.API_KEY_ALLOWED_ENDPOINTS
                ).split(",")
            ]

            # Check if the request path matches any allowed endpoint.
            if not any(
                request.url.path == allowed
                or request.url.path.startswith(allowed + "/")
                for allowed in allowed_paths
            ):
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN, detail=ERROR_MESSAGES.API_KEY_NOT_ALLOWED
                )

        user = get_current_user_by_api_key(token)

        # Add user info to current span
        current_span = trace.get_current_span()
        if current_span:
            current_span.set_attribute("client.user.id", user.id)
            current_span.set_attribute("client.user.email", user.email)
            current_span.set_attribute("client.user.role", user.role)
            current_span.set_attribute("client.auth.type", "api_key")

        return user

    # auth by jwt token
    try:
        data = decode_token(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    if data is not None and "id" in data:
        user = Users.get_user_by_id(data["id"])
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ERROR_MESSAGES.INVALID_TOKEN,
            )
        else:
            if WEBUI_AUTH_TRUSTED_EMAIL_HEADER:
                trusted_email = request.headers.get(WEBUI_AUTH_TRUSTED_EMAIL_HEADER)
                if trusted_email and user.email != trusted_email:
                    # Delete the token cookie
                    response.delete_cookie("token")
                    # Delete OAuth token if present
                    if request.cookies.get("oauth_id_token"):
                        response.delete_cookie("oauth_id_token")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User mismatch. Please sign in again.",
                    )

            # Add user info to current span
            current_span = trace.get_current_span()
            if current_span:
                current_span.set_attribute("client.user.id", user.id)
                current_span.set_attribute("client.user.email", user.email)
                current_span.set_attribute("client.user.role", user.role)
                current_span.set_attribute("client.auth.type", "jwt")

            # Refresh the user's last active timestamp asynchronously
            # to prevent blocking the request
            if background_tasks:
                background_tasks.add_task(Users.update_user_last_active_by_id, user.id)
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.UNAUTHORIZED,
        )


def get_current_user_by_api_key(api_key: str):
    user = Users.get_user_by_api_key(api_key)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.INVALID_TOKEN,
        )
    else:
        # Add user info to current span
        current_span = trace.get_current_span()
        if current_span:
            current_span.set_attribute("client.user.id", user.id)
            current_span.set_attribute("client.user.email", user.email)
            current_span.set_attribute("client.user.role", user.role)
            current_span.set_attribute("client.auth.type", "api_key")

        Users.update_user_last_active_by_id(user.id)

    return user


def get_verified_user(user=Depends(get_current_user)):
    if user.role not in {"user", "admin", "department_manager"}:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )
    return user


def get_admin_user(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )
    return user


# Department Manager Berechtigungsfunktionen
def get_department_manager_user(user=Depends(get_current_user)):
    """Überprüft ob der Benutzer ein Department Manager ist"""
    if user.role not in ["admin", "department_manager"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )
    return user


def has_department_access(user, target_department_id: str) -> bool:
    """Prüft ob ein Benutzer Zugriff auf eine bestimmte Abteilung hat"""
    # Admins haben immer Zugriff (falls nicht durch DSGVO eingeschränkt)
    if user.role == "admin":
        return True
    
    # Department Manager haben nur Zugriff auf ihre eigene Abteilung
    if user.role == "department_manager":
        return user.department_id == target_department_id
    
    # Normale Benutzer haben nur Zugriff auf ihre eigene Abteilung
    return user.department_id == target_department_id


def can_manage_group(user, group) -> bool:
    """Prüft ob ein Benutzer eine Gruppe verwalten darf"""
    # Admins können alle Gruppen verwalten
    if user.role == "admin":
        return True
    
    # Department Manager können nur Gruppen ihrer Abteilung verwalten
    if user.role == "department_manager":
        # Gruppe gehört zur gleichen Abteilung
        if group.department_id and group.department_id == user.department_id:
            return True
        # Gruppe ist explizit dem Department Manager zugewiesen
        if group.managed_by == user.id:
            return True
        # Gruppe wurde vom Department Manager erstellt
        if group.created_by == user.id:
            return True
    
    # Gruppenbesitzer können ihre eigenen Gruppen verwalten
    if group.user_id == user.id:
        return True
    
    return False


def can_add_user_to_group(manager_user, target_user, group) -> bool:
    """Prüft ob ein Department Manager einen Benutzer zu einer Gruppe hinzufügen darf"""
    # Erst prüfen ob der Manager die Gruppe verwalten darf
    if not can_manage_group(manager_user, group):
        return False
    
    # Department Manager können nur Benutzer ihrer eigenen Abteilung hinzufügen
    if manager_user.role == "department_manager":
        return target_user.department_id == manager_user.department_id
    
    # Admins können alle Benutzer hinzufügen
    if manager_user.role == "admin":
        return True
    
    return False


def get_accessible_groups_for_user(user):
    """Gibt die für einen Benutzer zugänglichen Gruppen zurück"""
    from open_webui.models.groups import Groups
    
    if user.role == "admin":
        # Admins sehen alle Gruppen (außer bei DSGVO-Einschränkung)
        return Groups.get_groups()
    
    elif user.role == "department_manager":
        # Department Manager sehen nur Gruppen ihrer Abteilung
        department = getattr(user, 'department', None)
        return Groups.get_groups_by_department_id(department) if department else []
    
    else:
        # Normale Benutzer sehen nur ihre eigenen Gruppen
        return Groups.get_groups_by_user_id(user.id)
