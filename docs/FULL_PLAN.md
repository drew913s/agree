# Agree - Enterprise Agreement Signing Platform

## Queen Architecture Plan

**Project**: DocuSign Competitor MVP
**Methodology**: Brick Development (50-line max per brick)
**Status**: Ready for Implementation
**Execution**: Parallel Princess Teams

---

## Colony Manager Tool (NEW)

A comprehensive CLI dashboard that shows the FULL PROJECT PLAN, tracks all Claude session roles, and updates as work progresses.

### Core Purpose
- **Full Plan Visibility** - See the entire architecture at a glance
- **Role Tracking** - Know exactly what each Claude window should do
- **Live Updates** - Plan file updates as work completes
- **Human-Readable** - Understand the colony without reading code

### Features
1. **Full Plan View** - Complete architecture, all domains, all bricks
2. **Role Assignments** - Which Princess owns which domain
3. **Session Guide** - Ready-to-paste prompts for each Claude window
4. **Progress Tracker** - Real-time brick completion status
5. **Plan Editor** - Updates plan.json when bricks complete
6. **Brick Validator** - Checks 50-line limit, meta.json, tests

### CLI Commands
```bash
# Show FULL plan with all details
python colony.py plan

# Show status dashboard
python colony.py status

# Show specific domain details
python colony.py domain Q-14

# List all Princess roles with their responsibilities
python colony.py roles

# Generate prompt to paste into a new Claude window
python colony.py session Q-14

# Validate all bricks
python colony.py validate

# Watch for changes and auto-update plan
python colony.py watch

# Mark a brick as complete (updates plan.json)
python colony.py complete security/rate_limiter

# Add JSON flag to any command
python colony.py status --json
```

### Master Plan File: plan.json

The Colony Manager reads/writes a `plan.json` file that contains the COMPLETE project state:

```json
{
  "project": {
    "name": "Agree",
    "description": "Enterprise Agreement Signing Platform",
    "methodology": "Brick Development",
    "created": "2024-01-15",
    "queen": "This Claude session"
  },
  "waves": [
    {
      "id": 1,
      "name": "Foundation + Security",
      "status": "in_progress",
      "princesses": [
        {
          "id": "Q-14",
          "domain": "security",
          "description": "Encryption, validation, rate limiting",
          "status": "assigned",
          "assigned_to": "Claude Window 2",
          "bricks": [
            {
              "name": "rate_limiter",
              "file": "bricks/security/rate_limiter.py",
              "description": "Redis-based sliding window rate limiter",
              "status": "pending",
              "lines": null,
              "score": null,
              "dependencies": ["redis"]
            },
            {
              "name": "token_generator",
              "file": "bricks/security/token_generator.py",
              "description": "Cryptographically secure token generation",
              "status": "pending",
              "lines": null,
              "score": null,
              "dependencies": ["secrets", "hashlib"]
            }
          ]
        }
      ]
    }
  ],
  "tech_stack": {
    "backend": "FastAPI + Python 3.11",
    "frontend": "Vue 3 + TypeScript",
    "database": "PostgreSQL 15",
    "cache": "Redis",
    "storage": "MinIO (dev) / GCS (prod)",
    "email": "SendGrid",
    "ai": "Claude API + Whisper Lite"
  },
  "security": {
    "encryption": "AES-256-GCM",
    "passwords": "Argon2id",
    "tokens": "HMAC-SHA256",
    "audit": "Blockchain-style hash chain"
  }
}
```

### Human-Readable Plan View

When you run `python colony.py plan`, you see:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        AGREE - ENTERPRISE AGREEMENT SIGNING                  ║
║                              Full Project Plan                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Methodology: Brick Development (50-line max per file)                        ║
║ Total Bricks: 108 | Completed: 5 | Progress: 4.6%                           ║
╠══════════════════════════════════════════════════════════════════════════════╣

