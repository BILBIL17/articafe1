from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

# Membuat database dan tabel
def create_database():
    connection = sqlite3.connect('members.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

# Route: Add Member
@app.route('/add_member', methods=['POST'])
def add_member():
    data = request.json
    member_id = data.get('id')
    name = data.get('name')
    email = data.get('email')

    if not member_id or not name or not email:
        return jsonify({'status': 'error', 'message': 'All fields are required'}), 400

    connection = sqlite3.connect('members.db')
    cursor = connection.cursor()

    cursor.execute('SELECT id FROM members WHERE id = ?', (member_id,))
    if cursor.fetchone():
        connection.close()
        return jsonify({'status': 'error', 'message': 'Member ID already exists'}), 400

    cursor.execute('INSERT INTO members (id, name, email) VALUES (?, ?, ?)', (member_id, name, email))
    connection.commit()
    connection.close()

    return jsonify({'status': 'success', 'message': 'Member added successfully'}), 200

# Route: Verify Member
@app.route('/verify_member/<int:member_id>', methods=['GET'])
def verify_member(member_id):
    connection = sqlite3.connect('members.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM members WHERE id = ?', (member_id,))
    member = cursor.fetchone()
    connection.close()

    if member:
        return jsonify({'status': 'success', 'data': {'id': member[0], 'name': member[1], 'email': member[2]}})
    else:
        return jsonify({'status': 'error', 'message': 'Member not found'}), 404

# Route: Dashboard
@app.route('/dashboard')
def dashboard():
    connection = sqlite3.connect('members.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    connection.close()
    return render_template("dashboard.html", members=members)

# Jalankan server
if __name__ == '__main__':
    create_database()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
