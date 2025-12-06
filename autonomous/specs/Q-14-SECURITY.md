# Princess Q-14: Security Domain

## Overview
Build 8 security bricks for the Agree enterprise agreement signing platform.

## Brick Rules
- Maximum 50 lines of code per brick (excluding comments/blanks)
- Return format: `{'result': X, 'error': str|None}`
- Create `{name}.py` + `{name}.meta.json` + `test_{name}.py` for each brick
- Location: `bricks/security/`
- No banned patterns: `eval`, `exec`, `shell=True`, `subprocess` without validation

## Dependencies Available
- `redis` - Redis client for rate limiting
- `cryptography` - AES-256-GCM encryption
- `secrets` - Cryptographically secure random
- `hashlib` - SHA-256 hashing
- `bleach` - HTML sanitization
- `argon2-cffi` - Password hashing

---

## Bricks to Build (in order)

### 1. rate_limiter.py
**Purpose**: Redis-based sliding window rate limiter

**Function Signature**:
```python
async def rate_limit(
    key: str,
    limit: int,
    window_seconds: int,
    redis_client
) -> dict:
```

**Inputs**:
- `key`: Unique identifier (e.g., "user:123:api", "ip:1.2.3.4:login")
- `limit`: Maximum requests allowed in window
- `window_seconds`: Time window in seconds
- `redis_client`: Async Redis client instance

**Output**:
```python
{
    'result': {
        'allowed': True,      # Whether request is allowed
        'remaining': 5,       # Remaining requests in window
        'reset_at': 1704067200  # Unix timestamp when window resets
    },
    'error': None
}
```

**Implementation Notes**:
- Use sliding window with Redis ZADD + ZREMRANGEBYSCORE
- Key pattern: `ratelimit:{key}`
- TTL should match window_seconds
- Thread-safe for concurrent requests

**Tests Required**:
- `test_allows_under_limit()` - Requests under limit pass
- `test_blocks_over_limit()` - Requests over limit blocked
- `test_window_reset()` - Counter resets after window

---

### 2. token_generator.py
**Purpose**: Generate cryptographically secure random tokens

**Function Signature**:
```python
def generate_token(
    length: int = 32,
    prefix: str = ""
) -> dict:
```

**Inputs**:
- `length`: Token length in bytes (default 32)
- `prefix`: Optional prefix (e.g., "sign_", "api_")

**Output**:
```python
{
    'result': 'sign_a1b2c3d4e5f6...',  # URL-safe base64 token
    'error': None
}
```

**Implementation Notes**:
- Use `secrets.token_urlsafe(length)`
- Prepend prefix if provided
- Minimum length: 16 bytes

**Tests Required**:
- `test_generates_unique_tokens()` - No duplicates in 1000 tokens
- `test_correct_length()` - Output matches expected length
- `test_prefix_applied()` - Prefix correctly prepended

---

### 3. encrypt_field.py
**Purpose**: AES-256-GCM field-level encryption for PII

**Function Signature**:
```python
def encrypt_field(
    plaintext: str,
    key: bytes
) -> dict:
```

**Inputs**:
- `plaintext`: String to encrypt
- `key`: 32-byte AES key

**Output**:
```python
{
    'result': 'base64_encoded_ciphertext',  # nonce + ciphertext + tag
    'error': None
}
```

**Implementation Notes**:
- Use `cryptography.hazmat.primitives.ciphers.aead.AESGCM`
- Generate 12-byte random nonce
- Output format: `base64(nonce || ciphertext || tag)`
- Associated data: None (can be added later)

**Tests Required**:
- `test_encrypt_decrypt_roundtrip()` - Decrypt returns original
- `test_different_nonces()` - Same plaintext produces different ciphertext
- `test_invalid_key_length()` - Rejects non-32-byte keys

---

### 4. decrypt_field.py
**Purpose**: Decrypt AES-256-GCM encrypted fields

**Function Signature**:
```python
def decrypt_field(
    ciphertext: str,
    key: bytes
) -> dict:
```

**Inputs**:
- `ciphertext`: Base64-encoded encrypted data from encrypt_field
- `key`: 32-byte AES key (same as used for encryption)

**Output**:
```python
{
    'result': 'original plaintext string',
    'error': None
}
```

**Implementation Notes**:
- Decode base64, extract nonce (first 12 bytes)
- Use AESGCM.decrypt()
- Return error on authentication failure (tampered data)

