from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status, Request
import logging

from open_webui.models.knowledge import (
    Knowledges,
    KnowledgeForm,
    KnowledgeResponse,
    KnowledgeUserResponse,
)
from open_webui.models.files import Files, FileModel, FileMetadataResponse
from open_webui.retrieval.vector.factory import VECTOR_DB_CLIENT
from open_webui.routers.retrieval import (
    process_file,
    ProcessFileForm,
    process_files_batch,
    BatchProcessFilesForm,
)
from open_webui.storage.provider import Storage

from open_webui.constants import ERROR_MESSAGES
from open_webui.utils.auth import get_verified_user
from open_webui.utils.access_control import has_access, has_permission
from open_webui.config import ENABLE_ADMIN_KNOWLEDGE_ACCESS_OVERRIDE

from open_webui.env import SRC_LOG_LEVELS
from open_webui.models.models import Models, ModelForm


log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

router = APIRouter()

# DSGVO-konforme Hilfsfunktionen
def has_access_to_knowledge(user, knowledge) -> bool:
    """
    Prüft, ob ein Benutzer Zugriff auf eine Wissensdatenbank hat.
    DSGVO-konform: Admins haben NICHT automatisch Zugriff auf alle Datenbanken.
    """
    # Besitzer hat immer Zugriff
    if knowledge.user_id == user.id:
        return True
    
    # Prüfe explizite Berechtigungen
    if hasattr(knowledge, 'access_control') and knowledge.access_control:
        if has_access(user.id, "read", knowledge.access_control):
            return True
    
    # Legacy-Modus: Wenn aktiviert, haben Admins vollen Zugriff (NICHT DSGVO-konform!)
    if ENABLE_ADMIN_KNOWLEDGE_ACCESS_OVERRIDE and user.role == "admin":
        log.warning(f"WARNUNG: Admin {user.id} greift via Legacy-Modus auf Knowledge {knowledge.id} zu")
        return True
    
    return False

def has_write_access_to_knowledge(user, knowledge) -> bool:
    """
    Prüft, ob ein Benutzer Schreibzugriff auf eine Wissensdatenbank hat.
    """
    # Besitzer hat immer Schreibzugriff
    if knowledge.user_id == user.id:
        return True
    
    # Prüfe explizite Schreibberechtigungen
    if hasattr(knowledge, 'access_control') and knowledge.access_control:
        if has_access(user.id, "write", knowledge.access_control):
            return True
    
    # Legacy-Modus für Admins (falls aktiviert)
    if ENABLE_ADMIN_KNOWLEDGE_ACCESS_OVERRIDE and user.role == "admin":
        log.warning(f"WARNUNG: Admin {user.id} nutzt Legacy-Schreibzugriff auf Knowledge {knowledge.id}")
        return True
    
    return False

############################
# getKnowledgeBases
############################


@router.get("/", response_model=list[KnowledgeUserResponse])
async def get_knowledge(user=Depends(get_verified_user)):
    knowledge_bases = []

    # DSGVO-konform: Auch Admins sehen nur ihre eigenen + explizit freigegebene Datenbanken
    knowledge_bases = Knowledges.get_knowledge_bases_by_user_id(user.id, "read")

    # Get files for each knowledge base
    knowledge_with_files = []
    for knowledge_base in knowledge_bases:
        files = []
        if knowledge_base.data:
            files = Files.get_file_metadatas_by_ids(
                knowledge_base.data.get("file_ids", [])
            )

            # Check if all files exist
            if len(files) != len(knowledge_base.data.get("file_ids", [])):
                missing_files = list(
                    set(knowledge_base.data.get("file_ids", []))
                    - set([file.id for file in files])
                )
                if missing_files:
                    data = knowledge_base.data or {}
                    file_ids = data.get("file_ids", [])

                    for missing_file in missing_files:
                        file_ids.remove(missing_file)

                    data["file_ids"] = file_ids
                    Knowledges.update_knowledge_data_by_id(
                        id=knowledge_base.id, data=data
                    )

                    files = Files.get_file_metadatas_by_ids(file_ids)

        knowledge_with_files.append(
            KnowledgeUserResponse(
                **knowledge_base.model_dump(),
                files=files,
            )
        )

    return knowledge_with_files

