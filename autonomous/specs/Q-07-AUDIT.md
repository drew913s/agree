# Princess Q-07: Audit Domain

## Overview
Build 8 audit bricks for immutable event logging with hash chain integrity.

## Brick Rules
- Maximum 50 lines of code per brick
- Return format: `{'result': X, 'error': str|None}`
- Create `{name}.py` + `{name}.meta.json` + `test_{name}.py`
- Location: `bricks/audit/`

## Dependencies Available
- `sqlalchemy` - Database operations
- `hashlib` - SHA-256 hashing
- `json` - Deterministic serialization
- `datetime` - Timestamp handling
- `models.enums.EventType` - Event type enum

## Event Types (from models/enums.py)
```python
class EventType(str, Enum):
    DOCUMENT_CREATED = "document.created"
    DOCUMENT_UPDATED = "document.updated"
    DOCUMENT_SENT = "document.sent"
    DOCUMENT_VIEWED = "document.viewed"
    DOCUMENT_COMPLETED = "document.completed"
    DOCUMENT_VOIDED = "document.voided"
    SIGNER_INVITED = "signer.invited"
    SIGNER_VIEWED = "signer.viewed"
    SIGNER_SIGNED = "signer.signed"
    SIGNER_DECLINED = "signer.declined"
    FIELD_FILLED = "field.filled"
    USER_LOGIN = "user.login"
    USER_LOGOUT = "user.logout"
```

---

## Bricks to Build (in order)

### 1. log_event.py
**Purpose**: Log audit event with hash chain integrity

**Function Signature**:
```python
async def log_event(
    db_session,
    event_type: str,
    document_id: str = None,
    signer_id: str = None,
    user_id: str = None,
    ip_hash: str = None,
    metadata: dict = None
) -> dict:
```

**Inputs**:
- `db_session`: SQLAlchemy async session
- `event_type`: EventType enum value
- `document_id`: Optional document UUID
- `signer_id`: Optional signer UUID
- `user_id`: Optional user UUID
- `ip_hash`: Hashed IP address
- `metadata`: Additional event data

**Output**:
```python
{
    'result': {
        'event_id': 'uuid',
        'event_hash': 'sha256...',
        'timestamp': '2024-01-15T10:30:00Z'
    },
    'error': None
}
```

**Implementation Notes**:
- Get previous event's hash for chain
- Compute new event hash
- Insert atomically
- Use UTC timestamps

**Tests Required**:
- `test_logs_event()` - Event created in DB
- `test_chain_integrity()` - Hash links to previous
- `test_handles_first_event()` - Genesis event works

---

### 2. get_trail.py
**Purpose**: Retrieve audit trail for a document

**Function Signature**:
```python
async def get_audit_trail(
    db_session,
    document_id: str,
    limit: int = 100
) -> dict:
```

**Inputs**:
- `db_session`: SQLAlchemy async session
- `document_id`: Document UUID
- `limit`: Maximum events to return

**Output**:
```python
{
    'result': {
        'events': [
            {
                'id': 'uuid',
                'event_type': 'document.created',
                'timestamp': '2024-01-15T10:30:00Z',
                'actor_id': 'uuid',
                'metadata': {},
                'event_hash': 'sha256...'
            },
            ...
        ],
        'total': 15,
        'chain_valid': True
    },
    'error': None
}
```

**Implementation Notes**:
- Order by timestamp ascending
- Include chain validation status
- Paginate for large trails

**Tests Required**:
- `test_retrieves_events()` - Events returned in order
- `test_filters_by_document()` - Only matching events
- `test_validates_chain()` - Chain integrity checked

---

### 3. verify_chain.py
**Purpose**: Verify audit trail hash chain integrity

**Function Signature**:
```python
async def verify_chain(
    db_session,
    document_id: str = None
) -> dict:
```

**Inputs**:
- `db_session`: SQLAlchemy async session
- `document_id`: Optional - verify specific document or all

**Output**:
```python
{
    'result': {
        'valid': True,
        'events_checked': 150,
        'first_invalid_at': None  # Event ID if chain broken
    },
    'error': None
}
```

**Implementation Notes**:
- Recompute each hash from previous
- Stop at first mismatch
- Report which event broke chain

**Tests Required**:
- `test_valid_chain_passes()` - Clean chain verified
- `test_detects_tampering()` - Modified event caught
- `test_handles_empty_chain()` - No events is valid

---

### 4. event_types.py
**Purpose**: Event type definitions and validation

**Function Signature**:
```python
def get_event_types() -> dict:

def validate_event_type(event_type: str) -> dict:

def get_event_category(event_type: str) -> dict:
```

**Inputs**:
- `event_type`: Event type string to validate

