# Princess Q-08: Auth Domain

## Overview
Build 8 authentication bricks for JWT tokens and secure signing links.

## Brick Rules
- Maximum 50 lines of code per brick
- Return format: `{'result': X, 'error': str|None}`
- Create `{name}.py` + `{name}.meta.json` + `test_{name}.py`
- Location: `bricks/auth/`

## Dependencies Available
- `python-jose[cryptography]` - JWT handling
- `argon2-cffi` - Argon2id password hashing
- `secrets` - Secure random generation
- `core.config.get_settings()` - JWT secrets, expiry config

## Auth Config
```python
# From core/config.py
JWT_SECRET_KEY = "..."          # 256-bit secret
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
SIGNING_TOKEN_SECRET = "..."    # For signer links
```

---

## Bricks to Build (in order)

### 1. create_token.py
**Purpose**: Generate JWT access token

**Function Signature**:
```python
def create_access_token(
    user_id: str,
    email: str,
    expires_minutes: int = 15
) -> dict:
```

**Inputs**:
- `user_id`: User UUID string
- `email`: User email
- `expires_minutes`: Token validity (default 15)

**Output**:
```python
{
    'result': {
        'access_token': 'eyJ...',
        'token_type': 'bearer',
        'expires_at': 1704067200
    },
    'error': None
}
```

**Implementation Notes**:
- Claims: sub (user_id), email, exp, iat, jti (unique ID)
- Use HS256 algorithm
- Include issued_at for rotation tracking

**Tests Required**:
- `test_creates_valid_token()` - Token is decodable
- `test_includes_claims()` - All claims present
- `test_respects_expiry()` - Expiry time correct

---

### 2. validate_token.py
**Purpose**: Validate and decode JWT token

**Function Signature**:
```python
def validate_access_token(
    token: str
) -> dict:
```

**Inputs**:
- `token`: JWT string (without "Bearer " prefix)

**Output**:
```python
{
    'result': {
        'user_id': 'uuid-string',
        'email': 'user@example.com',
        'exp': 1704067200,
        'valid': True
    },
    'error': None
}
```

**Implementation Notes**:
- Verify signature
- Check expiration
- Return error with code for expired/invalid tokens

**Tests Required**:
- `test_validates_good_token()` - Valid token passes
- `test_rejects_expired_token()` - Expired token fails
- `test_rejects_tampered_token()` - Modified token fails
- `test_rejects_wrong_secret()` - Wrong key fails

---

### 3. refresh_token.py
**Purpose**: Generate long-lived refresh token

**Function Signature**:
```python
def create_refresh_token(
    user_id: str,
    expires_days: int = 7
) -> dict:
```

**Inputs**:
- `user_id`: User UUID
- `expires_days`: Token validity

**Output**:
```python
{
    'result': {
        'refresh_token': 'eyJ...',
        'expires_at': 1704672000
    },
    'error': None
}
```

**Implementation Notes**:
- Separate secret or different claim structure
- Include token family ID for rotation detection
- Longer expiry than access token

**Tests Required**:
- `test_creates_refresh_token()` - Token created
- `test_longer_expiry()` - Expiry is days not minutes

---

### 4. password_hash.py
**Purpose**: Hash passwords with Argon2id

**Function Signature**:
```python
def hash_password(
    password: str
) -> dict:
```

**Inputs**:
- `password`: Plain text password

**Output**:
```python
{
    'result': '$argon2id$v=19$m=65536,t=3,p=4$...',
    'error': None
}
```

**Implementation Notes**:
- Use argon2-cffi with Argon2id variant
- Memory: 64MB, Time: 3 iterations, Parallelism: 4
- Salt is auto-generated and embedded in hash

**Tests Required**:
- `test_creates_hash()` - Hash is created
- `test_different_hashes_same_password()` - Random salt works
- `test_hash_format()` - Argon2id format correct

---

### 5. verify_password.py
**Purpose**: Verify password against Argon2id hash

**Function Signature**:
```python
def verify_password(
    password: str,
    password_hash: str
) -> dict:
```

**Inputs**:
- `password`: Plain text password to check
- `password_hash`: Stored Argon2id hash

**Output**:
```python
{
    'result': {'verified': True},
    'error': None
}
```

**Implementation Notes**:
- Use constant-time comparison
- Handle invalid hash format gracefully

**Tests Required**:
- `test_verifies_correct_password()` - Match returns True
- `test_rejects_wrong_password()` - Mismatch returns False
- `test_handles_invalid_hash()` - Bad format returns error

---

### 6. signing_link.py
**Purpose**: Generate secure one-time signing URL

**Function Signature**:
```python
def create_signing_link(
    document_id: str,
    signer_id: str,
    expires_days: int = 7
) -> dict:
```

**Inputs**:
- `document_id`: Document UUID
- `signer_id`: Signer UUID
- `expires_days`: Link validity

**Output**:
```python
{
    'result': {
        'token': 'sign_abc123xyz...',
        'url': '/sign/sign_abc123xyz...',
        'expires_at': 1704672000
    },
    'error': None
}
```

**Implementation Notes**:
- Token = HMAC-SHA256(document_id + signer_id + expiry + nonce)
- Include version byte for future changes
- URL-safe base64 encoding

**Tests Required**:
- `test_creates_signing_link()` - Link generated
- `test_unique_tokens()` - Each call produces different token
- `test_includes_expiry()` - Expiry embedded correctly

---

### 7. validate_signing_link.py
**Purpose**: Validate signing link token

**Function Signature**:
```python
def validate_signing_token(
    token: str
) -> dict:
```

**Inputs**:
- `token`: Signing token from URL

**Output**:
```python
{
    'result': {
        'valid': True,
        'document_id': 'uuid',
        'signer_id': 'uuid',
        'expires_at': 1704672000
    },
    'error': None
}
```

**Implementation Notes**:
- Verify HMAC signature
- Check expiration
- Extract embedded document_id and signer_id

**Tests Required**:
- `test_validates_good_token()` - Valid token passes
- `test_rejects_expired()` - Expired token fails
- `test_rejects_tampered()` - Modified token fails

---

### 8. api_key.py
**Purpose**: Generate and validate API keys

**Function Signature**:
```python
def generate_api_key(
    user_id: str,
    name: str = "default"
) -> dict:

def validate_api_key(
    api_key: str
) -> dict:
```

**Inputs**:
- `user_id`: Owner UUID
- `name`: Key name/label
- `api_key`: Key to validate

**Output (generate)**:
```python
{
    'result': {
        'api_key': 'ak_live_abc123...',  # Only shown once
        'api_key_hash': 'sha256...',      # Store this
        'prefix': 'ak_live_abc',          # For identification
        'name': 'default'
    },
    'error': None
}
```

**Output (validate)**:
```python
{
    'result': {
        'valid': True,
        'prefix': 'ak_live_abc'
    },
    'error': None
}
```

**Implementation Notes**:
- Generate 32-byte random key
- Prefix with "ak_live_" or "ak_test_"
- Store SHA256 hash, never plain key
- First 8 chars as prefix for identification

**Tests Required**:
- `test_generates_api_key()` - Key created with prefix
- `test_validates_correct_key()` - Validation works
- `test_hash_not_reversible()` - Can't recover key from hash

---

## Completion Checklist

After building each brick:
1. Verify line count: `wc -l bricks/auth/{name}.py`
2. Run tests: `pytest bricks/auth/test_{name}.py -v`
3. Mark complete: `python3 colony.py complete auth/{name}`
4. Commit: `git add bricks/auth/ && git commit -m "feat: add {name} brick"`

## Start Now
Begin with: **create_token.py**
