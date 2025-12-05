"""
Authentication utilities for Prescient System
JWT Token generation, password hashing, email sending
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import hashlib
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Security Configuration
SECRET_KEY = "prescient-secret-key-change-this-in-production-2024"  # CHANGE IN PRODUCTION!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Email Configuration (Gmail SMTP)
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "your-email@gmail.com"  # REPLACE WITH YOUR GMAIL
EMAIL_PASSWORD = "your-app-password"  # REPLACE WITH GMAIL APP PASSWORD

# Pydantic Models
class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ForgotPassword(BaseModel):
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Password utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password"""
    # Extract salt and hash from stored password
    # Format: salt$hash
    try:
        salt, stored_hash = hashed_password.split('$')
        # Hash the plain password with the same salt
        password_hash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), 
                                           salt.encode('utf-8'), 100000)
        calculated_hash = password_hash.hex()
        return calculated_hash == stored_hash
    except:
        return False

def get_password_hash(password: str) -> str:
    """Hash a plain password with salt"""
    # Generate random salt
    salt = secrets.token_hex(16)
    # Hash password with salt
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), 
                                       salt.encode('utf-8'), 100000)
    # Return salt$hash format
    return f"{salt}${password_hash.hex()}"

# JWT Token utilities
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    """Verify JWT token and extract username"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception

# Email utilities
def send_reset_password_email(email: str, reset_token: str):
    """
    Send password reset email to user
    
    SETUP GMAIL APP PASSWORD:
    1. Go to https://myaccount.google.com/security
    2. Enable 2-Step Verification
    3. Go to App passwords: https://myaccount.google.com/apppasswords
    4. Select "Mail" and "Other (Custom name)" -> Name it "Prescient"
    5. Copy the 16-character password
    6. Replace EMAIL_PASSWORD in this file
    """
    
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Prescient - Reset Password Request"
        message["From"] = EMAIL_USER
        message["To"] = email
        
        # Reset link (frontend route)
        reset_link = f"http://localhost:8000/reset-password?token={reset_token}"
        
        # HTML email body
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #050507; color: #e2e8f0; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: rgba(15, 16, 20, 0.9); border-radius: 16px; padding: 40px; border: 1px solid rgba(99, 102, 241, 0.3);">
              <h1 style="color: #6366f1; margin-bottom: 20px;">🔐 Prescient Password Reset</h1>
              <p style="font-size: 16px; line-height: 1.6;">
                Anda menerima email ini karena ada permintaan reset password untuk akun Prescient Anda.
              </p>
              <p style="font-size: 16px; line-height: 1.6;">
                Klik tombol di bawah untuk mereset password Anda:
              </p>
              <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}" 
                   style="background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); 
                          color: white; 
                          padding: 14px 32px; 
                          text-decoration: none; 
                          border-radius: 12px; 
                          font-weight: bold;
                          display: inline-block;
                          box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);">
                  RESET PASSWORD
                </a>
              </div>
              <p style="font-size: 14px; color: #9ca3af; line-height: 1.6;">
                Atau copy link berikut ke browser Anda:<br>
                <code style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 4px; display: block; margin-top: 8px; word-break: break-all;">
                  {reset_link}
                </code>
              </p>
              <hr style="border: 1px solid rgba(255,255,255,0.1); margin: 30px 0;">
              <p style="font-size: 12px; color: #6b7280;">
                ⚠️ Link ini akan kadaluarsa dalam 1 jam.<br>
                Jika Anda tidak meminta reset password, abaikan email ini.
              </p>
              <p style="font-size: 12px; color: #4b5563; margin-top: 20px;">
                Best regards,<br>
                <strong>Prescient Team</strong>
              </p>
            </div>
          </body>
        </html>
        """
        
        # Attach HTML body
        part = MIMEText(html, "html")
        message.attach(part)
        
        # Send email via Gmail SMTP
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(message)
        
        return True
    
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

def generate_password_reset_token(email: str) -> str:
    """Generate JWT token for password reset (expires in 1 hour)"""
    expires_delta = timedelta(hours=1)
    return create_access_token(
        data={"sub": email, "purpose": "password_reset"}, 
        expires_delta=expires_delta
    )
