# Security Checklist Reference

OWASP-based security guidelines for the fullstack orchestrator.

## Authentication & Authorization

### Password Security
- [ ] Use bcrypt with cost factor ≥12
- [ ] Enforce minimum password length (8+)
- [ ] Implement password complexity rules
- [ ] Never log passwords or tokens

### JWT Security
- [ ] Use RS256 or HS256 with strong secret
- [ ] Set appropriate expiration (15-30 min)
- [ ] Implement refresh token rotation
- [ ] Store tokens securely (httpOnly cookies preferred)

### Session Management
- [ ] Invalidate sessions on logout
- [ ] Implement session timeout
- [ ] Regenerate session ID after login

## Input Validation (OWASP A03:2021)

### SQL Injection Prevention
```python
# BAD - Never do this
query = f"SELECT * FROM users WHERE email = '{email}'"

# GOOD - Use parameterized queries
result = await db.execute(select(User).where(User.email == email))
```

### XSS Prevention
```typescript
// BAD - Never do this
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// GOOD - React escapes by default
<div>{userInput}</div>

// If HTML needed, sanitize first
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />
```

### Request Validation
```python
# Always validate with Pydantic
from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=128)
```

## API Security

### Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/login")
@limiter.limit("5/minute")
async def login(request: Request):
    pass
```

### CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Not "*" in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### Security Headers
```python
from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response
```

## Dependency Security

### Python
```bash
# Check vulnerabilities
pip-audit

# Update dependencies
pip install --upgrade -r requirements.txt
```

### Node.js
```bash
# Check vulnerabilities
npm audit

# Fix vulnerabilities
npm audit fix
```

## Data Protection

### Sensitive Data
- [ ] Encrypt sensitive data at rest
- [ ] Use HTTPS for all communications
- [ ] Mask sensitive data in logs
- [ ] Implement data retention policies

### Environment Variables
```bash
# .env.example - Document required vars
DATABASE_URL=
SECRET_KEY=
JWT_SECRET=

# Never commit .env files
# .gitignore
.env
.env.local
.env.production
```

## Error Handling

### Safe Error Messages
```python
# BAD - Exposes internal details
raise HTTPException(status_code=500, detail=str(e))

# GOOD - Generic message, log details
logger.error(f"Database error: {e}")
raise HTTPException(status_code=500, detail="Internal server error")
```

## Audit Commands

```bash
# Backend security scan
bandit -r app/
safety check

# Frontend security scan
npm audit
npx eslint --ext .tsx,.ts src/ --rule 'security/*'

# OWASP ZAP scan (if available)
zap-cli quick-scan --self-contained http://localhost:8000
```
