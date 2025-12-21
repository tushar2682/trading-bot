# Backend/app/utils/encryption.py
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def get_cipher_suite():
    """
    Generates a Fernet cipher suite based on the App Secret.
    Ensures the key is 32 URL-safe base64-encoded bytes.
    """
    secret = os.environ.get('SECRET_KEY', 'default-unsafe-dev-key').encode()
    # Use a static salt for determinism (in prod, handle keys carefully via KMS)
    salt = b'trading-n8n-salt' 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret))
    return Fernet(key)

def encrypt_value(plaintext: str) -> str:
    """Encrypts a string."""
    if not plaintext:
        return None
    f = get_cipher_suite()
    return f.encrypt(plaintext.encode()).decode()

def decrypt_value(ciphertext: str) -> str:
    """Decrypts a string."""
    if not ciphertext:
        return None
    f = get_cipher_suite()
    return f.decrypt(ciphertext.encode()).decode()