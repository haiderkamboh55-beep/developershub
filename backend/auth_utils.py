import jwt
import bcrypt
from functools import wraps
from flask import request, jsonify
from config import Config
from db import get_db

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Token is missing or invalid'}), 401
        
        token = token.split(' ')[1]
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            conn = get_db()
            cur = conn.cursor()
            cur.execute('SELECT * FROM users WHERE id = %s', (data['user_id'],))
            user = cur.fetchone()
            cur.close()
            conn.close()
            
            if not user or user['role'] != 'admin':
                return jsonify({'error': 'Admin privileges required'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
            
        return f(*args, **kwargs)
    return decorated
