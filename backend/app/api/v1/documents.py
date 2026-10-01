import os
import uuid
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Query, Request, UploadFile, status
from sqlalchemy.orm import Session
from app.core.rate_limit import limiter
from app.core.auth.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.services.document_service import (
    create_document_service,
    delete_document_service,
    get_document_service,
    get_documents_service,
    update_document_status_service,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("10/minute")
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    extension = Path(file.filename).suffix
    stored_filename = f"{uuid.uuid4()}{extension}"
    file_path = UPLOAD_DIR / stored_filename

    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    document = create_document_service(
        db=db,
        user_id=current_user.id,
        filename=file.filename,
        file_url=str(file_path),
        content_type=file.content_type,
    )

    return document


@router.get("")
def get_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_documents_service(
        db=db,
        user_id=current_user.id,
        page=page,
        page_size=page_size,
    )

@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    document = get_document_service(
        db=db,
        user_id=current_user.id,
        document_id=document_id,
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return document


@router.patch(
    "/{document_id}/status",
    response_model=DocumentResponse,
)
def update_document_status(
    document_id: UUID,
    status_value: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    document = update_document_status_service(
        db=db,
        user_id=current_user.id,
        document_id=document_id,
        status=status_value,
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return document


@router.delete(
    "/{document_id}",
    response_model=DocumentResponse,
)
def delete_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    document = delete_document_service(
        db=db,
        user_id=current_user.id,
        document_id=document_id,
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return document