┌─ WAVE 1: Foundation + Security ──────────────────────────────────────────────┐
│                                                                              │
│  Q-14 SECURITY [████████░░░░░░░░░░░░] 25% - Claude Window 2                 │
│  ├── ✓ rate_limiter.py (48 lines, score: 92)                                │
│  ├── ✓ token_generator.py (45 lines, score: 95)                             │
│  ├── ○ encrypt_field.py                                                      │
│  ├── ○ decrypt_field.py                                                      │
│  ├── ○ hash_chain.py                                                         │
│  ├── ○ validate_pdf.py                                                       │
│  ├── ○ sanitize_input.py                                                     │
│  └── ○ ip_hasher.py                                                          │
│                                                                              │
│  Q-10 STORAGE [░░░░░░░░░░░░░░░░░░░░] 0% - Unassigned                        │
│  ├── ○ save_file.py                                                          │
│  ├── ○ get_file.py                                                           │
│  ├── ○ delete_file.py                                                        │
│  └── ... (5 more)                                                            │
│                                                                              │
│  Q-08 AUTH [░░░░░░░░░░░░░░░░░░░░] 0% - Unassigned                           │
│  Q-07 AUDIT [░░░░░░░░░░░░░░░░░░░░] 0% - Unassigned                          │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ WAVE 2: Core Features ──────────────────────────────────────────────────────┐
│  Q-01 DOCUMENTS - Waiting for Wave 1                                         │
│  Q-02 FIELDS - Waiting for Wave 1                                            │
│  Q-05 PARTIES - Waiting for Wave 1                                           │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ WAVE 3: Signing Flow ───────────────────────────────────────────────────────┐
│  Q-03 SIGNING - Waiting for Wave 2                                           │
│  Q-04 WORKFLOW - Waiting for Wave 2                                          │
│  Q-06 NOTIFICATIONS - Waiting for Wave 2                                     │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ WAVE 4: AI & Frontend ──────────────────────────────────────────────────────┐
│  Q-09 API - Waiting for Wave 3                                               │
│  Q-11 FRONTEND - Waiting for Wave 3                                          │
│  Q-12 TEMPLATES - Waiting for Wave 3                                         │
│  Q-13 AUTOMATIONS - Waiting for Wave 3                                       │
└──────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
TECH STACK: FastAPI | Vue 3 | PostgreSQL | Redis | GCS | SendGrid | Claude AI
SECURITY: AES-256-GCM | Argon2id | HMAC-SHA256 | Hash Chain Audit
═══════════════════════════════════════════════════════════════════════════════
```

### Session Prompt Generator

When you run `python colony.py session Q-14`, it generates a complete prompt to paste into a new Claude window:

```markdown
# Princess Q-14: Security Domain

You are Princess Q-14, responsible for building the Security domain bricks.

## Project Context
- **Project**: Agree - Enterprise Agreement Signing Platform
- **Your Domain**: Security (encryption, validation, rate limiting)
- **Working Directory**: /home/drew913s/agree
- **Brick Location**: bricks/security/

## Brick Rules
1. Maximum 50 lines of code (excluding comments/blanks)
2. Return format: {'result': X, 'error': str|None}
3. Create {name}.py + {name}.meta.json + test_{name}.py for each brick
4. No banned patterns (eval, exec, shell=True, etc.)

## Your Assigned Bricks (in order)

### 1. rate_limiter.py
**Purpose**: Redis-based sliding window rate limiter
**Inputs**: key (str), limit (int), window_seconds (int), redis_client
**Outputs**: {'result': {'allowed': bool, 'remaining': int}, 'error': None}
**Dependencies**: redis

### 2. token_generator.py
**Purpose**: Cryptographically secure token generation
**Inputs**: length (int), prefix (str optional)
**Outputs**: {'result': 'token_string', 'error': None}
**Dependencies**: secrets

### 3. encrypt_field.py
**Purpose**: AES-256-GCM field-level encryption
**Inputs**: plaintext (str), key (bytes)
**Outputs**: {'result': 'base64_ciphertext', 'error': None}
**Dependencies**: cryptography

[... continues for all 8 bricks ...]

## When Complete
After building each brick, run:
```
python colony.py complete security/{brick_name}
```

This updates the master plan and notifies the Queen.

## Start Now
Begin with: rate_limiter.py
```

### Output Example
```
╔══════════════════════════════════════════════════════════════╗
║                    AGREE COLONY STATUS                       ║
╠══════════════════════════════════════════════════════════════╣
║ Wave 1 - Foundation                                          ║
╠──────────────┬────────┬──────────┬───────────────────────────╣
║ Domain       │ Status │ Bricks   │ Progress                  ║
╠──────────────┼────────┼──────────┼───────────────────────────╣
║ Q-14 security│ 🔨     │ 2/8      │ ████████░░░░░░░░░░░░ 25%  ║
║ Q-10 storage │ 🔨     │ 3/8      │ ████████████░░░░░░░░ 38%  ║
║ Q-08 auth    │ ⏳     │ 0/8      │ ░░░░░░░░░░░░░░░░░░░░  0%  ║
║ Q-07 audit   │ ⏳     │ 0/8      │ ░░░░░░░░░░░░░░░░░░░░  0%  ║
╚══════════════╧════════╧══════════╧═══════════════════════════╝

Recent Activity:
  ✓ security/rate_limiter.py - VALID (48 lines, score: 92)
  ✓ security/token_generator.py - VALID (45 lines, score: 95)
  ✗ storage/save_file.py - INVALID (52 lines - exceeds limit!)