**Tests Required**:
- `test_decrypts_valid_ciphertext()` - Successful decryption
- `test_fails_on_tampered_data()` - Returns error for modified ciphertext
- `test_fails_on_wrong_key()` - Returns error for incorrect key

---

### 5. hash_chain.py
**Purpose**: Create blockchain-style hash chain for audit trail integrity

**Function Signature**:
```python
def compute_event_hash(
    event_data: dict,
    previous_hash: str
) -> dict:
```

**Inputs**:
- `event_data`: Dict with event fields (id, type, timestamp, etc.)
- `previous_hash`: Hash of previous event in chain (or "genesis" for first)

**Output**:
```python
{
    'result': {
        'event_hash': 'sha256_hex_string',
        'chain_valid': True
    },
    'error': None
}
```

**Implementation Notes**:
- Serialize event_data deterministically (sorted keys, no whitespace)
- Hash = SHA256(previous_hash + serialized_event)
- Genesis hash: SHA256("genesis")

**Tests Required**:
- `test_deterministic_hash()` - Same input = same hash
- `test_chain_integrity()` - Tampering breaks chain
- `test_genesis_event()` - First event handled correctly

---

### 6. validate_pdf.py
**Purpose**: Security validation for uploaded PDF files

**Function Signature**:
```python
def validate_pdf_security(
    file_bytes: bytes,
    max_size_mb: int = 25
) -> dict:
```

**Inputs**:
- `file_bytes`: Raw PDF file content
- `max_size_mb`: Maximum allowed file size

**Output**:
```python
{
    'result': {
        'valid': True,
        'warnings': ['Contains external links'],
        'metadata_stripped': True
    },
    'error': None
}
```

**Implementation Notes**:
- Check PDF magic bytes: `%PDF-`
- Check file size against limit
- Detect embedded JavaScript (reject)
- Detect external links (warn)
- Use PyMuPDF for parsing

**Tests Required**:
- `test_accepts_valid_pdf()` - Clean PDF passes
- `test_rejects_non_pdf()` - Non-PDF files rejected
- `test_rejects_oversized()` - Large files rejected
- `test_detects_javascript()` - JS in PDF flagged

---

### 7. sanitize_input.py
**Purpose**: XSS and injection prevention for user input

**Function Signature**:
```python
def sanitize_input(
    text: str,
    max_length: int = 1000,
    allow_html: bool = False
) -> dict:
```

**Inputs**:
- `text`: User-provided text input
- `max_length`: Maximum allowed length
- `allow_html`: If True, allow safe HTML subset

**Output**:
```python
{
    'result': 'sanitized text string',
    'error': None
}
```

**Implementation Notes**:
- Strip leading/trailing whitespace
- Truncate to max_length
- If allow_html: use bleach with whitelist (a, b, i, em, strong)
- If not allow_html: escape all HTML entities
- Remove null bytes and control characters

**Tests Required**:
- `test_escapes_script_tags()` - XSS prevented
- `test_truncates_long_input()` - Length enforced
- `test_preserves_safe_html()` - Whitelisted tags kept when allowed
- `test_removes_null_bytes()` - Control chars stripped

---

### 8. ip_hasher.py
**Purpose**: Privacy-preserving IP address hashing for audit logs

**Function Signature**:
```python
def hash_ip_address(
    ip_address: str,
    salt: str
) -> dict:
```

**Inputs**:
- `ip_address`: IPv4 or IPv6 address string
- `salt`: Server-side secret salt

**Output**:
```python
{
    'result': 'hashed_ip_prefix',  # First 16 chars of hash
    'error': None
}
```

**Implementation Notes**:
- Validate IP format (IPv4 or IPv6)
- Hash = SHA256(salt + ip_address)
- Return first 16 hex chars (enough for uniqueness, privacy-preserving)
- Consistent hashing allows detecting same IP without storing raw

**Tests Required**:
- `test_consistent_hash()` - Same IP + salt = same hash
- `test_different_salt_different_hash()` - Salt affects output
- `test_validates_ip_format()` - Invalid IPs rejected
- `test_handles_ipv6()` - IPv6 addresses work

---

## Completion Checklist

After building each brick:
1. Verify line count: `wc -l bricks/security/{name}.py`
2. Run tests: `pytest bricks/security/test_{name}.py -v`
3. Mark complete: `python3 colony.py complete security/{name}`
4. Commit: `git add bricks/security/ && git commit -m "feat: add {name} brick"`

## Start Now
Begin with: **rate_limiter.py**
