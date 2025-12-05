# ============================================================
# PRESCIENT AUTHENTICATION - QUICK INSTALL SCRIPT
# ============================================================
# Run this script to install authentication dependencies
# Usage: ./install_auth.ps1

Write-Output ""
Write-Output "╔══════════════════════════════════════════════════════════╗"
Write-Output "║   PRESCIENT - AUTHENTICATION SETUP INSTALLER             ║"
Write-Output "╚══════════════════════════════════════════════════════════╝"
Write-Output ""

# Check if venv exists
$venvPath = "C:/Users/mriva/OneDrive/Dokumen/New folder/.venv/Scripts/python.exe"
if (-not (Test-Path $venvPath)) {
    Write-Output "❌ Virtual environment not found at: $venvPath"
    Write-Output "   Please activate your venv first."
    exit 1
}

Write-Output "✅ Virtual environment found"
Write-Output ""

# Install dependencies
Write-Output "📦 Installing authentication dependencies..."
Write-Output ""

& $venvPath -m pip install --upgrade pip

$packages = @(
    "sqlalchemy>=2.0.23",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "python-multipart>=0.0.6",
    "pydantic[email]>=2.4.0"
)

foreach ($package in $packages) {
    Write-Output "   Installing: $package"
    & $venvPath -m pip install $package
}

Write-Output ""
Write-Output "═══════════════════════════════════════════════════════════"
Write-Output "✅ INSTALLATION COMPLETE!"
Write-Output "═══════════════════════════════════════════════════════════"
Write-Output ""
Write-Output "📋 NEXT STEPS:"
Write-Output ""
Write-Output "1. Configure Gmail SMTP in auth.py:"
Write-Output "   - Line 26: EMAIL_USER = 'your-email@gmail.com'"
Write-Output "   - Line 27: EMAIL_PASSWORD = 'your-app-password'"
Write-Output ""
Write-Output "2. Get Gmail App Password:"
Write-Output "   https://myaccount.google.com/apppasswords"
Write-Output ""
Write-Output "3. Start server:"
Write-Output "   python main.py"
Write-Output ""
Write-Output "4. Test endpoints:"
Write-Output "   http://localhost:8000/docs"
Write-Output ""
Write-Output "📚 Full guide: AUTH_SETUP_GUIDE.md"
Write-Output ""