```

### Princess Prompt Generator
When you run `python colony.py assign Q-14 security`, it outputs:

```markdown
# Princess Q-14 Assignment: Security Domain

You are Princess Q-14, responsible for the Security domain.

## Your Bricks to Build:
1. rate_limiter.py - Redis-based rate limiting
2. token_generator.py - Secure random token generation
3. encrypt_field.py - AES-256-GCM field encryption
4. decrypt_field.py - Field decryption
5. hash_chain.py - Audit trail integrity hashing
6. validate_pdf.py - PDF security scanning
7. sanitize_input.py - XSS/injection prevention
8. ip_hasher.py - Privacy-preserving IP hashing

## Brick Rules:
- Maximum 50 lines of code
- Return format: {'result': X, 'error': str|None}
- Include docstring with inputs/outputs/errors
- Create matching .meta.json file
- Create test_{name}.py with tests

## Start with: rate_limiter.py
[Full brick specification follows...]
```

### File: colony.py (Location: /home/drew913s/agree/colony.py)

### Output Modes
- **Default**: Rich CLI with colors, boxes, progress bars
- **--json flag**: Machine-readable JSON for automation

```bash
# Human-readable
python colony.py status
# JSON output
python colony.py status --json
```

### JSON Schema Example
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "project": "agree",
  "waves": [
    {
      "id": 1,
      "name": "Foundation",
      "status": "in_progress",
      "domains": [
        {
          "id": "Q-14",
          "name": "security",
          "status": "in_progress",
          "bricks": {
            "total": 8,
            "completed": 2,
            "valid": 2,
            "invalid": 0
          },
          "progress_percent": 25,
          "bricks_detail": [
            {
              "name": "rate_limiter",
              "status": "valid",
              "lines": 48,
              "score": 92,
              "has_meta": true,
              "has_tests": true
            }
          ]
        }
      ]
    }
  ],
  "summary": {
    "total_bricks": 108,
    "completed": 5,
    "progress_percent": 4.6
  }
}
```

### Build Order (UPDATED)
1. **colony.py** - Build first to manage the process
2. **Wave 1 bricks** - Use colony.py to track progress
3. **Wave 2-4 bricks** - Continue with colony.py guidance

---

## Parallel Princess Assignments

### Wave 1 (Foundation + Security) - Start Immediately
| Princess | Domain | Priority Bricks |
|----------|--------|-----------------|
| Q-14 | Security | rate_limiter, token_generator, encrypt_field, hash_chain |
| Q-10 | Storage | save_file, get_file, local_storage (MinIO dev) |
| Q-08 | Auth | create_token, validate_token, password_hash (Argon2id) |
| Q-07 | Audit | log_event, event_types, timestamp, chain integrity |

### Wave 2 (Core Features) - After Wave 1
| Princess | Domain | Priority Bricks |
|----------|--------|-----------------|
| Q-01 | Documents | upload, validate_pdf, retrieve, page_count |
| Q-02 | Fields | create_field, list_fields, field_types |
| Q-05 | Parties | add_signer, list_signers, signer_status |

### Wave 3 (Signing Flow) - After Wave 2
| Princess | Domain | Priority Bricks |
|----------|--------|-----------------|
| Q-03 | Signing | capture_sig, apply_sig, flatten_pdf |
| Q-04 | Workflow | state_machine, transition, complete_check |
| Q-06 | Notifications | send_invite, email_template, render_email |

### Wave 4 (AI & Frontend) - After Wave 3
| Princess | Domain | Priority Components |
|----------|--------|---------------------|
| Q-09 | API | All route handlers |
| Q-11 | Frontend | Dashboard, PdfViewer, SignaturePad |
| Q-12 | Templates | create_template, fill_template |
| Q-13 | Automations | voice_to_text, parse_intent, execute_send |

---

## API Keys Required

| Service | Purpose | Get From |
|---------|---------|----------|
| Anthropic | Claude AI for conversation | console.anthropic.com |
| SendGrid | Email delivery | sendgrid.com |
| MinIO (dev) | Local storage | No key needed (local) |
| GCS (prod) | Production storage | console.cloud.google.com |

---

## Step 0: Project Scaffolding (Queen Task)

Before Princesses can work, create base structure:

```
agree/
├── bricks/
│   ├── __init__.py
│   ├── documents/
│   ├── fields/
│   ├── signing/
│   ├── workflow/
│   ├── parties/
│   ├── notifications/
│   ├── audit/
│   ├── auth/
│   ├── api/
│   ├── storage/
│   ├── templates/
│   └── automations/
├── models/
│   ├── __init__.py
│   └── enums.py
├── core/
│   ├── __init__.py
│   ├── config.py          # Environment config
│   └── database.py        # SQLAlchemy setup
├── frontend/              # Vue 3 app (vite create)
├── migrations/
├── tests/
├── main.py                # FastAPI entry point
├── requirements.txt
├── docker-compose.yml     # PostgreSQL + Redis + MinIO
├── .env.example
└── README.md
```

