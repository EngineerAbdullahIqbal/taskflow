# Password Security Standards

## Password Hashing (bcrypt)

**Constitution Requirement**: Cost factor ≥12

**Backend Implementation**:
```python
# backend/app/services/auth_service.py
import bcrypt

def hash_password(password: str) -> str:
    """Hash password with bcrypt (cost factor 12)."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed.encode('utf-8')
    )
```

**Why bcrypt?**:
- Adaptive: Cost factor can increase as hardware improves
- Salt built-in: Prevents rainbow table attacks
- Slow by design: Resists brute-force attacks

## Password Validation Rules

**Constitution Requirements**:
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special symbol

**Frontend Validation** (TypeScript):
```typescript
// frontend/lib/validation/password.ts
export const passwordSchema = z.string()
  .min(8, "Password must be at least 8 characters")
  .regex(/[A-Z]/, "Password must contain uppercase letter")
  .regex(/[a-z]/, "Password must contain lowercase letter")
  .regex(/[0-9]/, "Password must contain number")
  .regex(/[^A-Za-z0-9]/, "Password must contain special symbol")

// Usage with React Hook Form
const form = useForm({
  resolver: zodResolver(z.object({
    password: passwordSchema
  }))
})
```

**Backend Validation** (Pydantic):
```python
# backend/app/schemas/auth.py
import re
from pydantic import BaseModel, field_validator

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str

    @field_validator('password')
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain number")
        if not re.search(r"[^A-Za-z0-9]", v):
            raise ValueError("Password must contain special symbol")
        return v
```

## Common Password Vulnerabilities (Prevent)

### 1. Plaintext Storage ❌
**Never store passwords in plaintext.**
```python
# WRONG
user.password = password

# CORRECT
user.password_hash = hash_password(password)
```

### 2. Weak Hashing Algorithms ❌
**Never use MD5, SHA1, or SHA256 for passwords.**
```python
# WRONG
import hashlib
hashed = hashlib.sha256(password.encode()).hexdigest()

# CORRECT
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))
```

### 3. Password Leakage in Logs ❌
**Never log passwords or tokens.**
```python
# WRONG
logger.info(f"User signup: {email} with password {password}")

# CORRECT
logger.info(f"User signup: {email}")
```

### 4. Password in API Responses ❌
**Never return password_hash in API responses.**
```python
# WRONG
return {"id": user.id, "email": user.email, "password_hash": user.password_hash}

# CORRECT
return {"id": user.id, "email": user.email, "name": user.name}
```

### 5. Timing Attacks on Login ❌
**Use constant-time comparison for password verification.**
```python
# bcrypt.checkpw() is already constant-time
# Avoid custom comparison logic
```

## Rate Limiting for Brute-Force Prevention

**Constitution Requirement**: Max 5 failed login attempts per 15 minutes

**FastAPI Implementation**:
```python
# backend/app/middleware/rate_limit.py
from fastapi import HTTPException
from collections import defaultdict
from datetime import datetime, timedelta

# In-memory store (use Redis in production)
failed_attempts = defaultdict(list)

def check_rate_limit(email: str):
    """Check if user has exceeded login attempt limit."""
    now = datetime.utcnow()
    cutoff = now - timedelta(minutes=15)

    # Remove old attempts
    failed_attempts[email] = [
        timestamp for timestamp in failed_attempts[email]
        if timestamp > cutoff
    ]

    if len(failed_attempts[email]) >= 5:
        raise HTTPException(429, "Too many failed attempts. Try again in 15 minutes.")

def record_failed_attempt(email: str):
    """Record failed login attempt."""
    failed_attempts[email].append(datetime.utcnow())

# Usage in login route
@router.post("/api/auth/login")
async def login(request: LoginRequest):
    check_rate_limit(request.email)

    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password_hash):
        record_failed_attempt(request.email)
        raise HTTPException(401, "Invalid credentials")

    # Success: clear failed attempts
    failed_attempts.pop(request.email, None)
    return generate_tokens(user)
```

## Password Reset Security (Phase 3 Feature)

**Best Practices**:
1. Generate cryptographically random reset token (32+ bytes)
2. Hash token before storing in database
3. Set token expiration (15-30 minutes)
4. Invalidate token after use
5. Send reset link to verified email only
6. Require old password OR email verification
