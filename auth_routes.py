"""
Authentication routes for Prescient System
Register, Login, Forgot Password endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, User, init_db
from auth import (
    UserRegister, 
    UserLogin, 
    ForgotPassword, 
    Token,
    get_password_hash, 
    verify_password,
    create_access_token,
    send_reset_password_email,
    generate_password_reset_token
)

# Initialize database tables
init_db()

# Create router
router = APIRouter(prefix="/auth", tags=["Authentication"])

# ==================== REGISTER ENDPOINT ====================
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register new user
    
    - **email**: Valid email address (must be unique)
    - **username**: Username (must be unique)
    - **password**: Plain password (will be hashed)
    """
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sudah terdaftar. Gunakan email lain atau login."
        )
    
    # Check if username already exists
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username sudah digunakan. Pilih username lain."
        )
    
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    
    # Create new user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "success": True,
        "message": f"Akun berhasil dibuat untuk {user_data.username}!",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "username": new_user.username
        }
    }

# ==================== LOGIN ENDPOINT ====================
@router.post("/token", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login and get access token
    
    - **username**: Your username
    - **password**: Your password
    
    Returns JWT access token for authenticated requests
    """
    
    # Find user by username
    user = db.query(User).filter(User.username == user_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Akun Anda tidak aktif. Hubungi administrator."
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ==================== FORGOT PASSWORD ENDPOINT ====================
@router.post("/forgot-password")
def forgot_password(request: ForgotPassword, db: Session = Depends(get_db)):
    """
    Request password reset email
    
    - **email**: Your registered email address
    
    Sends password reset link to email if account exists
    """
    
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    
    # For security: always return success even if email not found
    # This prevents email enumeration attacks
    if not user:
        return {
            "success": True,
            "message": "Jika email terdaftar, instruksi reset password telah dikirim."
        }
    
    # Generate reset token
    reset_token = generate_password_reset_token(user.email)
    
    # Send email
    email_sent = send_reset_password_email(user.email, reset_token)
    
    if email_sent:
        return {
            "success": True,
            "message": "Instruksi reset password telah dikirim ke email Anda. Periksa inbox atau folder spam.",
            "debug_token": reset_token  # REMOVE IN PRODUCTION!
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gagal mengirim email. Periksa konfigurasi SMTP."
        )

# ==================== HEALTH CHECK ====================
@router.get("/health")
def auth_health():
    """Check authentication service health"""
    return {
        "status": "healthy",
        "service": "Prescient Authentication",
        "endpoints": [
            "POST /auth/register",
            "POST /auth/token",
            "POST /auth/forgot-password"
        ]
    }