### Immediate Actions (Queen executes):
1. Create directory structure
2. Write `requirements.txt`
3. Write `docker-compose.yml` (PostgreSQL, Redis, MinIO)
4. Write `core/config.py` (env vars)
5. Write `core/database.py` (SQLAlchemy async)
6. Write `models/enums.py` (all status enums)
7. Initialize Vue 3 frontend with Vite
8. Create `.env.example` with required keys

---

## Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Frontend | Vue 3 + TypeScript + Vite | Easiest to maintain, excellent docs |
| UI Framework | PrimeVue | Enterprise components, accessible |
| Backend | Python 3.11 + FastAPI | Async, modern, type-safe |
| Database | PostgreSQL 15 | Enterprise-grade, automation-friendly |
| ORM | SQLAlchemy 2.0 + Alembic | Best Python ORM, easy migrations |
| Cache | Redis | Sessions, rate limiting |
| Storage | Google Cloud Storage | User requirement |
| Email | SendGrid | User requirement |
| PDF Processing | PyMuPDF (fitz) | Fast, reliable PDF manipulation |

---

## Princess Domains (10 Domains)

| ID | Domain | Princess Role | Brick Count |
|----|--------|---------------|-------------|
| Q-01 | `documents` | PDF upload, storage, retrieval | 8 bricks |
| Q-02 | `fields` | Field placement & management | 8 bricks |
| Q-03 | `signing` | Signature capture & application | 8 bricks |
| Q-04 | `workflow` | Document state machine | 8 bricks |
| Q-05 | `parties` | Signers & recipients | 8 bricks |
| Q-06 | `notifications` | Email via SendGrid | 8 bricks |
| Q-07 | `audit` | Immutable event logging | 8 bricks |
| Q-08 | `auth` | JWT tokens & secure links | 8 bricks |
| Q-09 | `api` | FastAPI routes | 8 bricks |
| Q-10 | `storage` | GCS abstraction | 8 bricks |
| Q-11 | `frontend` | Vue 3 components | 20+ components |
| Q-12 | `templates` | Pre-saved contract templates | 8 bricks |
| Q-13 | `automations` | AI conversation & voice | 10 bricks |
| Q-14 | `security` | Encryption, validation, rate limiting | 8 bricks |

**Total Backend Bricks**: ~108 bricks
**Total Frontend Components**: ~20 components

---

## Directory Structure

```
agree/
├── bricks/                    # Backend brick modules
│   ├── documents/
│   ├── fields/
│   ├── signing/
│   ├── workflow/
│   ├── parties/
│   ├── notifications/
│   ├── audit/
│   ├── auth/
│   ├── api/
│   ├── storage/
│   ├── templates/
│   ├── automations/
│   └── security/              # CRITICAL: encryption, validation
├── models/                    # SQLAlchemy models
│   ├── __init__.py
│   ├── document.py
│   ├── field.py
│   ├── signer.py
│   ├── signature.py
│   ├── audit_event.py
│   ├── user.py
│   └── enums.py
├── core/                      # Shared infrastructure
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   └── exceptions.py
├── migrations/                # Alembic migrations
├── templates/email/           # SendGrid templates
├── frontend/                  # Vue 3 application
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── stores/
│   │   ├── composables/
│   │   └── api/
│   ├── package.json
│   └── vite.config.ts
├── main.py                    # FastAPI entry
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## Core Data Models

### Document
```
id, title, owner_id, status, storage_key, page_count,
file_hash, created_at, updated_at, expires_at
```

### Field
```
id, document_id, signer_id, field_type, page, x, y,
width, height, required, value, signed_at
```

### Signer
```
id, document_id, email, name, role, signing_order,
status, token, signed_at, ip_address
```

### AuditEvent
```
id, document_id, signer_id, event_type, timestamp,
ip_address, metadata, event_hash (chain integrity)
```

---

## Frontend Architecture (Vue 3)

### Views (Pages)
| View | Route | Description |
|------|-------|-------------|
| Dashboard | `/` | Document list, stats, quick actions |
| DocumentCreate | `/documents/new` | Upload PDF, add title |
| DocumentEdit | `/documents/:id/edit` | Add fields, assign signers |
| DocumentView | `/documents/:id` | View status, audit trail |
| SigningView | `/sign/:token` | Public signing experience |
| Settings | `/settings` | User preferences, API keys |

### Core Components
| Component | Purpose |
|-----------|---------|
| `PdfViewer.vue` | Display PDF with overlays |
| `FieldPlacer.vue` | Drag-drop field placement |
| `SignaturePad.vue` | Draw/type signature capture |
| `SignerList.vue` | Manage document signers |
| `AuditTrail.vue` | Display event history |
| `DocumentCard.vue` | Document list item |
| `StatusBadge.vue` | Document/signer status |
| `EmailPreview.vue` | Preview invitation email |

### State Management (Pinia)
- `useDocumentStore` - Current document state
- `useUserStore` - Auth state, preferences
- `useSigningStore` - Active signing session

---

## AI Automation System (Q-12 & Q-13)

### Conversational Flow Example
```
User (voice): "Send the NDA contract to John Smith"

