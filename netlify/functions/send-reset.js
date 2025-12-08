const nodemailer = require('nodemailer');
const jwt = require('jsonwebtoken');
const fs = require('fs').promises;
const path = require('path');

/**
 * NETLIFY FUNCTION: Send Password Reset Email
 * 
 * Endpoint: /.netlify/functions/send-reset
 * Method: POST
 * Body: { email: "user@example.com" }
 * 
 * Environment Variables Required:
 * - EMAIL_USER: Gmail address (e.g., yourapp@gmail.com)
 * - EMAIL_PASS: Gmail App Password (NOT regular password)
 * - JWT_SECRET: Secret key for signing reset tokens
 * - SITE_URL: Your site URL (e.g., https://your-app.netlify.app)
 */

exports.handler = async (event, context) => {
  // Set CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle preflight OPTIONS request
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed. Use POST.' })
    };
  }

  try {
    // Parse request body
    const { email } = JSON.parse(event.body);

    // Validation
    if (!email || !email.includes('@')) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ 
          success: false,
          error: 'Email tidak valid!' 
        })
      };
    }

    // === STEP 1: CHECK IF USER EXISTS ===
    // In production, you would check a database
    // For this demo, we'll check the users.json file
    
    let userExists = false;
    let userName = '';
    
    try {
      // Try to read users from localStorage simulation file
      // In production, use a proper database
      const usersData = await fs.readFile(
        path.join(__dirname, '../../data/users.json'), 
        'utf-8'
      );
      const users = JSON.parse(usersData);
      
      const user = users.find(u => u.email === email);
      if (user) {
        userExists = true;
        userName = user.username;
      }
    } catch (err) {
      console.log('Users file not found, checking demo accounts...');
      
      // Check demo account
      if (email === 'lab.fisikaterapan@untirta.ac.id') {
        userExists = true;
        userName = 'eiz';
      }
    }

    if (!userExists) {
      // For security: Don't reveal if email exists or not
      // Always return success message
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          message: 'Jika email terdaftar, instruksi reset password telah dikirim.'
        })
      };
    }

    // === STEP 2: GENERATE RESET TOKEN ===
    const JWT_SECRET = process.env.JWT_SECRET || 'prescient-default-secret-change-in-production';
    
    // Token expires in 1 hour
    const resetToken = jwt.sign(
      { 
        email: email,
        username: userName,
        type: 'password-reset'
      },
      JWT_SECRET,
      { expiresIn: '1h' }
    );

    // === STEP 3: CREATE RESET LINK ===
    const SITE_URL = process.env.SITE_URL || 'http://localhost:8888';
    const resetLink = `${SITE_URL}/reset-password.html?token=${resetToken}`;

    // === STEP 4: CONFIGURE EMAIL TRANSPORTER ===
    const EMAIL_USER = process.env.EMAIL_USER;
    const EMAIL_PASS = process.env.EMAIL_PASS;

    if (!EMAIL_USER || !EMAIL_PASS) {
      console.error('⚠️ EMAIL_USER or EMAIL_PASS not configured!');
      
      // In development, log the reset link instead
      console.log('🔗 Password Reset Link:', resetLink);
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          message: 'Email konfigurasi belum diatur. Reset link: ' + resetLink,
          resetLink: resetLink, // Remove this in production!
          devMode: true
        })
      };
    }

    // Create Nodemailer transporter for Gmail
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: EMAIL_USER,
        pass: EMAIL_PASS // Use Gmail App Password, not regular password
      }
    });

    // === STEP 5: COMPOSE EMAIL ===
    const mailOptions = {
      from: `"Prescient Lead Scoring" <${EMAIL_USER}>`,
      to: email,
      subject: '🔐 Reset Password - Prescient Lead Scoring',
      html: `
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            body {
              font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
              background-color: #0f172a;
              color: #e2e8f0;
              margin: 0;
              padding: 20px;
            }
            .container {
              max-width: 600px;
              margin: 0 auto;
              background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
              border-radius: 16px;
              overflow: hidden;
              border: 1px solid rgba(99, 102, 241, 0.2);
            }
            .header {
              background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
              padding: 30px;
              text-align: center;
            }
            .header h1 {
              margin: 0;
              color: white;
              font-size: 24px;
            }
            .content {
              padding: 40px 30px;
            }
            .greeting {
              font-size: 18px;
              margin-bottom: 20px;
              color: #cbd5e1;
            }
            .message {
              font-size: 14px;
              line-height: 1.6;
              color: #94a3b8;
              margin-bottom: 30px;
            }
            .button {
              display: inline-block;
              padding: 14px 32px;
              background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
              color: white !important;
              text-decoration: none;
              border-radius: 8px;
              font-weight: bold;
              font-size: 16px;
              margin: 20px 0;
            }
            .button:hover {
              opacity: 0.9;
            }
            .warning {
              background: rgba(239, 68, 68, 0.1);
              border-left: 4px solid #ef4444;
              padding: 15px;
              margin: 20px 0;
              border-radius: 4px;
              font-size: 13px;
              color: #fca5a5;
            }
            .footer {
              text-align: center;
              padding: 20px;
              font-size: 12px;
              color: #64748b;
              border-top: 1px solid rgba(255,255,255,0.1);
            }
            .link-box {
              background: rgba(255,255,255,0.05);
              padding: 15px;
              border-radius: 8px;
              margin: 20px 0;
              word-break: break-all;
              font-size: 12px;
              color: #94a3b8;
            }
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <h1>🔐 Reset Password</h1>
            </div>
            <div class="content">
              <div class="greeting">
                Halo, <strong>${userName}</strong>!
              </div>
              <div class="message">
                Kami menerima permintaan untuk mereset password akun Anda di <strong>Prescient Lead Scoring</strong>.
              </div>
              <div class="message">
                Klik tombol di bawah ini untuk membuat password baru:
              </div>
              <center>
                <a href="${resetLink}" class="button">Reset Password Sekarang</a>
              </center>
              <div class="message" style="margin-top: 30px;">
                Atau copy link berikut ke browser Anda:
              </div>
              <div class="link-box">
                ${resetLink}
              </div>
              <div class="warning">
                ⚠️ <strong>Penting:</strong> Link ini hanya berlaku selama <strong>1 jam</strong> dan hanya bisa digunakan sekali. Jika Anda tidak meminta reset password, abaikan email ini.
              </div>
            </div>
            <div class="footer">
              <p>Email ini dikirim secara otomatis oleh sistem Prescient Lead Scoring.</p>
              <p>© 2025 Lab Fisika Terapan - Untirta</p>
            </div>
          </div>
        </body>
        </html>
      `,
      text: `
        Reset Password - Prescient Lead Scoring
        
        Halo, ${userName}!
        
        Kami menerima permintaan untuk mereset password akun Anda.
        
        Klik link berikut untuk membuat password baru:
        ${resetLink}
        
        Link ini hanya berlaku selama 1 jam.
        
        Jika Anda tidak meminta reset password, abaikan email ini.
        
        Salam,
        Tim Prescient Lead Scoring
      `
    };

    // === STEP 6: SEND EMAIL ===
    await transporter.sendMail(mailOptions);

    console.log('✅ Reset email sent to:', email);

    // === STEP 7: RETURN SUCCESS RESPONSE ===
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        message: 'Email berisi instruksi reset password telah dikirim. Periksa inbox Anda.',
        // In production, never send the token back!
        // devNote: 'Check email for reset link'
      })
    };

  } catch (error) {
    console.error('❌ Error in send-reset function:', error);

    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: 'Terjadi kesalahan saat mengirim email. Silakan coba lagi.',
        details: process.env.NODE_ENV === 'development' ? error.message : undefined
      })
    };
  }
};
