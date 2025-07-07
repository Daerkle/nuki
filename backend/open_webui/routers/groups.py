import os
from pathlib import Path
from typing import Optional
import logging

from open_webui.models.users import Users
from open_webui.models.groups import (
    Groups,
    GroupForm,
    GroupUpdateForm,
    GroupResponse,
)

from open_webui.config import CACHE_DIR
from open_webui.constants import ERROR_MESSAGES
from fastapi import APIRouter, Depends, HTTPException, Request, status

from open_webui.utils.auth import (
    get_admin_user, 
    get_verified_user,
    get_department_manager_user,
    can_manage_group,
    can_add_user_to_group,
    get_accessible_groups_for_user
)
from open_webui.env import SRC_LOG_LEVELS


log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MAIN"])

router = APIRouter()

############################
# GetFunctions
############################


@router.get("/", response_model=list[GroupResponse])
async def get_groups(user=Depends(get_verified_user)):
    """Gibt Gruppen basierend auf Benutzerrolle zurück"""
    if user.role == "admin":
        return Groups.get_groups()
    elif user.role == "department_manager":
        # Department Manager sehen alle Gruppen (vereinfacht für jetzt)
        return Groups.get_groups()
    else:
        return Groups.get_groups_by_member_id(user.id)


############################
# CreateNewGroup
############################


@router.post("/create", response_model=Optional[GroupResponse])
async def create_new_group(form_data: GroupForm, user=Depends(get_department_manager_user)):
    """Erstellt eine neue Gruppe - Admins und Department Manager"""
    try:
        if user.role == "department_manager":
            # Department Manager erstellen Gruppen für ihre Abteilung
            group = Groups.create_group_by_department_manager(
                user.id, getattr(user, 'department', None), form_data
            )
        else:
            # Admin erstellt normale Gruppe
            group = Groups.insert_new_group(user.id, form_data)
            
        if group:
            return group
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES.DEFAULT("Error creating group"),
            )
    except Exception as e:
        log.exception(f"Error creating a new group: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT(e),
        )


############################
# GetGroupById
############################


@router.get("/id/{id}", response_model=Optional[GroupResponse])
async def get_group_by_id(id: str, user=Depends(get_department_manager_user)):
    group = Groups.get_group_by_id(id)
    if group:
        return group
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )


############################
# UpdateGroupById
############################


@router.post("/id/{id}/update", response_model=Optional[GroupResponse])
async def update_group_by_id(
    id: str, form_data: GroupUpdateForm, user=Depends(get_department_manager_user)
):
    try:
        if form_data.user_ids:
            form_data.user_ids = Users.get_valid_user_ids(form_data.user_ids)

        group = Groups.update_group_by_id(id, form_data)
        if group:
            return group
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES.DEFAULT("Error updating group"),
            )
    except Exception as e:
        log.exception(f"Error updating group {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT(e),
        )


############################
# DeleteGroupById
############################


@router.delete("/id/{id}/delete", response_model=bool)
async def delete_group_by_id(id: str, user=Depends(get_department_manager_user)):
    try:
        result = Groups.delete_group_by_id(id)
        if result:
            return result
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES.DEFAULT("Error deleting group"),
            )
    except Exception as e:
        log.exception(f"Error deleting group {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT(e),
        )


############################
# Department Manager Endpoints
############################


@router.get("/managed", response_model=list[GroupResponse])
async def get_managed_groups(user=Depends(get_department_manager_user)):
    """Gibt alle vom Department Manager verwalteten Gruppen zurück"""
    if user.role == "department_manager":
        return Groups.get_managed_groups_by_user_id(user.id)
    elif user.role == "admin":
        # Admins sehen alle Gruppen
        return Groups.get_groups()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )


@router.get("/department/{department_id}", response_model=list[GroupResponse])
async def get_groups_by_department(department_id: str, user=Depends(get_department_manager_user)):
    """Gibt alle Gruppen einer Abteilung zurück"""
    # Prüfen ob Benutzer Zugriff auf diese Abteilung hat
    if user.role == "admin":
        return Groups.get_groups_by_department_id(department_id)
    elif user.role == "department_manager" and getattr(user, 'department', None) == department_id:
        return Groups.get_groups_by_department_id(department_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )


@router.post("/{group_id}/members/add")
async def add_user_to_group(
    group_id: str, 
    user_id: str, 
    manager=Depends(get_department_manager_user)
):
    """Fügt einen Benutzer zu einer Gruppe hinzu (Department Manager)"""
    try:
        # Gruppe und Zielbenutzer abrufen
        group = Groups.get_group_by_id(group_id)
        target_user = Users.get_user_by_id(user_id)
        
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )
        
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Berechtigung prüfen
        if not can_add_user_to_group(manager, target_user, group):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
            )
        
        # Benutzer zur Gruppe hinzufügen
        success = Groups.add_user_to_group_by_id(group_id, user_id)
        
        if success:
            return {"message": "User added to group successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to add user to group"
            )
            
    except Exception as e:
        log.exception(f"Error adding user {user_id} to group {group_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT(e),
        )


@router.post("/{group_id}/members/remove")
async def remove_user_from_group(
    group_id: str, 
    user_id: str, 
    manager=Depends(get_department_manager_user)
):
    """Entfernt einen Benutzer aus einer Gruppe (Department Manager)"""
    try:
        # Gruppe abrufen
        group = Groups.get_group_by_id(group_id)
        
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )
        
        # Berechtigung prüfen
        if not can_manage_group(manager, group):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
            )
        
        # Benutzer aus Gruppe entfernen
        success = Groups.delete_user_from_group_by_id(group_id, user_id)
        
        if success:
            return {"message": "User removed from group successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to remove user from group"
            )
            
    except Exception as e:
        log.exception(f"Error removing user {user_id} from group {group_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT(e),
        )


@router.get("/stats/department")
async def get_department_stats(user=Depends(get_department_manager_user)):
    """Gibt Statistiken für die Abteilung des Department Managers zurück"""
    if user.role == "department_manager" and getattr(user, 'department', None):
        try:
            department = getattr(user, 'department', None)
            groups = Groups.get_groups() if department else []  # Vereinfacht für jetzt
            managed_groups = []  # Vereinfacht für jetzt

            # Benutzer in der Abteilung zählen
            department_users = []  # Vereinfacht für jetzt

            return {
                "department": department,
                "total_groups": len(groups),
                "managed_groups": len(managed_groups),
                "department_users": len(department_users),
                "groups": [{"id": g.id, "name": g.name, "member_count": len(g.user_ids or [])} for g in groups]
            }
        except Exception as e:
            log.exception(f"Error getting department stats: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES.DEFAULT(e),
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )
