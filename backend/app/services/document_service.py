from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.document_repository import (
    create_document,
    delete_document,
    get_document,
    get_documents,
    update_document_status,
)


def create_document_service(
    db: Session,
    user_id: UUID,
    filename: str,
    file_url: str,
    content_type: str | None,
):
    return create_document(
        db,
        user_id,
        filename,
        file_url,
        content_type,
    )


def get_documents_service(
    db: Session,
    user_id: UUID,
    page: int,
    page_size: int,
):
    return get_documents(
        db=db,
        user_id=user_id,
        page=page,
        page_size=page_size,
    )

def get_document_service(
    db: Session,
    user_id: UUID,
    document_id: UUID,
):
    return get_document(
        db,
        user_id,
        document_id,
    )


def update_document_status_service(
    db: Session,
    user_id: UUID,
    document_id: UUID,
    status: str,
):
    return update_document_status(
        db,
        user_id,
        document_id,
        status,
    )


def delete_document_service(
    db: Session,
    user_id: UUID,
    document_id: UUID,
):
    return delete_document(
        db,
        user_id,
        document_id,
    )