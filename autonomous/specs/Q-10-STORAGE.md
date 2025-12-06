# Princess Q-10: Storage Domain

## Overview
Build 8 storage bricks for GCS/MinIO abstraction layer.

## Brick Rules
- Maximum 50 lines of code per brick
- Return format: `{'result': X, 'error': str|None}`
- Create `{name}.py` + `{name}.meta.json` + `test_{name}.py`
- Location: `bricks/storage/`

## Dependencies Available
- `google-cloud-storage` - GCS client
- `minio` - MinIO client (dev)
- `aiofiles` - Async file operations
- `core.config.get_settings()` - Environment config

## Storage Backend Config
```python
# From core/config.py
STORAGE_BACKEND = "minio"  # or "gcs"
MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "..."
MINIO_SECRET_KEY = "..."
GCS_BUCKET = "agree-documents"
```

---

## Bricks to Build (in order)

### 1. save_file.py
**Purpose**: Upload file to storage backend

**Function Signature**:
```python
async def save_file(
    file_bytes: bytes,
    storage_key: str,
    content_type: str = "application/octet-stream",
    metadata: dict = None
) -> dict:
```

**Inputs**:
- `file_bytes`: File content as bytes
- `storage_key`: Path in bucket (e.g., "documents/uuid/file.pdf")
- `content_type`: MIME type
- `metadata`: Optional key-value metadata

**Output**:
```python
{
    'result': {
        'storage_key': 'documents/abc123/file.pdf',
        'size_bytes': 102400,
        'etag': 'abc123...'
    },
    'error': None
}
```

**Implementation Notes**:
- Auto-detect backend from settings
- Create bucket if not exists (dev only)
- Set appropriate content-type header

**Tests Required**:
- `test_saves_and_retrieves()` - Roundtrip works
- `test_sets_content_type()` - MIME type preserved
- `test_stores_metadata()` - Custom metadata saved

---

### 2. get_file.py
**Purpose**: Retrieve file from storage

**Function Signature**:
```python
async def get_file(
    storage_key: str
) -> dict:
```

**Inputs**:
- `storage_key`: Path in bucket

**Output**:
```python
{
    'result': {
        'content': b'file bytes...',
        'content_type': 'application/pdf',
        'size_bytes': 102400,
        'metadata': {}
    },
    'error': None
}
```

**Implementation Notes**:
- Return None result with error if not found
- Include content-type from storage metadata

**Tests Required**:
- `test_retrieves_existing_file()` - Gets saved file
- `test_returns_error_not_found()` - Missing file handled
- `test_preserves_content_type()` - MIME type returned

---

### 3. delete_file.py
**Purpose**: Delete file from storage

**Function Signature**:
```python
async def delete_file(
    storage_key: str
) -> dict:
```

**Inputs**:
- `storage_key`: Path in bucket

**Output**:
```python
{
    'result': {'deleted': True},
    'error': None
}
```

**Implementation Notes**:
- Idempotent: no error if file doesn't exist
- Log deletion for audit purposes

**Tests Required**:
- `test_deletes_existing_file()` - File removed
- `test_idempotent_delete()` - No error on missing file

---

### 4. presign_url.py
**Purpose**: Generate presigned download URL

**Function Signature**:
```python
async def presign_url(
    storage_key: str,
    expires_seconds: int = 3600,
    download_filename: str = None
) -> dict:
```

**Inputs**:
- `storage_key`: Path in bucket
- `expires_seconds`: URL validity period
- `download_filename`: Optional Content-Disposition filename

**Output**:
```python
{
    'result': {
        'url': 'https://storage.../file?signature=...',
        'expires_at': 1704070800
    },
    'error': None
}
```

**Implementation Notes**:
- Use GCS signed URLs or MinIO presigned URLs
- Set Content-Disposition if download_filename provided
- Maximum expiry: 7 days

**Tests Required**:
- `test_generates_valid_url()` - URL is accessible
- `test_url_expires()` - Expired URL rejected
- `test_sets_download_filename()` - Content-Disposition works

---

### 5. list_files.py
**Purpose**: List files in a bucket prefix

**Function Signature**:
```python
async def list_files(
    prefix: str = "",
    max_results: int = 100
) -> dict:
```

**Inputs**:
- `prefix`: Filter by path prefix (e.g., "documents/user123/")
- `max_results`: Maximum files to return

**Output**:
```python
{
    'result': {
        'files': [
            {'key': 'documents/a.pdf', 'size': 1024, 'modified': '2024-01-15T...'},
            ...
        ],
        'truncated': False
    },
    'error': None
}
```

**Implementation Notes**:
- Sort by modified date descending
- Include pagination token if truncated

**Tests Required**:
- `test_lists_files_in_prefix()` - Filters correctly
- `test_respects_max_results()` - Limit enforced
- `test_empty_prefix_lists_all()` - Root listing works

---

### 6. file_exists.py
**Purpose**: Check if file exists in storage

**Function Signature**:
```python
async def file_exists(
    storage_key: str
) -> dict:
```

**Inputs**:
- `storage_key`: Path in bucket

**Output**:
```python
{
    'result': {'exists': True},
    'error': None
}
```

**Implementation Notes**:
- Use HEAD request (don't download content)
- Fast check for existence

**Tests Required**:
- `test_returns_true_for_existing()` - Existing file detected
- `test_returns_false_for_missing()` - Missing file detected

---

### 7. get_metadata.py
**Purpose**: Get file metadata without downloading content

**Function Signature**:
```python
async def get_metadata(
    storage_key: str
) -> dict:
```

**Inputs**:
- `storage_key`: Path in bucket

**Output**:
```python
{
    'result': {
        'size_bytes': 102400,
        'content_type': 'application/pdf',
        'etag': 'abc123',
        'modified': '2024-01-15T10:30:00Z',
        'custom_metadata': {}
    },
    'error': None
}
```

**Implementation Notes**:
- Use HEAD request
- Return error if not found

**Tests Required**:
- `test_returns_metadata()` - All fields present
- `test_returns_custom_metadata()` - User metadata included

---

### 8. copy_file.py
**Purpose**: Copy file within storage

**Function Signature**:
```python
async def copy_file(
    source_key: str,
    dest_key: str
) -> dict:
```

**Inputs**:
- `source_key`: Source path in bucket
- `dest_key`: Destination path in bucket

**Output**:
```python
{
    'result': {
        'source': 'documents/original.pdf',
        'destination': 'documents/copy.pdf',
        'size_bytes': 102400
    },
    'error': None
}
```

**Implementation Notes**:
- Server-side copy (no download/upload)
- Preserve metadata
- Error if source doesn't exist

**Tests Required**:
- `test_copies_file()` - Both files exist after copy
- `test_preserves_metadata()` - Metadata copied
- `test_error_missing_source()` - Source not found handled

---

## Completion Checklist

After building each brick:
1. Verify line count: `wc -l bricks/storage/{name}.py`
2. Run tests: `pytest bricks/storage/test_{name}.py -v`
3. Mark complete: `python3 colony.py complete storage/{name}`
4. Commit: `git add bricks/storage/ && git commit -m "feat: add {name} brick"`

## Start Now
Begin with: **save_file.py**