AI: "I found your NDA template. Who is the recipient?"
User: "John Smith at john@company.com"

AI: "What is John's company name for the NDA?"
User: "Acme Corporation"

AI: "What confidentiality period - 2 years or 5 years?"
User: "5 years"

AI: "Ready to send NDA to John Smith at john@company.com
     for Acme Corporation with 5-year confidentiality. Send now?"
User: "Yes, send it"

AI: "Done! NDA sent to John Smith. I'll notify you when he signs."
```

### Q-12: Templates Domain
```
bricks/templates/
  create_template.py      # Save document as template
  list_templates.py       # List user's templates
  get_template.py         # Retrieve template
  delete_template.py      # Remove template
  template_fields.py      # Define fillable variables
  parse_variables.py      # Extract {{variable}} placeholders
  fill_template.py        # Populate template with values
  clone_to_doc.py         # Create document from template
```

### Template Model
```
id, owner_id, name, description, storage_key,
variables: [{name, type, required, prompt_question}],
default_signers: [{role, signing_order}],
created_at, usage_count
```

### Q-13: Automations Domain
```
bricks/automations/
  parse_intent.py         # Understand user command (Claude API)
  extract_entities.py     # Extract names, emails, values
  match_template.py       # Find matching template by name/context
  build_questions.py      # Generate clarifying questions
  validate_answers.py     # Validate user responses
  execute_send.py         # Orchestrate document creation & send
  voice_to_text.py        # Whisper API transcription
  text_to_voice.py        # TTS for responses (optional)
  conversation_state.py   # Track multi-turn conversation
  automation_log.py       # Log automation executions
```

### AI Integration Stack
| Component | Technology | Purpose |
|-----------|------------|---------|
| LLM | Claude API (Anthropic) | Intent parsing, entity extraction |
| Voice Input | Whisper Lite (local) | Fast speech-to-text, runs locally |
| Voice Output | Browser Web Speech API | Native TTS, zero latency |
| State | Redis | Conversation session state |

### Whisper Lite Integration
- **Local deployment**: Runs on server, no API costs
- **Model**: `whisper-tiny` or `whisper-base` for speed
- **Library**: `faster-whisper` (CTranslate2 optimized)
- **Latency**: <500ms for typical commands
- **Languages**: English primary, multi-language support

### Automation API Endpoints
```
POST   /api/v1/chat/message          Send text message to AI
POST   /api/v1/chat/voice            Send audio for transcription + processing
GET    /api/v1/chat/session          Get current conversation state
DELETE /api/v1/chat/session          Reset conversation

