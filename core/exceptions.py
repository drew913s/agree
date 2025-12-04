"""Custom exceptions for the Agree application."""

from typing import Any, Dict, Optional


class AgreeException(Exception):
    """Base exception for Agree application."""

    def __init__(
        self,
        message: str,
        code: str = "AGREE_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


# Authentication Exceptions
class AuthenticationError(AgreeException):
    """Authentication failed."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="AUTH_ERROR")


class TokenExpiredError(AuthenticationError):
    """Token has expired."""

    def __init__(self):
        super().__init__("Token has expired")
        self.code = "TOKEN_EXPIRED"


class InvalidTokenError(AuthenticationError):
    """Token is invalid."""

    def __init__(self):
        super().__init__("Invalid token")
        self.code = "INVALID_TOKEN"


# Authorization Exceptions
class AuthorizationError(AgreeException):
    """User not authorized for this action."""

    def __init__(self, message: str = "Not authorized"):
        super().__init__(message, code="AUTHORIZATION_ERROR")


class ResourceNotFoundError(AgreeException):
    """Requested resource not found."""

    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            f"{resource} not found: {resource_id}",
            code="NOT_FOUND",
            details={"resource": resource, "id": resource_id},
        )


# Document Exceptions
class DocumentError(AgreeException):
    """Document-related error."""

    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, code="DOCUMENT_ERROR", details=details)


class InvalidPDFError(DocumentError):
    """PDF file is invalid or corrupted."""

    def __init__(self, reason: str = "Invalid PDF file"):
        super().__init__(reason)
        self.code = "INVALID_PDF"


class DocumentNotEditableError(DocumentError):
    """Document cannot be edited in current state."""

    def __init__(self, status: str):
        super().__init__(
            f"Document cannot be edited in status: {status}",
            details={"status": status},
        )
        self.code = "NOT_EDITABLE"


# Signing Exceptions
class SigningError(AgreeException):
    """Signing-related error."""

    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, code="SIGNING_ERROR", details=details)


class SigningTokenInvalidError(SigningError):
    """Signing token is invalid or expired."""

    def __init__(self):
        super().__init__("Signing link is invalid or has expired")
        self.code = "INVALID_SIGNING_TOKEN"


class AlreadySignedError(SigningError):
    """Document has already been signed by this signer."""

    def __init__(self):
        super().__init__("You have already signed this document")
        self.code = "ALREADY_SIGNED"


# Validation Exceptions
class ValidationError(AgreeException):
    """Input validation error."""

    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            message,
            code="VALIDATION_ERROR",
            details={"field": field} if field else {},
        )


class FileTooLargeError(ValidationError):
    """Uploaded file exceeds size limit."""

    def __init__(self, max_size_mb: int):
        super().__init__(
            f"File size exceeds maximum limit of {max_size_mb}MB",
            field="file",
        )
        self.code = "FILE_TOO_LARGE"


# Rate Limiting Exceptions
class RateLimitExceededError(AgreeException):
    """Rate limit exceeded."""

    def __init__(self, retry_after: int = 60):
        super().__init__(
            "Rate limit exceeded. Please try again later.",
            code="RATE_LIMIT_EXCEEDED",
            details={"retry_after": retry_after},
        )


# Storage Exceptions
class StorageError(AgreeException):
    """Storage operation failed."""

    def __init__(self, message: str, operation: str):
        super().__init__(
            message,
            code="STORAGE_ERROR",
            details={"operation": operation},
        )


# Email Exceptions
class EmailError(AgreeException):
    """Email sending failed."""

    def __init__(self, message: str, recipient: Optional[str] = None):
        super().__init__(
            message,
            code="EMAIL_ERROR",
            details={"recipient": recipient} if recipient else {},
        )
