"""Enums for document workflow and status tracking."""

from enum import Enum


class DocumentStatus(str, Enum):
    """Document lifecycle status."""

    DRAFT = "draft"
    SENT = "sent"
    VIEWED = "viewed"
    PARTIALLY_SIGNED = "partially_signed"
    COMPLETED = "completed"
    VOIDED = "voided"
    EXPIRED = "expired"


class SignerStatus(str, Enum):
    """Individual signer status."""

    PENDING = "pending"
    SENT = "sent"
    VIEWED = "viewed"
    SIGNED = "signed"
    DECLINED = "declined"


class FieldType(str, Enum):
    """Types of form fields in documents."""

    SIGNATURE = "signature"
    INITIALS = "initials"
    TEXT = "text"
    DATE = "date"
    CHECKBOX = "checkbox"
    DROPDOWN = "dropdown"


class SignatureType(str, Enum):
    """How signature was captured."""

    DRAWN = "drawn"
    TYPED = "typed"
    UPLOADED = "uploaded"


class EventType(str, Enum):
    """Audit trail event types."""

    # Document events
    DOCUMENT_CREATED = "document.created"
    DOCUMENT_UPLOADED = "document.uploaded"
    DOCUMENT_SENT = "document.sent"
    DOCUMENT_VIEWED = "document.viewed"
    DOCUMENT_COMPLETED = "document.completed"
    DOCUMENT_VOIDED = "document.voided"
    DOCUMENT_EXPIRED = "document.expired"
    DOCUMENT_DOWNLOADED = "document.downloaded"

    # Signer events
    SIGNER_ADDED = "signer.added"
    SIGNER_REMOVED = "signer.removed"
    SIGNER_INVITED = "signer.invited"
    SIGNER_VIEWED = "signer.viewed"
    SIGNER_SIGNED = "signer.signed"
    SIGNER_DECLINED = "signer.declined"

    # Field events
    FIELD_ADDED = "field.added"
    FIELD_REMOVED = "field.removed"
    FIELD_FILLED = "field.filled"

    # Notification events
    REMINDER_SENT = "reminder.sent"
    NOTIFICATION_SENT = "notification.sent"

    # Auth events
    TOKEN_GENERATED = "token.generated"
    TOKEN_USED = "token.used"
    TOKEN_EXPIRED = "token.expired"

    # Security events
    ACCESS_DENIED = "access.denied"
    RATE_LIMITED = "rate.limited"


class StorageBackend(str, Enum):
    """Supported storage backends."""

    MINIO = "minio"
    GCS = "gcs"
    LOCAL = "local"


class WebhookEvent(str, Enum):
    """Webhook event types."""

    DOCUMENT_SENT = "document.sent"
    DOCUMENT_VIEWED = "document.viewed"
    DOCUMENT_COMPLETED = "document.completed"
    DOCUMENT_VOIDED = "document.voided"
    SIGNER_SIGNED = "signer.signed"
    SIGNER_DECLINED = "signer.declined"
