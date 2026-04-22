from flask import Blueprint, request, jsonify
from db import get_db
from auth_utils import admin_required

booking_bp = Blueprint('bookings', __name__)

@booking_bp.route('/', methods=['POST'])
def create_booking():
    data = request.json
    if not data or not data.get('name') or not data.get('email') or not data.get('date') or not data.get('time_slot'):
        return jsonify({'error': 'Required fields missing'}), 400

    conn = get_db()
    cur = conn.cursor()
    # Check if slot is already booked
    cur.execute('SELECT id FROM bookings WHERE date = %s AND time_slot = %s AND status != %s', 
                            (data['date'], data['time_slot'], 'cancelled'))
    existing = cur.fetchone()
    if existing:
        cur.close()
        conn.close()
        return jsonify({'error': 'This time slot is already booked'}), 400

    cur.execute('INSERT INTO bookings (name, email, phone, date, time_slot, purpose) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
                 (data['name'], data['email'], data.get('phone'), data['date'], data['time_slot'], data.get('purpose')))
    new_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': new_id, 'message': 'Booking confirmed'}), 201

@booking_bp.route('/available', methods=['GET'])
def get_available_slots():
    date = request.args.get('date')
    if not date:
        return jsonify({'error': 'Date is required'}), 400

    all_slots = ['09:00', '10:00', '11:00', '13:00', '14:00', '15:00', '16:00']
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT time_slot FROM bookings WHERE date = %s AND status != %s', (date, 'cancelled'))
    booked = cur.fetchall()
    cur.close()
    conn.close()
    
    booked_slots = [b['time_slot'] for b in booked]
    available = [s for s in all_slots if s not in booked_slots]
    return jsonify(available)

@booking_bp.route('/', methods=['GET'])
@admin_required
def get_bookings():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM bookings ORDER BY date DESC, time_slot DESC')
    bookings = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(bookings)

@booking_bp.route('/<int:id>/status', methods=['PUT'])
@admin_required
def update_booking_status(id):
    status = request.json.get('status')
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE bookings SET status = %s WHERE id = %s', (status, id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Booking status updated'})
