"""Security utilities for password hashing and verification"""

import base64
import hashlib

import bcrypt


def _prepare_password(password: str) -> bytes:
    """
    Prepare password for bcrypt hashing.

    bcrypt has a 72-byte limit. For longer passwords, we hash with SHA256
    and base64 encode to prevent NULL byte issues.

    Args:
        password: Plaintext password

    Returns:
        bytes: Password bytes ready for bcrypt (max 72 bytes)
    """
    password_bytes = password.encode('utf-8')

    # If password is longer than 72 bytes, hash it first
    if len(password_bytes) > 72:
        # SHA256 hash + base64 encode to avoid NULL bytes
        sha_hash = hashlib.sha256(password_bytes).digest()
        password_bytes = base64.b64encode(sha_hash)

    return password_bytes


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt with cost factor 12.

    Handles passwords longer than 72 bytes by hashing with SHA256 first.

    Args:
        password: Plaintext password

    Returns:
        str: Bcrypt hashed password

    Example:
        >>> hashed = hash_password("mypassword123")
        >>> len(hashed) == 60
        True
    """
    password_bytes = _prepare_password(password)
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a bcrypt hash.

    Args:
        plain_password: Plaintext password to verify
        hashed_password: Bcrypt hashed password from database

    Returns:
        bool: True if password matches, False otherwise

    Example:
        >>> hashed = hash_password("mypassword123")
        >>> verify_password("mypassword123", hashed)
        True
        >>> verify_password("wrongpassword", hashed)
        False
    """
    password_bytes = _prepare_password(plain_password)
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
