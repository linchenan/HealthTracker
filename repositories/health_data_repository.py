import sqlite3
from typing import List, Optional
from datetime import datetime
from interfaces.repositories import IHealthDataRepository
from models.domain import BloodPressureRecord, HeightWeightRecord


class HealthDataRepository(IHealthDataRepository):
    """SQLite implementation of health data repository"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    # Blood Pressure Methods
    def create_blood_pressure_record(self, record: BloodPressureRecord) -> bool:
        """Create a new blood pressure record"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                INSERT INTO blood_pressure (user_id, systolic, diastolic, pulse, notes, date, recorded_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (record.user_id, record.systolic, record.diastolic, record.pulse,
                  record.notes, record.date, record.recorded_at, record.created_at))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating blood pressure record: {e}")
            return False
    
    def get_blood_pressure_records_by_user(self, user_id: int) -> List[BloodPressureRecord]:
        """Get all blood pressure records for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("""
                SELECT * FROM blood_pressure 
                WHERE user_id = ? 
                ORDER BY recorded_at DESC
            """, (user_id,))
            rows = c.fetchall()
            conn.close()
            
            return [BloodPressureRecord(
                id=row['id'],
                user_id=row['user_id'],
                systolic=row['systolic'],
                diastolic=row['diastolic'],
                pulse=row['pulse'],
                notes=row['notes'],
                date=row['date'],
                recorded_at=row['recorded_at'],
                created_at=row['created_at']
            ) for row in rows]
        except Exception as e:
            print(f"Error getting blood pressure records: {e}")
            return []
    
    def update_blood_pressure_record(self, record: BloodPressureRecord) -> bool:
        """Update a blood pressure record"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                UPDATE blood_pressure 
                SET systolic = ?, diastolic = ?, pulse = ?, notes = ?, date = ?
                WHERE id = ?
            """, (record.systolic, record.diastolic, record.pulse, record.notes, 
                  record.date, record.id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating blood pressure record: {e}")
            return False
    
    def delete_blood_pressure_record(self, record_id: int) -> bool:
        """Delete a blood pressure record"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("DELETE FROM blood_pressure WHERE id = ?", (record_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting blood pressure record: {e}")
            return False
    
    # Height Weight Methods
    def create_height_weight_record(self, record: HeightWeightRecord) -> bool:
        """Create a new height/weight record"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                INSERT INTO height_weight (user_id, height, weight, notes, date, recorded_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (record.user_id, record.height, record.weight, record.notes,
                  record.date, record.recorded_at, record.created_at))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating height/weight record: {e}")
            return False
    
    def get_height_weight_records_by_user(self, user_id: int) -> List[HeightWeightRecord]:
        """Get all height/weight records for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("""
                SELECT * FROM height_weight 
                WHERE user_id = ? 
                ORDER BY recorded_at DESC
            """, (user_id,))
            rows = c.fetchall()
            conn.close()
            
            return [HeightWeightRecord(
                id=row['id'],
                user_id=row['user_id'],
                height=row['height'],
                weight=row['weight'],
                notes=row['notes'],
                date=row['date'],
                recorded_at=row['recorded_at'],
                created_at=row['created_at']
            ) for row in rows]
        except Exception as e:
            print(f"Error getting height/weight records: {e}")
            return []
    
    def update_height_weight_record(self, record: HeightWeightRecord) -> bool:
        """Update a height/weight record"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                UPDATE height_weight 
                SET height = ?, weight = ?, notes = ?, date = ?
                WHERE id = ?
            """, (record.height, record.weight, record.notes, record.date, record.id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating height/weight record: {e}")
            return False
    
    def delete_height_weight_record(self, record_id: int) -> bool:
        """Delete a height/weight record"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("DELETE FROM height_weight WHERE id = ?", (record_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting height/weight record: {e}")
            return False