**Output (get_event_types)**:
```python
{
    'result': {
        'document': ['document.created', 'document.updated', ...],
        'signer': ['signer.invited', 'signer.signed', ...],
        'user': ['user.login', 'user.logout']
    },
    'error': None
}
```

**Implementation Notes**:
- Group by category (document, signer, user)
- Include human-readable descriptions
- Validate against enum

**Tests Required**:
- `test_lists_all_types()` - All types returned
- `test_validates_known_type()` - Valid type passes
- `test_rejects_unknown_type()` - Invalid type fails

---

### 5. timestamp.py
**Purpose**: Generate consistent UTC timestamps

**Function Signature**:
```python
def get_timestamp() -> dict:

def parse_timestamp(ts_string: str) -> dict:

def format_timestamp(dt: datetime) -> dict:
```

**Inputs**:
- `ts_string`: ISO format timestamp string
- `dt`: Python datetime object

**Output (get_timestamp)**:
```python
{
    'result': {
        'iso': '2024-01-15T10:30:00.123456Z',
        'unix': 1705315800,
        'unix_ms': 1705315800123
    },
    'error': None
}
```

**Implementation Notes**:
- Always UTC timezone
- Microsecond precision
- ISO 8601 format with Z suffix

**Tests Required**:
- `test_returns_utc()` - Timezone is UTC
- `test_parses_iso_format()` - String parsing works
- `test_formats_consistently()` - Same datetime = same string

---

### 6. format_event.py
**Purpose**: Format audit event for display

**Function Signature**:
```python
def format_event(
    event: dict,
    include_hash: bool = False
) -> dict:
```

**Inputs**:
- `event`: Raw event dict from database
- `include_hash`: Whether to show hash in output

**Output**:
```python
{
    'result': {
        'id': 'uuid',
        'type': 'Document Signed',
        'description': 'John Smith signed the document',
        'timestamp': 'Jan 15, 2024 10:30 AM',
        'relative_time': '2 hours ago',
        'actor': {'name': 'John Smith', 'email': 'john@...'},
        'icon': 'signature'
    },
    'error': None
}
```

**Implementation Notes**:
- Human-readable event type names
- Relative timestamps (e.g., "2 hours ago")
- Icon mapping for UI
- Mask sensitive data

**Tests Required**:
- `test_formats_event_type()` - Type is readable
- `test_relative_time()` - Time ago calculated
- `test_masks_email()` - Partial email shown

---

### 7. export_trail.py
**Purpose**: Export audit trail as PDF or JSON

**Function Signature**:
```python
async def export_audit_trail(
    db_session,
    document_id: str,
    format: str = "json"
) -> dict:
```

**Inputs**:
- `db_session`: SQLAlchemy async session
- `document_id`: Document UUID
- `format`: "json" or "pdf"

**Output**:
```python
{
    'result': {
        'content': b'...',  # File bytes
        'content_type': 'application/json',
        'filename': 'audit_trail_abc123.json'
    },
    'error': None
}
```

**Implementation Notes**:
- JSON: Pretty-printed with verification info
- PDF: Formatted report with timestamps
- Include chain verification status

**Tests Required**:
- `test_exports_json()` - Valid JSON output
- `test_exports_pdf()` - Valid PDF output
- `test_includes_verification()` - Chain status included

---

### 8. search_events.py
**Purpose**: Search audit events with filters

**Function Signature**:
```python
async def search_events(
    db_session,
    filters: dict,
    page: int = 1,
    per_page: int = 50
) -> dict:
```

**Inputs**:
- `db_session`: SQLAlchemy async session
- `filters`: Search criteria
  - `event_types`: List of event types
  - `document_id`: Filter by document
  - `user_id`: Filter by user
  - `date_from`: Start date
  - `date_to`: End date
- `page`: Page number
- `per_page`: Results per page

**Output**:
```python
{
    'result': {
        'events': [...],
        'total': 150,
        'page': 1,
        'pages': 3,
        'per_page': 50
    },
    'error': None
}
```

**Implementation Notes**:
- Build query dynamically from filters
- Order by timestamp descending
- Efficient pagination

**Tests Required**:
- `test_filters_by_type()` - Event type filter works
- `test_filters_by_date()` - Date range works
- `test_paginates_correctly()` - Pagination works

---

## Completion Checklist

After building each brick:
1. Verify line count: `wc -l bricks/audit/{name}.py`
2. Run tests: `pytest bricks/audit/test_{name}.py -v`
3. Mark complete: `python3 colony.py complete audit/{name}`
4. Commit: `git add bricks/audit/ && git commit -m "feat: add {name} brick"`

## Start Now
Begin with: **log_event.py**