@router.get("/list", response_model=list[KnowledgeUserResponse])
async def get_knowledge_list(user=Depends(get_verified_user)):
    knowledge_bases = []

    # DSGVO-konform: Auch Admins sehen nur ihre eigenen + explizit freigegebene Datenbanken
    knowledge_bases = Knowledges.get_knowledge_bases_by_user_id(user.id, "write")

    # Get files for each knowledge base
    knowledge_with_files = []
    for knowledge_base in knowledge_bases:
        files = []
        if knowledge_base.data:
            files = Files.get_file_metadatas_by_ids(
                knowledge_base.data.get("file_ids", [])
            )

            # Check if all files exist
            if len(files) != len(knowledge_base.data.get("file_ids", [])):
                missing_files = list(
                    set(knowledge_base.data.get("file_ids", []))
                    - set([file.id for file in files])
                )
                if missing_files:
                    data = knowledge_base.data or {}
                    file_ids = data.get("file_ids", [])

                    for missing_file in missing_files:
                        file_ids.remove(missing_file)

                    data["file_ids"] = file_ids
                    Knowledges.update_knowledge_data_by_id(
                        id=knowledge_base.id, data=data
                    )

                    files = Files.get_file_metadatas_by_ids(file_ids)

        knowledge_with_files.append(
            KnowledgeUserResponse(
                **knowledge_base.model_dump(),
                files=files,
            )
        )
    return knowledge_with_files


############################
# CreateNewKnowledge
############################


############################
# CreateNewKnowledge
############################


@router.post("/create", response_model=Optional[KnowledgeResponse])
async def create_new_knowledge(
    request: Request, form_data: KnowledgeForm, user=Depends(get_verified_user)
):
    if user.role != "admin" and not has_permission(
        user.id, "workspace.knowledge", request.app.state.config.USER_PERMISSIONS
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.UNAUTHORIZED,
        )

    knowledge = Knowledges.insert_new_knowledge(user.id, form_data)

    if knowledge:
        return knowledge
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.FILE_EXISTS,
        )


############################
# ReindexKnowledgeFiles
############################


@router.post("/reindex", response_model=bool)
async def reindex_knowledge_files(request: Request, user=Depends(get_verified_user)):
    """
    Reindexiert Wissensdatenbanken.
    DSGVO-konform: Nur zugängliche Datenbanken werden reindexiert.
    """
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.UNAUTHORIZED,
        )

    # DSGVO-konforme Filterung: Nur zugängliche Wissensdatenbanken
    all_knowledge_bases = Knowledges.get_knowledge_bases()
    
    if ENABLE_ADMIN_KNOWLEDGE_ACCESS_OVERRIDE:
        # Legacy-Modus: Admin kann alle reindexieren
        knowledge_bases = all_knowledge_bases
        log.warning(f"DATENSCHUTZ-WARNUNG: Admin {user.id} reindexiert ALLE {len(knowledge_bases)} Wissensdatenbanken (Legacy-Modus)")
    else:
        # DSGVO-konformer Modus: Nur zugängliche reindexieren
        knowledge_bases = []
        for kb in all_knowledge_bases:
            if has_access_to_knowledge(user, kb):
                knowledge_bases.append(kb)
        
        log.info(f"Admin {user.id} reindexiert {len(knowledge_bases)} von {len(all_knowledge_bases)} zugänglichen Wissensdatenbanken")

    log.info(f"Starting reindexing for {len(knowledge_bases)} knowledge bases")

    deleted_knowledge_bases = []

    for knowledge_base in knowledge_bases:
        # -- Robust error handling for missing or invalid data
        if not knowledge_base.data or not isinstance(knowledge_base.data, dict):
            log.warning(
                f"Knowledge base {knowledge_base.id} has no data or invalid data ({knowledge_base.data!r}). Deleting."
            )
            try:
                Knowledges.delete_knowledge_by_id(id=knowledge_base.id)
                deleted_knowledge_bases.append(knowledge_base.id)
            except Exception as e:
                log.error(
                    f"Failed to delete invalid knowledge base {knowledge_base.id}: {e}"
                )
            continue

        try:
            file_ids = knowledge_base.data.get("file_ids", [])
            files = Files.get_files_by_ids(file_ids)
            try:
                if VECTOR_DB_CLIENT.has_collection(collection_name=knowledge_base.id):
                    VECTOR_DB_CLIENT.delete_collection(
                        collection_name=knowledge_base.id
                    )
            except Exception as e:
                log.error(f"Error deleting collection {knowledge_base.id}: {str(e)}")
                continue  # Skip, don't raise

            failed_files = []
            for file in files:
                try:
                    process_file(
                        request,
                        ProcessFileForm(
                            file_id=file.id, collection_name=knowledge_base.id
                        ),
                        user=user,
                    )
                except Exception as e:
                    log.error(
                        f"Error processing file {file.filename} (ID: {file.id}): {str(e)}"
                    )
                    failed_files.append({"file_id": file.id, "error": str(e)})
                    continue

        except Exception as e:
            log.error(f"Error processing knowledge base {knowledge_base.id}: {str(e)}")
            # Don't raise, just continue
            continue

        if failed_files:
            log.warning(
                f"Failed to process {len(failed_files)} files in knowledge base {knowledge_base.id}"
            )
            for failed in failed_files:
                log.warning(f"File ID: {failed['file_id']}, Error: {failed['error']}")

    log.info(
        f"Reindexing completed. Deleted {len(deleted_knowledge_bases)} invalid knowledge bases: {deleted_knowledge_bases}"
    )
    return True


