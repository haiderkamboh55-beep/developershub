from flask import Blueprint, request, jsonify
from db import get_db
from auth_utils import admin_required

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/', methods=['POST'])
def submit_inquiry():
    data = request.json
    if not data or not data.get('name') or not data.get('email') or not data.get('message'):
        return jsonify({'error': 'Name, email, and message are required'}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO inquiries (name, email, phone, message) VALUES (%s, %s, %s, %s) RETURNING id',
                 (data['name'], data['email'], data.get('phone'), data['message']))
    new_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': new_id, 'message': 'Inquiry received successfully'}), 201

@contact_bp.route('/', methods=['GET'])
@admin_required
def get_inquiries():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM inquiries ORDER BY created_at DESC')
    inquiries = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(inquiries)

@contact_bp.route('/<int:id>/status', methods=['PUT'])
@admin_required
def update_inquiry_status(id):
    status = request.json.get('status')
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE inquiries SET status = %s WHERE id = %s', (status, id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Status updated'})
