from flask import Blueprint, request, jsonify
from db import get_db
from auth_utils import admin_required

services_bp = Blueprint('services', __name__)

@services_bp.route('/', methods=['GET'])
def get_services():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM services ORDER BY id ASC')
    services = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(services)

@services_bp.route('/', methods=['POST'])
@admin_required
def create_service():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO services (title, description, icon) VALUES (%s, %s, %s) RETURNING id',
                 (data.get('title'), data.get('description'), data.get('icon', 'code')))
    new_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': new_id, 'message': 'Service created'}), 201

@services_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_service(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM services WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Service deleted'})

@services_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def edit_service(id):
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE services SET title = %s, description = %s, icon = %s WHERE id = %s',
                (data.get('title'), data.get('description'), data.get('icon'), id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Service updated'})
