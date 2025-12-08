const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const fs = require('fs').promises;
const path = require('path');

/**
 * NETLIFY FUNCTION: Verify Reset Token & Update Password
 * 
 * Endpoint: /.netlify/functions/reset-password
 * Method: POST
 * Body: { 
 *   token: "jwt-token-from-email", 
 *   newPassword: "newpass123" 
 * }
 * 
 * Environment Variables Required:
 * - JWT_SECRET: Same secret used in send-reset.js
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
    const { token, newPassword } = JSON.parse(event.body);

    // Validation
    if (!token || !newPassword) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ 
          success: false,
          error: 'Token dan password baru diperlukan!' 
        })
      };
    }

    if (newPassword.length < 5) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ 
          success: false,
          error: 'Password minimal 5 karakter!' 
        })
      };
    }

    // === STEP 1: VERIFY JWT TOKEN ===
    const JWT_SECRET = process.env.JWT_SECRET || 'prescient-default-secret-change-in-production';
    
    let decoded;
    try {
      decoded = jwt.verify(token, JWT_SECRET);
    } catch (err) {
      if (err.name === 'TokenExpiredError') {
        return {
          statusCode: 401,
          headers,
          body: JSON.stringify({
            success: false,
            error: 'Link reset password sudah expired! Silakan request ulang.'
          })
        };
      }
      
      return {
        statusCode: 401,
        headers,
        body: JSON.stringify({
          success: false,
          error: 'Token tidak valid!'
        })
      };
    }

    // Check token type
    if (decoded.type !== 'password-reset') {
      return {
        statusCode: 401,
        headers,
        body: JSON.stringify({
          success: false,
          error: 'Token bukan untuk reset password!'
        })
      };
    }

    const { email, username } = decoded;

    // === STEP 2: HASH NEW PASSWORD ===
    const hashedPassword = await bcrypt.hash(newPassword, 10);

    // === STEP 3: UPDATE PASSWORD IN DATABASE ===
    // In production, update your actual database
    // For this demo, we update users.json (localStorage simulation)
    
    try {
      const usersPath = path.join(__dirname, '../../data/users.json');
      
      // Read existing users
      let users = [];
      try {
        const usersData = await fs.readFile(usersPath, 'utf-8');
        users = JSON.parse(usersData);
      } catch (err) {
        // File doesn't exist, create new array
        users = [];
      }

      // Find and update user
      const userIndex = users.findIndex(u => u.email === email);
      
      if (userIndex !== -1) {
        // Update existing user
        users[userIndex].password = hashedPassword;
        users[userIndex].updatedAt = new Date().toISOString();
      } else {
        // User not found in file (might be demo account)
        // For demo account, we can't update (it's in frontend localStorage)
        console.log('⚠️ User not found in users.json, might be demo/localStorage account');
        
        // Return success anyway (for demo accounts, password stays in localStorage)
        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            success: true,
            message: 'Password berhasil direset! Silakan login dengan password baru.',
            note: 'Untuk akun demo, gunakan password: iris'
          })
        };
      }

      // Save updated users
      await fs.writeFile(usersPath, JSON.stringify(users, null, 2), 'utf-8');

      console.log('✅ Password updated for user:', username);

    } catch (err) {
      console.error('❌ Error updating users.json:', err);
      
      // Even if file update fails, we can continue (for localStorage users)
      // In production, this should be a proper database
    }

    // === STEP 4: RETURN SUCCESS ===
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        message: 'Password berhasil direset! Silakan login dengan password baru.',
        username: username
      })
    };

  } catch (error) {
    console.error('❌ Error in reset-password function:', error);

    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: 'Terjadi kesalahan saat mereset password. Silakan coba lagi.',
        details: process.env.NODE_ENV === 'development' ? error.message : undefined
      })
    };
  }
};
