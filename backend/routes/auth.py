from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import datetime
from config import Config
from db import get_db
from auth_utils import admin_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE email = %s', (data['email'],))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password_hash'].encode('utf-8')):
        token = jwt.encode({
            'user_id': user['id'],
            'email': user['email'],
            'role': user['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, Config.SECRET_KEY, algorithm='HS256')

        return jsonify({
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role']
            }
        })
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/me', methods=['GET'])
@admin_required
def me():
    return jsonify({'message': 'Valid token'})