GET    /api/v1/templates             List templates
POST   /api/v1/templates             Create template from document
GET    /api/v1/templates/:id         Get template details
DELETE /api/v1/templates/:id         Delete template
POST   /api/v1/templates/:id/send    AI-assisted send (with variables)
```

### Frontend: Chat Interface Component
```
ChatWidget.vue           # Floating chat bubble
ChatPanel.vue            # Full conversation panel
VoiceButton.vue          # Push-to-talk voice input
MessageBubble.vue        # Chat message display
QuickReply.vue           # Suggested response buttons
TemplateSelector.vue     # Quick template picker
```

---

## API Endpoints

### Documents
```
POST   /api/v1/documents              Upload PDF
GET    /api/v1/documents              List documents
GET    /api/v1/documents/:id          Get document
DELETE /api/v1/documents/:id          Delete document
POST   /api/v1/documents/:id/send     Send for signing
GET    /api/v1/documents/:id/pdf      Download PDF
```

### Fields
```
POST   /api/v1/documents/:id/fields   Create field
GET    /api/v1/documents/:id/fields   List fields
PUT    /api/v1/fields/:id             Update field
DELETE /api/v1/fields/:id             Delete field
```

### Signers
```
POST   /api/v1/documents/:id/signers  Add signer
GET    /api/v1/documents/:id/signers  List signers
DELETE /api/v1/signers/:id            Remove signer
POST   /api/v1/signers/:id/remind     Send reminder
```

### Signing (Public)
```
GET    /api/v1/sign/:token            Get signing session
GET    /api/v1/sign/:token/pdf        Get PDF for signing
POST   /api/v1/sign/:token/fields/:id Fill field
POST   /api/v1/sign/:token/complete   Complete signing
```

### Auth
```
POST   /api/v1/auth/register          Register
POST   /api/v1/auth/login             Login
POST   /api/v1/auth/refresh           Refresh token
GET    /api/v1/auth/me                Current user
```

---

## Implementation Phases

### Phase 1: Foundation
**Princess Assignments**: Q-10 (Storage), Q-08 (Auth), Q-07 (Audit)

| Task | Bricks |
|------|--------|
| Project scaffolding | Setup files, configs |
| Database models | All SQLAlchemy models |
| GCS integration | save_file, get_file, delete_file, presign_url |
| Auth system | create_token, validate_token, password_hash, signing_link |
| Audit logging | log_event, get_trail, timestamp, hash_event |

### Phase 2: Document Core
**Princess Assignments**: Q-01 (Documents), Q-02 (Fields)

| Task | Bricks |
|------|--------|
| PDF upload | upload, validate_pdf, page_count, metadata |
| PDF retrieval | retrieve, thumbnail, download |
| Field management | create_field, update_field, delete_field, list_fields |
| Field validation | validate_position, field_types, assign_field |

### Phase 3: Signing Flow
**Princess Assignments**: Q-03 (Signing), Q-04 (Workflow), Q-05 (Parties)

| Task | Bricks |
|------|--------|
| Signer management | add_signer, remove_signer, list_signers, signing_order |
| Signature capture | capture_sig, sig_image, typed_sig, drawn_sig |
| PDF signing | apply_sig, flatten_pdf, verify_sig |
| State machine | state_machine, transition, current_state, complete_check |

### Phase 4: Notifications
**Princess Assignment**: Q-06 (Notifications)

| Task | Bricks |
|------|--------|
| SendGrid integration | email_template, render_email, delivery_status |
| Email workflows | send_invite, send_reminder, send_complete |

### Phase 5: API Layer
**Princess Assignment**: Q-09 (API)

| Task | Bricks |
|------|--------|
| Route handlers | doc_routes, field_routes, sign_routes, party_routes |
| Middleware | error_handler, request_log, response_fmt |

### Phase 6: Frontend
**Princess Assignment**: Q-11 (Frontend)

| Task | Components |
|------|------------|
| Core layout | AppLayout, Navbar, Sidebar |
| Dashboard | Dashboard, DocumentCard, StatusBadge |
| Document editor | PdfViewer, FieldPlacer, SignerList |
| Signing experience | SigningView, SignaturePad, FieldInput |
| Settings | Settings, ApiKeyManager |

### Phase 7: Templates & AI Automation
**Princess Assignments**: Q-12 (Templates), Q-13 (Automations)

| Task | Bricks/Components |
|------|-------------------|
| Template system | create_template, parse_variables, fill_template, clone_to_doc |
| Whisper Lite setup | voice_to_text, audio preprocessing |
| Claude integration | parse_intent, extract_entities, build_questions |
| Conversation engine | conversation_state, validate_answers, execute_send |
| Chat UI | ChatWidget, ChatPanel, VoiceButton, MessageBubble |

### Voice Command Examples
```
"Send the NDA to john@acme.com"
"Create a new consulting agreement for Sarah"
"Remind Mike to sign the contract"
"What's the status of the Johnson deal?"
"Show me all pending signatures"
```

---

## Security Architecture (Enterprise Grade)

### 1. Authentication & Authorization

| Layer | Implementation | Details |
|-------|----------------|---------|
| User Auth | JWT + Refresh Tokens | 15min access / 7day refresh, httpOnly cookies |
| API Auth | API Keys + HMAC | Rate-limited, revocable, IP whitelist option |
| Signer Auth | One-time tokens | HMAC-SHA256, time-limited (7 days), single-use |
| Admin Auth | MFA required | TOTP (Google Auth) for admin actions |
| Session | Redis-backed | Secure session management, forced logout capability |

### 2. Encryption

| Data State | Method | Key Management |
|------------|--------|----------------|
| At Rest (DB) | AES-256-GCM | Field-level encryption for PII |
| At Rest (Files) | AES-256-GCM | Per-document encryption keys |
| In Transit | TLS 1.3 only | HSTS, perfect forward secrecy |
| Passwords | Argon2id | Memory-hard, GPU-resistant |
| API Keys | PBKDF2-SHA256 | Hashed storage, never logged |
| Signing Tokens | HMAC-SHA256 | Time-based, document-scoped |

### 3. Secure Signing Links

```python
# Token structure (tamper-proof)
token = base64url(
    version (1 byte) +
    document_id (16 bytes UUID) +
    signer_id (16 bytes UUID) +
    expiry_timestamp (8 bytes) +
    nonce (8 bytes random) +
    HMAC-SHA256(all_above, SERVER_SECRET)
)

