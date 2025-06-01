from typing import List, Dict, Optional
from datetime import datetime, timedelta
import sqlite3

class MoodRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_today_mood(self, user_id: int) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        today = datetime.today().strftime('%Y-%m-%d')
        c.execute('SELECT id, mood, mood_date, created_at FROM mood_records WHERE user_id=? AND mood_date=?', (user_id, today))
        row = c.fetchone()
        conn.close()
        if row:
            return {'id': row[0], 'mood': row[1], 'mood_date': row[2], 'created_at': row[3]}
        return None

    def add_mood(self, user_id: int, mood: str) -> None:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        today = datetime.today().strftime('%Y-%m-%d')
        c.execute('INSERT INTO mood_records (user_id, mood, mood_date) VALUES (?, ?, ?)', (user_id, mood, today))
        conn.commit()
        conn.close()

    def get_last_7_days(self, user_id: int) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        seven_days_ago = (datetime.today() - timedelta(days=6)).strftime('%Y-%m-%d')
        c.execute('SELECT mood, mood_date FROM mood_records WHERE user_id=? AND mood_date >= ? ORDER BY mood_date DESC', (user_id, seven_days_ago))
        rows = c.fetchall()
        conn.close()
        return [{'mood': r[0], 'mood_date': r[1]} for r in rows]
