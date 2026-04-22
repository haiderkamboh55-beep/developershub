from flask import Blueprint, request, jsonify
from db import get_db
from auth_utils import admin_required

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/', methods=['GET'])
def get_portfolio():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM portfolio ORDER BY id DESC')
    items = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(items)

@portfolio_bp.route('/', methods=['POST'])
@admin_required
def create_portfolio():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO portfolio (title, description, image_url, tech_stack, project_url) VALUES (%s, %s, %s, %s, %s) RETURNING id',
                 (data.get('title'), data.get('description'), data.get('image_url'), data.get('tech_stack'), data.get('project_url')))
    new_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': new_id, 'message': 'Project created'}), 201

@portfolio_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_portfolio(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM portfolio WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Project deleted'})

@portfolio_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def edit_portfolio(id):
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE portfolio SET title = %s, description = %s, image_url = %s, tech_stack = %s, project_url = %s WHERE id = %s',
                (data.get('title'), data.get('description'), data.get('image_url'), data.get('tech_stack'), data.get('project_url'), id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Project updated'})
