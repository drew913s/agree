# API Keys Setup Guide

## Required API Keys for Agree

This document explains how to obtain and configure the API keys needed for the Agree platform.

---

## 1. Google Cloud Storage (GCS)

### What You Need
- **Service Account JSON Key File** - A JSON file containing credentials for a GCS service account

### Setup Steps

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com

2. **Create a Project** (if you don't have one)
   - Click "Select a project" → "New Project"
   - Name it something like `agree-production`

3. **Enable Cloud Storage API**
   - Go to: APIs & Services → Library
   - Search for "Cloud Storage"
   - Click "Cloud Storage API" → "Enable"

4. **Create a Storage Bucket**
   - Go to: Cloud Storage → Buckets → "Create"
   - Choose a globally unique name (e.g., `agree-documents-prod`)
   - Select region closest to your users
   - Choose "Standard" storage class
   - Set access control to "Uniform"
   - Click "Create"

5. **Create a Service Account**
   - Go to: IAM & Admin → Service Accounts
   - Click "Create Service Account"
   - Name: `agree-storage-access`
   - Click "Create and Continue"

6. **Grant Permissions**
   - Role: "Storage Object Admin" (for read/write access)
   - Click "Continue" → "Done"

7. **Generate Key File**
   - Click on the service account you just created
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key"
   - Select "JSON" format
   - Click "Create" - the file will download automatically

8. **Store the Key File**
   - Save as `gcs-credentials.json` in your project root
   - **NEVER commit this file to git!**
   - Add to `.gitignore`

### Environment Variables
```bash
# .env
GCS_BUCKET_NAME=agree-documents-prod
GCS_CREDENTIALS_PATH=./gcs-credentials.json

# OR use the JSON content directly (for Docker/cloud deployment)
GCS_CREDENTIALS_JSON='{"type": "service_account", ...}'
```

### Cost Estimate
- **Storage**: ~$0.02/GB/month (Standard class)
- **Operations**: ~$0.004 per 10,000 operations
- **Free Tier**: 5GB storage, 5,000 Class A ops, 50,000 Class B ops/month

---

## 2. SendGrid (Email)

### What You Need
- **API Key** - A single API key string for sending emails

### Setup Steps

1. **Create SendGrid Account**
   - Visit: https://sendgrid.com
   - Click "Start for Free"
   - Complete registration (email verification required)

2. **Verify Sender Identity**
   - Go to: Settings → Sender Authentication
   - Choose "Single Sender Verification" (easiest for MVP)
   - Or set up "Domain Authentication" (recommended for production)
   - Enter your email address and verify it

3. **Create API Key**
   - Go to: Settings → API Keys
   - Click "Create API Key"
   - Name: `agree-production`
   - Permissions: Choose "Restricted Access"
     - Mail Send: **Full Access**
     - (Leave others as "No Access" for security)
   - Click "Create & View"
   - **COPY THE KEY IMMEDIATELY** - it won't be shown again!

4. **Store the API Key**
   ```bash
   # .env
   SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxx
   SENDGRID_FROM_EMAIL=noreply@yourdomain.com
   SENDGRID_FROM_NAME=Agree Signing
   ```

### Email Templates (Optional)
- Go to: Email API → Dynamic Templates
- Create templates for:
  - Signing invitation
  - Reminder
  - Completion notification
- Note the Template IDs for use in the app

### Cost Estimate
- **Free Tier**: 100 emails/day forever
- **Essentials**: $19.95/month for 50,000 emails
- **Pro**: $89.95/month for 100,000 emails + advanced features

### Testing
- SendGrid provides a sandbox mode
- Use `SENDGRID_SANDBOX_MODE=true` in development

---

## 3. Anthropic (Claude API)

### What You Need
- **API Key** - For AI-powered conversation and voice command processing

### Setup Steps

1. **Access Anthropic Console**
   - Visit: https://console.anthropic.com
   - You mentioned you already have an account

2. **Get API Key**
   - Go to: Settings → API Keys
   - Click "Create Key"
   - Name: `agree-production`
   - Copy the key immediately

3. **Store the API Key**
   ```bash
   # .env
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
   ```

### Cost Estimate
- **Claude 3 Haiku**: $0.25/M input tokens, $1.25/M output tokens (fast, cheap)
- **Claude 3 Sonnet**: $3/M input tokens, $15/M output tokens (balanced)
- For voice commands, Haiku is recommended (fast responses)

---

## Complete .env.example

```bash
# ===========================================
# AGREE - Environment Configuration
# ===========================================

# Application
APP_NAME=Agree
APP_ENV=development
DEBUG=true
SECRET_KEY=your-256-bit-secret-key-here

# Database
DATABASE_URL=postgresql+asyncpg://agree:agree_password@localhost:5432/agree_db

# Redis (for sessions, rate limiting, caching)
REDIS_URL=redis://localhost:6379/0

# Google Cloud Storage
GCS_BUCKET_NAME=your-bucket-name
GCS_CREDENTIALS_PATH=./gcs-credentials.json
# OR for production:
# GCS_CREDENTIALS_JSON={"type": "service_account", ...}

# SendGrid (Email)
SENDGRID_API_KEY=SG.your-api-key-here
SENDGRID_FROM_EMAIL=noreply@yourdomain.com
SENDGRID_FROM_NAME=Agree Signing
SENDGRID_SANDBOX_MODE=true

# Anthropic (Claude AI)
ANTHROPIC_API_KEY=sk-ant-your-api-key-here

# Security
JWT_SECRET_KEY=your-jwt-secret-256-bits
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

SIGNING_TOKEN_SECRET=your-signing-token-secret
SIGNING_TOKEN_EXPIRE_DAYS=7

# Encryption (for at-rest encryption)
DATABASE_ENCRYPTION_KEY=your-32-byte-aes-key-base64

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_DEFAULT=100/minute

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# File Upload
MAX_UPLOAD_SIZE_MB=25
ALLOWED_EXTENSIONS=["pdf"]
```

---

## Security Checklist

- [ ] Never commit `.env` or `gcs-credentials.json` to git
- [ ] Add both to `.gitignore`
- [ ] Use different API keys for development and production
- [ ] Rotate keys periodically (every 90 days recommended)
- [ ] Use restricted permissions (principle of least privilege)
- [ ] Enable 2FA on all service accounts
- [ ] Monitor API usage for anomalies

---

## Quick Start

1. Copy `.env.example` to `.env`
2. Replace placeholder values with your actual keys
3. Run `docker-compose up -d` to start services
4. Run `alembic upgrade head` to create database tables
5. Run `uvicorn main:app --reload` to start the API

---

## Need Help?

- **GCS Issues**: https://cloud.google.com/storage/docs
- **SendGrid Issues**: https://docs.sendgrid.com
- **Anthropic Issues**: https://docs.anthropic.com