# Verification
- Check HMAC integrity
- Verify expiry not passed
- Confirm signer exists and status is pending
- Check nonce not reused (Redis bloom filter)
- Log access with IP/user-agent
```

### 4. Audit Trail Integrity (Tamper-Proof)

```python
# Blockchain-style chaining
event = {
    "id": uuid4(),
    "document_id": doc_id,
    "event_type": "signer.signed",
    "timestamp": utc_now_iso(),
    "actor_id": signer_id,
    "ip_address": hashed_ip,  # Privacy-preserving
    "user_agent": truncated_ua,
    "metadata": {...},
    "previous_hash": prev_event_hash,
    "event_hash": SHA256(all_fields + prev_hash)
}

# Verification: Any tampering breaks the chain
# External anchor: Daily hash published to blockchain (optional)
```

### 5. Input Validation & Sanitization

| Input Type | Validation | Sanitization |
|------------|------------|--------------|
| Email | RFC 5322 regex + MX check | Lowercase, strip |
| PDF Files | Magic bytes + structure parse | Virus scan, flatten JS |
| Field Coords | Bounds check (0-100%) | Numeric coercion |
| Text Fields | Length limits, charset | HTML escape, XSS filter |
| File Uploads | Size limit (25MB), type whitelist | Strip metadata |
| API Params | Pydantic strict mode | Type coercion disabled |

### 6. OWASP Top 10 Mitigations

| Vulnerability | Mitigation |
|---------------|------------|
| A01 Broken Access | RBAC, resource ownership checks on every request |
| A02 Crypto Failures | AES-256, TLS 1.3, no MD5/SHA1, secure key storage |
| A03 Injection | Parameterized queries, ORM only, no raw SQL |
| A04 Insecure Design | Threat modeling, security review gates |
| A05 Misconfiguration | Secure defaults, env validation, no debug in prod |
| A06 Vulnerable Components | Dependabot, weekly updates, CVE scanning |
| A07 Auth Failures | MFA, rate limiting, account lockout |
| A08 Data Integrity | Signed packages, audit trail, checksums |
| A09 Logging Failures | Structured logging, SIEM integration, alert rules |
| A10 SSRF | URL validation, internal network blocking |

### 7. Rate Limiting & DDoS Protection

```python
# Multi-layer rate limiting
RATE_LIMITS = {
    "global": "1000/minute",           # Per IP
    "auth_login": "5/minute",           # Brute force prevention
    "auth_register": "3/hour",          # Spam prevention
    "document_upload": "10/hour",       # Resource protection
    "signing_complete": "1/token",      # One-time use
    "api_key": "100/minute",            # Per API key
}

# Implemented via:
# - Redis sliding window
# - Cloudflare/AWS WAF (production)
# - Fail2ban for repeated violations
```

### 8. Secrets Management

```yaml
# Never in code, always from environment
secrets:
  - JWT_SECRET_KEY          # 256-bit random
  - SIGNING_TOKEN_SECRET    # 256-bit random
  - DATABASE_ENCRYPTION_KEY # AES-256 key
  - SENDGRID_API_KEY        # External service
  - ANTHROPIC_API_KEY       # External service
  - GCS_SERVICE_ACCOUNT     # JSON key file

# Production: HashiCorp Vault or AWS Secrets Manager
# Development: .env file (git-ignored) + .env.example
```

### 9. PDF Security

```python
# PDF processing security
def secure_pdf_process(file_bytes):
    # 1. Validate magic bytes (PDF header)
    # 2. Scan for embedded JavaScript (remove)
    # 3. Scan for external links (flag)
    # 4. Check for encrypted content (reject)
    # 5. Virus scan (ClamAV integration)
    # 6. Strip metadata (author, software, GPS)
    # 7. Flatten form fields if present
    # 8. Generate thumbnail from rasterized page (no vectors)
```

### 10. Network Security

```
┌─────────────────────────────────────────────────────────────┐
│                    Cloudflare / AWS WAF                     │
│              DDoS protection, bot filtering                 │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTPS only
┌─────────────────────────▼───────────────────────────────────┐
│                    Load Balancer                            │
│              TLS termination, health checks                 │
└─────────────────────────┬───────────────────────────────────┘
                          │ Internal network
