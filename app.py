from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from health_routes import create_health_bp
from di_container import initialize_container, get_auth_service, get_health_service, get_notification_service
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 請改為安全的隨機字串

DB_PATH = 'healthTracker.db'

# Initialize dependency injection container
initialize_container(DB_PATH)

def init_db():
    """Initialize database with required tables"""
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create users table with all required fields
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            gender TEXT,
            birthday TEXT,
            created_at TEXT
        )
    """)
    
    # Create health data tables
    c.execute("""
        CREATE TABLE IF NOT EXISTS blood_pressure (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            systolic INTEGER,
            diastolic INTEGER,
            pulse INTEGER,
            notes TEXT,
            date TEXT,
            recorded_at TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS height_weight (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            height REAL,
            weight REAL,
            notes TEXT,
            date TEXT,
            recorded_at TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            visit_date TEXT,
            hospital TEXT,
            department TEXT,
            doctor TEXT,
            diagnosis TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            appointment_date TEXT,
            hospital TEXT,
            department TEXT,
            doctor TEXT,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS exercise_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            exercise_date TEXT,
            exercise_type TEXT,
            duration INTEGER,
            calories INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS diet_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            diet_date TEXT,
            meal_type TEXT,
            description TEXT,
            calories INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    
    # Add missing columns to existing tables
    columns = [row[1] for row in c.execute("PRAGMA table_info(users)")]
    for col, coltype in [('email', 'TEXT'), ('gender', 'TEXT'), ('birthday', 'TEXT'), ('created_at', 'TEXT')]:
        if col not in columns:
            c.execute(f'ALTER TABLE users ADD COLUMN {col} {coltype}')
    
    # Add missing columns to blood_pressure table
    bp_columns = [row[1] for row in c.execute("PRAGMA table_info(blood_pressure)")]
    for col, coltype in [('pulse', 'INTEGER'), ('notes', 'TEXT'), ('date', 'TEXT'), ('recorded_at', 'TEXT')]:
        if col not in bp_columns:
            c.execute(f'ALTER TABLE blood_pressure ADD COLUMN {col} {coltype}')
    
    # Add missing columns to height_weight table
    hw_columns = [row[1] for row in c.execute("PRAGMA table_info(height_weight)")]
    for col, coltype in [('notes', 'TEXT'), ('date', 'TEXT'), ('recorded_at', 'TEXT')]:
        if col not in hw_columns:
            c.execute(f'ALTER TABLE height_weight ADD COLUMN {col} {coltype}')
    
    conn.commit()
    conn.close()

init_db()

def get_current_user():
    """Get current logged in user"""
    username = session.get('username')
    if not username:
        return None
    
    auth_service = get_auth_service()
    user = auth_service.get_user_by_username(username)
    if user:
        # Convert User object to dict for backward compatibility
        return {
            'id': user.id,
            'username': user.username,
            'password': user.password,
            'email': user.email,
            'gender': user.gender,
            'birthday': user.birthday,
            'created_at': user.created_at
        }
    return None

@app.route('/')
def index():
    """Main dashboard page"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    health_service = get_health_service()
    notification_service = get_notification_service()
    
    # Get user profile information
    gender, birthday = health_service.get_user_profile(user['id'])
    age_str, age_years = health_service.calculate_age_and_days(birthday)
    
    # Get health recommendations
    disease_info, prevention = health_service.get_disease_info_and_prevention(age_years)
    # 修正：確保 disease_info, prevention 為 list 型態
    if isinstance(disease_info, str):
        disease_info = [disease_info]
    if isinstance(prevention, str):
        prevention = [prevention]
    warning = '※以上資訊僅供參考，實際健康狀況請諮詢專業醫師診斷與建議。'
    
    # Get next appointment
    next_appointment = None
    appt_reminder = None
    
    # Query next appointment from database
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.today().date()
    c.execute('''SELECT appointment_date, hospital, department, reason FROM appointments 
                WHERE user_id=? AND appointment_date >= ? ORDER BY appointment_date ASC LIMIT 1''', 
              (user['id'], today.strftime('%Y-%m-%d')))
    appt = c.fetchone()
    
    if appt:
        appt_date = datetime.strptime(appt[0], '%Y-%m-%d').date()
        days_left = (appt_date - today).days
        next_appointment = {
            'date': appt[0],
            'hospital': appt[1],
            'department': appt[2],
            'reason': appt[3],
            'days_left': days_left
        }
        
        if days_left <= 7:
            appt_reminder = f"⚠️ 您有預約於 {appt[0]} ({days_left} 天後) 於 {appt[1]} {appt[2]} 看診，請準備相關資料。"
        else:
            appt_reminder = f"下次預約看診：{appt[0]}，{appt[1]} {appt[2]}。"
    
    conn.close()
    
    # 取得最新血壓與BMI評估
    bp_records = health_service.get_blood_pressure_records(user['id'])
    bp_list = [
        {
            'id': r['id'],
            'systolic': r['systolic'],
            'diastolic': r['diastolic'],
            'created_at': r.get('date', r.get('created_at', ''))
        } for r in bp_records
    ]
    latest_bp = bp_list[0] if bp_list else None
    bp_evaluation = health_service.evaluate_blood_pressure(latest_bp)

    hw_records = health_service.get_height_weight_records(user['id'])
    hw_list = [
        {
            'id': r['id'],
            'height': r['height'],
            'weight': r['weight'],
            'created_at': r.get('date', r.get('created_at', ''))
        } for r in hw_records
    ]
    latest_hw = hw_list[0] if hw_list else None
    gender, birthday = health_service.get_user_profile(user['id'])
    _, age = health_service.calculate_age_and_days(birthday)
    bmi_evaluation = health_service.evaluate_bmi(latest_hw, gender, age)

    return render_template('index.html', 
                         username=user['username'], 
                         age_str=age_str, 
                         disease_info=disease_info, 
                         prevention=prevention, 
                         warning=warning, 
                         next_appointment=next_appointment, 
                         appt_reminder=appt_reminder,
                         bp_evaluation=bp_evaluation,
                         bmi_evaluation=bmi_evaluation)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        auth_service = get_auth_service()
        if auth_service.register_user(username, password):
            flash('註冊成功，請登入')
            return redirect(url_for('login'))
        else:
            flash('註冊失敗，使用者名稱可能已存在')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        auth_service = get_auth_service()
        user = auth_service.authenticate_user(username, password)
        if user:
            session['username'] = username
            return redirect(url_for('index'))
        
        flash('帳號或密碼錯誤')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.pop('username', None)
    flash('已登出')
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """User profile management"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    health_service = get_health_service()
    
    if request.method == 'POST':
        gender = request.form['gender']
        birthday = request.form['birthday']
        
        # Update profile using health service
        health_service.update_user_profile(user['id'], gender, birthday)
        flash('基本資料已更新')
        return redirect(url_for('profile'))
    
    # Get current profile data
    gender, birthday = health_service.get_user_profile(user['id'])
    age_str, _ = health_service.calculate_age_and_days(birthday)
    
    return render_template('profile.html', 
                         gender=gender, 
                         birthday=birthday, 
                         age_str=age_str, 
                         username=user['username'])

@app.route('/blood_pressure')
def blood_pressure():
    """Blood pressure records page"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    health_service = get_health_service()
    
    # Handle delete request
    if request.args.get('delete_id'):
        delete_id = int(request.args.get('delete_id'))
        health_service.delete_blood_pressure_record(delete_id, user['id'])
        flash('血壓紀錄已刪除')
        return redirect(url_for('blood_pressure'))
    
    # Get blood pressure records
    bp_records = health_service.get_blood_pressure_records(user['id'])
    
    # Convert to format expected by template
    bp_list = []
    for record in bp_records:
        bp_list.append({
            'id': record['id'],
            'systolic': record['systolic'],
            'diastolic': record['diastolic'],
            'created_at': record.get('date', record.get('created_at', ''))
        })
    
    # Get health evaluation for latest record
    latest_bp = bp_list[0] if bp_list else None
    evaluations = health_service.evaluate_blood_pressure(latest_bp)
    
    return render_template('blood_pressure.html', 
                         bp_list=bp_list, 
                         evaluations=evaluations, 
                         username=user['username'])

@app.route('/height_weight')
def height_weight():
    """Height and weight records page"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    health_service = get_health_service()
    
    # Handle delete request
    if request.args.get('delete_id'):
        delete_id = int(request.args.get('delete_id'))
        health_service.delete_height_weight_record(delete_id, user['id'])
        flash('身高體重紀錄已刪除')
        return redirect(url_for('height_weight'))
    
    # Get height/weight records
    hw_records = health_service.get_height_weight_records(user['id'])
    
    # Convert to format expected by template
    hw_list = []
    for record in hw_records:
        hw_list.append({
            'id': record['id'],
            'height': record['height'],
            'weight': record['weight'],
            'created_at': record.get('date', record.get('created_at', ''))
        })
    
    # Get health evaluation for latest record
    latest_hw = hw_list[0] if hw_list else None
    gender, birthday = health_service.get_user_profile(user['id'])
    _, age = health_service.calculate_age_and_days(birthday)
    evaluation = health_service.evaluate_bmi(latest_hw, gender, age)
    return render_template('height_weight.html', 
                         hw_list=hw_list, 
                         evaluation=evaluation, 
                         username=user['username'])

@app.route('/medical_records', methods=['GET', 'POST'])
def medical_records():
    """Medical records management"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if request.method == 'POST':
        visit_date = request.form['visit_date']
        hospital = request.form['hospital']
        department = request.form['department']
        diagnosis = request.form['diagnosis']
        notes = request.form['notes']
        
        c.execute('''INSERT INTO medical_records (user_id, visit_date, hospital, department, diagnosis, notes) 
                    VALUES (?, ?, ?, ?, ?, ?)''',
                  (user['id'], visit_date, hospital, department, diagnosis, notes))
        conn.commit()
        flash('醫療紀錄已新增')
    
    # Handle delete request
    if request.args.get('delete_id'):
        delete_id = request.args.get('delete_id')
        c.execute('DELETE FROM medical_records WHERE id=? AND user_id=?', (delete_id, user['id']))
        conn.commit()
        flash('醫療紀錄已刪除')
        return redirect(url_for('medical_records'))
    
    # Get medical records
    c.execute('''SELECT id, visit_date, hospital, department, diagnosis, notes 
                FROM medical_records WHERE user_id=? ORDER BY visit_date DESC''', (user['id'],))
    records = c.fetchall()
    conn.close()
    
    return render_template('medical_records.html', records=records, username=user['username'])

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    """Appointments management"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if request.method == 'POST':
        appointment_date = request.form['appointment_date']
        hospital = request.form['hospital']
        department = request.form['department']
        reason = request.form['reason']
        
        c.execute('''INSERT INTO appointments (user_id, appointment_date, hospital, department, reason) 
                    VALUES (?, ?, ?, ?, ?)''',
                  (user['id'], appointment_date, hospital, department, reason))
        conn.commit()
        flash('預約看診紀錄已新增')
    
    # Handle delete request
    if request.args.get('delete_id'):
        delete_id = request.args.get('delete_id')
        c.execute('DELETE FROM appointments WHERE id=? AND user_id=?', (delete_id, user['id']))
        conn.commit()
        flash('預約看診紀錄已刪除')
        return redirect(url_for('appointments'))
    
    # Get appointments
    c.execute('''SELECT id, appointment_date, hospital, department, reason 
                FROM appointments WHERE user_id=? ORDER BY appointment_date DESC''', (user['id'],))
    appts = c.fetchall()
    conn.close()
    
    return render_template('appointments.html', appts=appts, username=user['username'])

@app.route('/exercise', methods=['GET', 'POST'])
def exercise():
    """Exercise records management"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    encouragement = None
    calories_table = {
        '快走': 4.5,   # METs
        '慢跑': 7.0,
        '騎自行車': 6.0,
        '游泳': 8.0,
        '瑜珈': 3.0,
        '跳繩': 10.0,
        '有氧舞蹈': 6.5,
        '重量訓練': 5.0,
        '登山健行': 6.0,
        '球類運動': 7.0,
        '其他': 4.0
    }
    
    # Get user weight
    c.execute('SELECT weight FROM height_weight WHERE user_id=? ORDER BY created_at DESC LIMIT 1', (user['id'],))
    row = c.fetchone()
    weight = row[0] if row else 65  # Default 65kg if no data
    
    if request.method == 'POST':
        exercise_date = request.form['exercise_date']
        exercise_type = request.form['exercise_type']
        duration = int(request.form['duration'])
        notes = request.form['notes']
        
        mets = calories_table.get(exercise_type, 4.0)
        calories = int(mets * weight * duration / 60)
        
        c.execute('''INSERT INTO exercise_records (user_id, exercise_date, exercise_type, duration, calories, notes) 
                    VALUES (?, ?, ?, ?, ?, ?)''',
                  (user['id'], exercise_date, exercise_type, duration, calories, notes))
        conn.commit()
        encouragement = f"太棒了！這次運動大約消耗了 {calories} 大卡，持續運動讓健康加分！"
    
    # Handle delete request
    if request.args.get('delete_id'):
        delete_id = request.args.get('delete_id')
        c.execute('DELETE FROM exercise_records WHERE id=? AND user_id=?', (delete_id, user['id']))
        conn.commit()
        flash('運動紀錄已刪除')
        return redirect(url_for('exercise'))
    
    # Get exercise records
    c.execute('''SELECT id, exercise_date, exercise_type, duration, calories, notes 
                FROM exercise_records WHERE user_id=? ORDER BY exercise_date DESC''', (user['id'],))
    records = c.fetchall()
    
    total_calories = sum(r[4] for r in records)
    if not encouragement and records:
        if total_calories >= 2000:
            encouragement = f"本月已累積消耗 {total_calories} 大卡，運動習慣很棒，繼續保持！"
        elif total_calories >= 1000:
            encouragement = f"本月已累積消耗 {total_calories} 大卡，離健康更進一步！"
        else:
            encouragement = f"已經開始運動紀錄，繼續努力，健康就在不遠處！"
    
    conn.close()
    
    return render_template('exercise.html', 
                         records=records, 
                         encouragement=encouragement, 
                         username=user['username'])

@app.route('/diet', methods=['GET', 'POST'])
def diet():
    """Diet records management"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get user data for calorie calculation
    c.execute('SELECT gender, birthday FROM users WHERE id=?', (user['id'],))
    row = c.fetchone()
    gender, birthday = row if row else (None, None)
    
    c.execute('SELECT weight, height FROM height_weight WHERE user_id=? ORDER BY created_at DESC LIMIT 1', (user['id'],))
    wh = c.fetchone()
    weight, height = wh if wh else (65, 170)
    
    # Calculate age
    age = None
    if birthday:
        from datetime import date
        try:
            bdate = datetime.strptime(birthday, '%Y-%m-%d').date()
            today = date.today()
            age = today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))
        except:
            age = 30
    
    # Calculate BMR and suggested calories
    if gender == 'male':
        bmr = 66 + 13.7 * weight + 5 * height - 6.8 * (age if age else 30)
    elif gender == 'female':
        bmr = 655 + 9.6 * weight + 1.8 * height - 4.7 * (age if age else 30)
    else:
        bmr = 1500
    
    suggest_min = int(bmr * 1.5)
    suggest_max = int(bmr * 1.7)
    
    if request.method == 'POST':
        diet_date = request.form['diet_date']
        meal_type = request.form['meal_type']
        description = request.form['description']
        calories = int(request.form['calories'])
        
        c.execute('''INSERT INTO diet_records (user_id, diet_date, meal_type, description, calories) 
                    VALUES (?, ?, ?, ?, ?)''',
                  (user['id'], diet_date, meal_type, description, calories))
        conn.commit()
        flash('飲食紀錄已新增')
    
    # Handle delete request
    if request.args.get('delete_id'):
        delete_id = request.args.get('delete_id')
        c.execute('DELETE FROM diet_records WHERE id=? AND user_id=?', (delete_id, user['id']))
        conn.commit()
        flash('飲食紀錄已刪除')
        return redirect(url_for('diet'))
    
    # Get today's diet records
    today_str = datetime.today().strftime('%Y-%m-%d')
    c.execute('''SELECT id, diet_date, meal_type, description, calories 
                FROM diet_records WHERE user_id=? AND diet_date=? ORDER BY created_at DESC''', 
              (user['id'], today_str))
    records = c.fetchall()
    
    total_cal = sum(r[4] for r in records)
    
    # Calculate status message
    if total_cal < suggest_min:
        status = f"今日總攝取 {total_cal} 大卡，低於建議攝取量 ({suggest_min}~{suggest_max} 大卡)，可適量增加營養攝取。"
    elif total_cal > suggest_max:
        status = f"今日總攝取 {total_cal} 大卡，超過建議攝取量 ({suggest_min}~{suggest_max} 大卡)，請注意飲食控制。"
    else:
        status = f"今日總攝取 {total_cal} 大卡，落在建議範圍 ({suggest_min}~{suggest_max} 大卡)，請持續保持！"
    
    # Get chart data for last 14 days
    c.execute('''SELECT diet_date, SUM(calories) 
                FROM diet_records WHERE user_id=? 
                GROUP BY diet_date ORDER BY diet_date DESC LIMIT 14''', (user['id'],))
    chart_rows = c.fetchall()[::-1]  # Reverse to show oldest to newest
    
    chart_labels = [r[0] for r in chart_rows]
    chart_data = [r[1] for r in chart_rows]
    chart_suggest = [int((suggest_min + suggest_max) / 2)] * len(chart_labels)
    
    conn.close()
    
    return render_template('diet.html', 
                         records=records, 
                         status=status, 
                         suggest_min=suggest_min, 
                         suggest_max=suggest_max, 
                         total_cal=total_cal, 
                         username=user['username'], 
                         now=datetime.today(), 
                         chart_labels=chart_labels, 
                         chart_data=chart_data, 
                         chart_suggest=chart_suggest)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password: verify username and birthday, then reset password"""
    if request.method == 'POST':
        username = request.form['username']
        birthday = request.form['birthday']
        new_password = request.form['new_password']
        auth_service = get_auth_service()
        user = auth_service.get_user_by_username(username)
        if not user:
            flash('查無此帳號，請確認輸入')
            return render_template('forgot_password.html')
        # 比對生日
        if not user.birthday or user.birthday != birthday:
            flash('生日驗證失敗，請確認輸入')
            return render_template('forgot_password.html')
        # 更新密碼
        if auth_service.update_user_password(username, new_password):
            flash('密碼已重設，請使用新密碼登入')
            return redirect(url_for('login'))
        else:
            flash('密碼重設失敗，請稍後再試')
            return render_template('forgot_password.html')
    return render_template('forgot_password.html')

# Register health data Blueprint
app.register_blueprint(create_health_bp(DB_PATH))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
