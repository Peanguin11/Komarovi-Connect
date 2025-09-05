from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sqlite3
import hashlib
import datetime
import json
from typing import Dict, List

app = Flask(__name__)
CORS(app)  


ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()


def init_db():
    conn = sqlite3.connect('donations.db')
    cursor = conn.cursor()
    
   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            goal INTEGER NOT NULL,
            raised INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            donor_name TEXT DEFAULT 'ანონიმური',
            card_last4 TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    ''')
    
    
    cursor.execute('SELECT COUNT(*) FROM projects')
    if cursor.fetchone()[0] == 0:
        demo_projects = [
            ('ვყიდულობ ფერარის', 
             'სურვლი გავაჩნი რომ კომაროვს ქონდეს ფერარი.', 
             15000),
            ('ვყიდულობთ შაურმას', 
             'მშია.', 
             25000)
        ]
        cursor.executemany('INSERT INTO projects (title, description, goal) VALUES (?, ?, ?)', demo_projects)
    
    conn.commit()
    conn.close()


@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if password_hash == ADMIN_PASSWORD_HASH:
            return jsonify({'success': True, 'message': 'წარმატებული ავტორიზაცია'})
        else:
            return jsonify({'success': False, 'message': 'არასწორი პაროლი'}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'შეცდომა: {str(e)}'}), 500


@app.route('/api/projects', methods=['GET'])
def get_projects():
    try:
        conn = sqlite3.connect('donations.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.id, p.title, p.description, p.goal, p.raised, p.created_at,
                   COUNT(d.id) as donation_count
            FROM projects p
            LEFT JOIN donations d ON p.id = d.project_id
            GROUP BY p.id
            ORDER BY p.created_at DESC
        ''')
        
        projects = []
        for row in cursor.fetchall():
            projects.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'goal': row[3],
                'raised': row[4],
                'created_at': row[5],
                'donation_count': row[6]
            })
        
        conn.close()
        return jsonify({'success': True, 'projects': projects})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'შეცდომა: {str(e)}'}), 500


@app.route('/api/admin/projects', methods=['POST'])
def add_project():
    try:
        data = request.get_json()
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        goal = int(data.get('goal', 0))
        
        if not title or not description or goal <= 0:
            return jsonify({'success': False, 'message': 'ყველა ველი სავალდებულოა'}), 400
        
        conn = sqlite3.connect('donations.db')
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO projects (title, description, goal) VALUES (?, ?, ?)',
            (title, description, goal)
        )
        
        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'პროექტი წარმატებით დაემატა',
            'project_id': project_id
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'შეცდომა: {str(e)}'}), 500


@app.route('/api/admin/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    try:
        conn = sqlite3.connect('donations.db')
        cursor = conn.cursor()
        
        
        cursor.execute('DELETE FROM donations WHERE project_id = ?', (project_id,))
        
        
        cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        
        if cursor.rowcount == 0:
            return jsonify({'success': False, 'message': 'პროექტი ვერ მოიძებნა'}), 404
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'პროექტი წარმატებით წაშლილია'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'შეცდომა: {str(e)}'}), 500


@app.route('/api/donate', methods=['POST'])
def make_donation():
    try:
        data = request.get_json()
        project_id = int(data.get('project_id', 0))
        amount = int(data.get('amount', 0))
        donor_name = data.get('donor_name', 'ანონიმური').strip()
        card_number = data.get('card_number', '').replace(' ', '')
        card_expiry = data.get('card_expiry', '')
        card_cvv = data.get('card_cvv', '')
        card_holder = data.get('card_holder', '').strip()
        
        # ვალიდაცია
        if project_id <= 0 or amount <= 0:
            return jsonify({'success': False, 'message': 'არასწორი მონაცემები'}), 400
        
        if len(card_number) != 16:
            return jsonify({'success': False, 'message': 'ბარათის ნომერი უნდა იყოს 16 ციფრი'}), 400
        
        if not card_expiry or len(card_expiry) != 5 or '/' not in card_expiry:
            return jsonify({'success': False, 'message': 'შეიყვანეთ სწორი ვალიდობა'}), 400
        
        if len(card_cvv) != 3:
            return jsonify({'success': False, 'message': 'CVV უნდა იყოს 3 ციფრი'}), 400
        
        if not card_holder:
            return jsonify({'success': False, 'message': 'შეიყვანეთ კარდჰოლდერის სახელი'}), 400
        
        
        import random
        payment_success = random.random() > 0.1  
        
        if not payment_success:
            return jsonify({'success': False, 'message': 'გადახდა ვერ შესრულდა. სცადეთ ხელახლა'}), 400
        
        
        conn = sqlite3.connect('donations.db')
        cursor = conn.cursor()
        
        
        cursor.execute('SELECT id FROM projects WHERE id = ?', (project_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'პროექტი ვერ მოიძებნა'}), 404
        
       
        card_last4 = card_number[-4:]
        cursor.execute(
            'INSERT INTO donations (project_id, amount, donor_name, card_last4) VALUES (?, ?, ?, ?)',
            (project_id, amount, donor_name, card_last4)
        )
        
        
        cursor.execute(
            'UPDATE projects SET raised = raised + ? WHERE id = ?',
            (amount, project_id)
        )
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'დონაცია {amount}₾ წარმატებით განხორციელდა! მადლობა {donor_name}!',
            'amount': amount,
            'donor': donor_name
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'შეცდომა: {str(e)}'}), 500


@app.route('/api/admin/stats', methods=['GET'])
def get_stats():
    try:
        conn = sqlite3.connect('donations.db')
        cursor = conn.cursor()
        
       
        cursor.execute('SELECT COUNT(*) FROM projects')
        total_projects = cursor.fetchone()[0]
        
        
        cursor.execute('SELECT SUM(raised) FROM projects')
        total_raised = cursor.fetchone()[0] or 0
        
        
        cursor.execute('SELECT COUNT(*) FROM donations')
        total_donations = cursor.fetchone()[0]
        
        
        cursor.execute('''
            SELECT d.amount, d.donor_name, p.title, d.created_at, d.card_last4
            FROM donations d
            JOIN projects p ON d.project_id = p.id
            ORDER BY d.created_at DESC
            LIMIT 10
        ''')
        
        recent_donations = []
        for row in cursor.fetchall():
            recent_donations.append({
                'amount': row[0],
                'donor': row[1],
                'project': row[2],
                'date': row[3],
                'card_last4': row[4]
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_projects': total_projects,
                'total_raised': total_raised,
                'total_donations': total_donations,
                'recent_donations': recent_donations
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'შეცდომა: {str(e)}'}), 500