┌─────────────────────────▼───────────────────────────────────┐
│                    API Containers                           │
│   - No root access                                         │
│   - Read-only filesystem                                    │
│   - Network policies (no egress except allowed)            │
│   - Resource limits (CPU/memory)                            │
└─────────────────────────┬───────────────────────────────────┘
                          │ Private subnet only
┌──────────────┬──────────┴──────────┬───────────────────────┐
│  PostgreSQL  │       Redis         │    MinIO/GCS          │
│  (encrypted) │   (auth required)   │  (signed URLs only)   │
└──────────────┴─────────────────────┴───────────────────────┘
```

### 11. Compliance Considerations

| Standard | Requirements | Implementation |
|----------|--------------|----------------|
| SOC 2 Type II | Access controls, audit logs | RBAC + immutable audit trail |
| GDPR | Data portability, right to delete | Export API, soft delete with purge |
| HIPAA | PHI protection (if health docs) | Encryption, access logs, BAA |
| eIDAS | Electronic signature validity | Audit trail, timestamp authority |
| ESIGN Act | Electronic signature legality | Consent, intent, attribution |

### 12. Security Bricks (Q-14 Security Domain)

```
bricks/security/
  validate_pdf.py         # PDF security scanning
  sanitize_input.py       # XSS/injection prevention
  rate_limiter.py         # Redis-based limiting
  ip_hasher.py            # Privacy-preserving IP storage
  token_generator.py      # Secure random tokens
  encrypt_field.py        # Field-level encryption
  decrypt_field.py        # Field-level decryption
  hash_chain.py           # Audit trail integrity
```

### 13. Security Testing Requirements

| Test Type | Tool | Frequency |
|-----------|------|-----------|
| SAST | Bandit, Semgrep | Every commit |
| DAST | OWASP ZAP | Weekly |
| Dependency Scan | Safety, Snyk | Daily |
| Secret Detection | Gitleaks, TruffleHog | Every commit |
| Penetration Test | Manual / Bug bounty | Quarterly |
| Container Scan | Trivy | Every build |

### 14. Incident Response

```
1. Detection   → Logging alerts, anomaly detection
2. Containment → API key revocation, account suspension
3. Eradication → Patch deployment, secret rotation
4. Recovery    → Service restoration, user notification
5. Lessons     → Post-mortem, security improvement
```

### 15. Security Headers

```python
# FastAPI middleware
SECURITY_HEADERS = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Content-Security-Policy": "default-src 'self'; script-src 'self'",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(self)",
}

---

## Brick Standard Format

Every brick follows this pattern:

```python
# bricks/{domain}/{name}.py (max 50 lines)
"""Brief description."""

async def brick_name(param1: Type, param2: Type) -> dict:
    """
    Docstring with inputs, outputs, errors.
    """
    try:
        # Implementation
        return {"result": data, "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}
```

```json
// bricks/{domain}/{name}.meta.json
{
  "name": "brick_name",
  "domain": "domain_name",
  "version": "1.0.0",
  "description": "What it does",
  "inputs": {},
  "outputs": {},
  "dependencies": []
}
```

---

## First Implementation Steps

1. Create project structure and config files
2. Set up PostgreSQL models with Alembic
3. Implement Q-10 Storage bricks (GCS)
4. Implement Q-08 Auth bricks (JWT)
5. Implement Q-01 Document upload brick
6. Create Vue 3 scaffold with PrimeVue
7. Build basic Dashboard view

---

## Dependencies

### Backend (requirements.txt)
```
# Core API
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.0
alembic>=1.13.0
asyncpg>=0.29.0
pydantic>=2.5.0
python-multipart>=0.0.6

# Auth & Security
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4

# PDF Processing
pymupdf>=1.23.0

# Storage & Email
google-cloud-storage>=2.14.0
sendgrid>=6.11.0

# Cache
redis>=5.0.0

# HTTP Client
httpx>=0.26.0

# AI & Voice (Whisper Lite)
anthropic>=0.18.0           # Claude API
faster-whisper>=1.0.0       # Local Whisper, CTranslate2 optimized
soundfile>=0.12.0           # Audio file handling
numpy>=1.26.0               # Audio processing

# Security
argon2-cffi>=23.1.0         # Argon2id password hashing
cryptography>=42.0.0        # AES-256-GCM encryption
pyotp>=2.9.0                # TOTP for MFA
bleach>=6.1.0               # HTML sanitization

# Security Testing (dev)
bandit>=1.7.0               # SAST
safety>=2.3.0               # Dependency vulnerability scan
```

### Frontend (package.json)
```
vue: ^3.4.0
vue-router: ^4.2.0
pinia: ^2.1.0
primevue: ^3.47.0
@vueuse/core: ^10.7.0
axios: ^1.6.0
pdf.js: ^4.0.0
signature_pad: ^4.1.0
```
