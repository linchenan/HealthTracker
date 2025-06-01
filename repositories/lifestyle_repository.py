import sqlite3
from typing import List, Optional
from interfaces.repositories import ILifestyleRepository
from models.domain import ExerciseRecord, DietRecord


class LifestyleRepository(ILifestyleRepository):
    """SQLite implementation of lifestyle repository"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    # Exercise Record Methods
    def create_exercise_record(self, record: ExerciseRecord) -> bool:
        """Create a new exercise record"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                INSERT INTO exercise (user_id, exercise_type, duration, intensity, calories_burned, notes, date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (record.user_id, record.exercise_type, record.duration, record.intensity,
                  record.calories_burned, record.notes, record.date, record.created_at))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating exercise record: {e}")
            return False
    
    def get_exercise_records_by_user(self, user_id: int) -> List[ExerciseRecord]:
        """Get all exercise records for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("""
                SELECT * FROM exercise 
                WHERE user_id = ? 
                ORDER BY date DESC
            """, (user_id,))
            rows = c.fetchall()
            conn.close()
            
            return [ExerciseRecord(
                id=row['id'],
                user_id=row['user_id'],
                exercise_type=row['exercise_type'],
                duration=row['duration'],
                intensity=row['intensity'],
                calories_burned=row['calories_burned'],
                notes=row['notes'],
                date=row['date'],
                created_at=row['created_at']
            ) for row in rows]
        except Exception as e:
            print(f"Error getting exercise records: {e}")
            return []
    
    def update_exercise_record(self, record: ExerciseRecord) -> bool:
        """Update an exercise record"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                UPDATE exercise 
                SET exercise_type = ?, duration = ?, intensity = ?, calories_burned = ?, notes = ?, date = ?
                WHERE id = ?
            """, (record.exercise_type, record.duration, record.intensity, record.calories_burned,
                  record.notes, record.date, record.id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating exercise record: {e}")
            return False
    
    def delete_exercise_record(self, record_id: int) -> bool:
        """Delete an exercise record"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("DELETE FROM exercise WHERE id = ?", (record_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting exercise record: {e}")
            return False
    
    # Diet Record Methods
    def create_diet_record(self, record: DietRecord) -> bool:
        """Create a new diet record"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                INSERT INTO diet (user_id, food_name, meal_type, portion_size, calories, notes, date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (record.user_id, record.food_name, record.meal_type, record.portion_size,
                  record.calories, record.notes, record.date, record.created_at))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating diet record: {e}")
            return False
    
    def get_diet_records_by_user(self, user_id: int) -> List[DietRecord]:
        """Get all diet records for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("""
                SELECT * FROM diet 
                WHERE user_id = ? 
                ORDER BY date DESC
            """, (user_id,))
            rows = c.fetchall()
            conn.close()
            
            return [DietRecord(
                id=row['id'],
                user_id=row['user_id'],
                food_name=row['food_name'],
                meal_type=row['meal_type'],
                portion_size=row['portion_size'],
                calories=row['calories'],
                notes=row['notes'],
                date=row['date'],
                created_at=row['created_at']
            ) for row in rows]
        except Exception as e:
            print(f"Error getting diet records: {e}")
            return []
    
    def update_diet_record(self, record: DietRecord) -> bool:
        """Update a diet record"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                UPDATE diet 
                SET food_name = ?, meal_type = ?, portion_size = ?, calories = ?, notes = ?, date = ?
                WHERE id = ?
            """, (record.food_name, record.meal_type, record.portion_size, record.calories,
                  record.notes, record.date, record.id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating diet record: {e}")
            return False
    
    def delete_diet_record(self, record_id: int) -> bool:
        """Delete a diet record"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("DELETE FROM diet WHERE id = ?", (record_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting diet record: {e}")
            return False