############################
# GetKnowledgeById
############################


class KnowledgeFilesResponse(KnowledgeResponse):
    files: list[FileMetadataResponse]


@router.get("/{id}", response_model=Optional[KnowledgeFilesResponse])
async def get_knowledge_by_id(id: str, user=Depends(get_verified_user)):
    """
    Gibt eine spezifische Wissensdatenbank zurück.
    DSGVO-konform: Zugriff nur wenn explizit berechtigt.
    """
    knowledge = Knowledges.get_knowledge_by_id(id=id)

    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

    if not has_access_to_knowledge(user, knowledge):
        log.warning(f"Zugriff verweigert: Benutzer {user.id} ({user.role}) versuchte auf Knowledge {id} zuzugreifen")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sie haben keine Berechtigung, auf diese Wissensdatenbank zuzugreifen.",
        )

    file_ids = knowledge.data.get("file_ids", []) if knowledge.data else []
    files = Files.get_file_metadatas_by_ids(file_ids)

    return KnowledgeFilesResponse(
        **knowledge.model_dump(),
        files=files,
    )


############################
# UpdateKnowledgeById
############################


@router.post("/{id}/update", response_model=Optional[KnowledgeFilesResponse])
async def update_knowledge_by_id(
    id: str,
    form_data: KnowledgeForm,
    user=Depends(get_verified_user),
):
    """
    Aktualisiert eine Wissensdatenbank.
    DSGVO-konform: Nur mit Schreibberechtigung.
    """
    knowledge = Knowledges.get_knowledge_by_id(id=id)
    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

    if not has_write_access_to_knowledge(user, knowledge):
        log.warning(f"Schreibzugriff verweigert: Benutzer {user.id} ({user.role}) versuchte Knowledge {id} zu bearbeiten")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sie haben keine Schreibberechtigung für diese Wissensdatenbank.",
        )

    knowledge = Knowledges.update_knowledge_by_id(id=id, form_data=form_data)
    if knowledge:
        file_ids = knowledge.data.get("file_ids", []) if knowledge.data else []
        files = Files.get_files_by_ids(file_ids)

        return KnowledgeFilesResponse(
            **knowledge.model_dump(),
            files=files,
        )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_MESSAGES.ID_TAKEN)


############################
# AddFileToKnowledge
############################


class KnowledgeFileIdForm(BaseModel):
    file_id: str


@router.post("/{id}/file/add", response_model=Optional[KnowledgeFilesResponse])
def add_file_to_knowledge_by_id(
    request: Request,
    id: str,
    form_data: KnowledgeFileIdForm,
    user=Depends(get_verified_user),
):
    knowledge = Knowledges.get_knowledge_by_id(id=id)

    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

    if not has_write_access_to_knowledge(user, knowledge):
        log.warning(f"Schreibzugriff verweigert: Benutzer {user.id} ({user.role}) versuchte Datei zu Knowledge {id} hinzuzufügen")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sie haben keine Schreibberechtigung für diese Wissensdatenbank.",
        )

    file = Files.get_file_by_id(form_data.file_id)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )
    if not file.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.FILE_NOT_PROCESSED,
        )

    # Add content to the vector database
    try:
        process_file(
            request,
            ProcessFileForm(file_id=form_data.file_id, collection_name=id),
            user=user,
        )
    except Exception as e:
        log.debug(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    if knowledge:
        data = knowledge.data or {}
        file_ids = data.get("file_ids", [])

        if form_data.file_id not in file_ids:
            file_ids.append(form_data.file_id)
            data["file_ids"] = file_ids

        knowledge = Knowledges.update_knowledge_data_by_id(id=id, data=data)

        if knowledge:
            files = Files.get_file_metadatas_by_ids(file_ids)

            return KnowledgeFilesResponse(
                **knowledge.model_dump(),
                files=files,
            )
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
