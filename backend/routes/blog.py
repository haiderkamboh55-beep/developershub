from flask import Blueprint, request, jsonify
from db import get_db
from auth_utils import admin_required

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/', methods=['GET'])
def get_posts():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM blog_posts ORDER BY created_at DESC')
    posts = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(posts)

@blog_bp.route('/<int:id>', methods=['GET'])
def get_post(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM blog_posts WHERE id = %s', (id,))
    post = cur.fetchone()
    cur.close()
    conn.close()
    if post:
        return jsonify(post)
    return jsonify({'error': 'Post not found'}), 404

@blog_bp.route('/', methods=['POST'])
@admin_required
def create_post():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO blog_posts (title, content, excerpt, author, image_url) VALUES (%s, %s, %s, %s, %s) RETURNING id',
                 (data.get('title'), data.get('content'), data.get('excerpt'), data.get('author', 'Admin'), data.get('image_url')))
    new_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': new_id, 'message': 'Post created'}), 201

@blog_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_post(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM blog_posts WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Post deleted'})

@blog_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def edit_post(id):
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE blog_posts SET title = %s, content = %s, excerpt = %s, image_url = %s WHERE id = %s',
                (data.get('title'), data.get('content'), data.get('excerpt'), data.get('image_url'), id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Post updated'})
