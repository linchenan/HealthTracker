from flask import Blueprint, request, redirect, url_for, session, render_template, flash
import sqlite3

# 取得目前登入的使用者ID
def get_current_user_id():
    return session.get('username')

def create_health_bp(DB_PATH):
    health_bp = Blueprint('health', __name__)

    @health_bp.route('/record/blood_pressure', methods=['POST'])
    def record_blood_pressure():
        username = session.get('username')
        if not username:
            return redirect(url_for('login'))
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id FROM users WHERE username=?', (username,))
        row = c.fetchone()
        if not row:
            conn.close()
            return redirect(url_for('login'))
        user_id = row[0]
        systolic = int(request.form['systolic'])
        diastolic = int(request.form['diastolic'])
        c.execute('INSERT INTO blood_pressure (user_id, systolic, diastolic) VALUES (?, ?, ?)', (user_id, systolic, diastolic))
        conn.commit()
        conn.close()
        flash('血壓紀錄已新增')
        return redirect(url_for('blood_pressure'))

    @health_bp.route('/record/height_weight', methods=['POST'])
    def record_height_weight():
        username = session.get('username')
        if not username:
            return redirect(url_for('login'))
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id FROM users WHERE username=?', (username,))
        row = c.fetchone()
        if not row:
            conn.close()
            return redirect(url_for('login'))
        user_id = row[0]
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        c.execute('INSERT INTO height_weight (user_id, height, weight) VALUES (?, ?, ?)', (user_id, height, weight))
        conn.commit()
        conn.close()
        flash('身高體重紀錄已新增')
        return redirect(url_for('height_weight'))

    return health_bp
