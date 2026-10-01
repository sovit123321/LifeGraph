from datetime import datetime
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(
    db: Session,
    user_id: UUID,
    filename: str,
    file_url: str,
    content_type: str | None,
):
    document = Document(
        user_id=user_id,
        filename=filename,
        file_url=file_url,
        content_type=content_type,
        status="uploaded",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_documents(
    db: Session,
    user_id: UUID,
    page: int,
    page_size: int,
):
    offset = (page - 1) * page_size

    total = db.scalar(
        select(func.count(Document.id)).where(
            Document.user_id == user_id,
            Document.deleted_at.is_(None),
        )
    )

    statement = (
        select(Document)
        .where(
            Document.user_id == user_id,
            Document.deleted_at.is_(None),
        )
        .order_by(Document.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )

    items = list(db.scalars(statement).all())

    return {
        "items": items,
        "total": total or 0,
        "page": page,
        "page_size": page_size,
    }


def get_document(
    db: Session,
    user_id: UUID,
    document_id: UUID,
):
    statement = select(Document).where(
        Document.id == document_id,
        Document.user_id == user_id,
        Document.deleted_at.is_(None),
    )

    return db.scalars(statement).first()


def update_document_status(
    db: Session,
    user_id: UUID,
    document_id: UUID,
    status: str,
):
    document = get_document(
        db,
        user_id,
        document_id,
    )

    if not document:
        return None

    document.status = status

    db.commit()
    db.refresh(document)

    return document


def delete_document(
    db: Session,
    user_id: UUID,
    document_id: UUID,
):
    document = get_document(
        db,
        user_id,
        document_id,
    )

    if not document:
        return None

    document.deleted_at = datetime.utcnow()

    db.commit()
    db.refresh(document)

    return document