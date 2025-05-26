import sqlite3
from datetime import datetime, date

DB_PATH = 'healthTracker.db'

class UserRepository:
    def get_by_username(self, username):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, username, password FROM users WHERE username=?', (username,))
        row = c.fetchone()
        conn.close()
        if row:
            return {'id': row[0], 'username': row[1], 'password': row[2]}
        return None

    def get_profile(self, user_id):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT gender, birthday FROM users WHERE id=?', (user_id,))
        row = c.fetchone()
        conn.close()
        return row if row else ('', '')

    def update_profile(self, user_id, gender, birthday):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE users SET gender=?, birthday=? WHERE id=?', (gender, birthday, user_id))
        conn.commit()
        conn.close()

    def create(self, username, password_hash):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        conn.close()

class HealthService:
    @staticmethod
    def calculate_age_and_days(birthday):
        age_str = ''
        age_years = None
        if birthday:
            try:
                bdate = datetime.strptime(birthday, '%Y-%m-%d').date()
                today = date.today()
                years = today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))
                this_year_birthday = bdate.replace(year=today.year)
                if today < this_year_birthday:
                    last_birthday = bdate.replace(year=today.year - 1)
                else:
                    last_birthday = this_year_birthday
                days = (today - last_birthday).days
                age_str = f'{years} 歲又 {days} 天'
                age_years = years
            except Exception:
                age_str = '生日格式錯誤'
                age_years = None
        return age_str, age_years

    @staticmethod
    def get_disease_info_and_prevention(age_years):
        disease_info = []
        prevention = []
        if age_years is not None:
            if age_years >= 65:
                disease_info = [
                    '高血壓、高血脂、糖尿病、心血管疾病、骨質疏鬆、失智症、退化性關節炎、白內障等。',
                    '建議定期健康檢查，注意慢性病管理與預防跌倒。'
                ]
                prevention = [
                    '均衡飲食，減少高油高鹽食物攝取。',
                    '維持規律運動，增強肌力與平衡感。',
                    '定期量測血壓、血糖、血脂。',
                    '預防跌倒，居家環境保持安全。',
                    '維持社交活動，預防失智與憂鬱。'
                ]
            elif age_years >= 45:
                disease_info = [
                    '高血壓、高血脂、糖尿病、心血管疾病、代謝症候群、退化性關節炎等。',
                    '建議維持健康飲食、規律運動，及早預防慢性病。'
                ]
                prevention = [
                    '控制體重，避免肥胖。',
                    '多蔬果、少油炸，減少精緻糖攝取。',
                    '每週至少150分鐘中等強度運動。',
                    '定期健康檢查，及早發現慢性病。',
                    '避免菸酒，減少心血管疾病風險。'
                ]
            elif age_years >= 30:
                disease_info = [
                    '高血壓、代謝症候群、脂肪肝、心血管疾病等風險逐漸增加。',
                    '建議養成健康生活型態，定期健康檢查。'
                ]
                prevention = [
                    '養成運動習慣，維持理想體重。',
                    '避免熬夜與過度壓力。',
                    '均衡飲食，少吃加工食品。',
                    '定期健康檢查，早期發現異常。'
                ]
        return disease_info, prevention

    @staticmethod
    def get_latest_blood_pressure(user_id):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT systolic, diastolic, created_at FROM blood_pressure WHERE user_id=? ORDER BY created_at DESC LIMIT 1', (user_id,))
        row = c.fetchone()
        conn.close()
        if row:
            return {'systolic': row[0], 'diastolic': row[1], 'created_at': row[2]}
        return None

    @staticmethod
    def evaluate_blood_pressure(bp):
        if not bp:
            return []
        evaluations = []
        if bp['systolic'] > 140 or bp['diastolic'] > 90:
            evaluations.append('血壓偏高，建議減少鹽分攝取並規律運動。')
        else:
            evaluations.append('血壓正常，請持續保持健康生活。')
        return evaluations

    @staticmethod
    def get_blood_pressure_history(user_id):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT systolic, diastolic, created_at FROM blood_pressure WHERE user_id=? ORDER BY created_at DESC', (user_id,))
        rows = c.fetchall()
        conn.close()
        return [{'systolic': row[0], 'diastolic': row[1], 'created_at': row[2]} for row in rows]

    @staticmethod
    def get_latest_height_weight(user_id):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT height, weight, created_at FROM height_weight WHERE user_id=? ORDER BY created_at DESC LIMIT 1', (user_id,))
        row = c.fetchone()
        conn.close()
        if row:
            return {'height': row[0], 'weight': row[1], 'created_at': row[2]}
        return None

    @staticmethod
    def get_height_weight_history(user_id):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT height, weight, created_at FROM height_weight WHERE user_id=? ORDER BY created_at DESC', (user_id,))
        rows = c.fetchall()
        conn.close()
        return [{'height': row[0], 'weight': row[1], 'created_at': row[2]} for row in rows]

    @staticmethod
    def evaluate_bmi(hw, gender=None, age=None):
        if not hw:
            return []
        evaluations = []
        bmi = hw['weight'] / ((hw['height']/100) ** 2)
        evaluations.append(f'您的 BMI 為 {bmi:.1f}')
        bmr = None
        if gender and age is not None:
            try:
                age = int(age)
                if gender == 'male':
                    bmr = 66 + 13.7 * hw['weight'] + 5 * hw['height'] - 6.8 * age
                elif gender == 'female':
                    bmr = 655 + 9.6 * hw['weight'] + 1.8 * hw['height'] - 4.7 * age
                if bmr:
                    evaluations.append(f'建議每日基礎代謝率：約 {bmr:.0f} 大卡')
                    evaluations.append(f'建議每日總熱量攝取：約 {bmr*1.5:.0f} ~ {bmr*1.7:.0f} 大卡 (依活動量調整)')
            except Exception:
                pass
        if bmi < 18.5:
            evaluations.append('體重過輕，建議增加營養攝取，適度運動以增強體力。')
            evaluations.append('可諮詢營養師，規劃高熱量均衡飲食。')
        elif bmi < 24:
            evaluations.append('體重正常，請持續保持健康飲食與規律運動。')
            evaluations.append('建議每年定期健康檢查。')
        elif bmi < 27:
            evaluations.append('體重略高，建議減少高熱量食物攝取，增加運動量。')
            evaluations.append('可設定每週運動目標，並監測體重變化。')
        else:
            evaluations.append('體重過重，建議積極控制飲食並規律運動。')
            evaluations.append('可尋求專業醫療或營養諮詢，預防慢性疾病。')
        return evaluations
