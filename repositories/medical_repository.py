import sqlite3
from typing import List, Optional
from interfaces.repositories import IMedicalRepository
from models.domain import MedicalRecord, Appointment


class MedicalRepository(IMedicalRepository):
    """SQLite implementation of medical repository"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    # Medical Record Methods
    def create_medical_record(self, record: MedicalRecord) -> bool:
        """Create a new medical record"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                INSERT INTO medical_records (user_id, record_type, description, doctor, hospital, date, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (record.user_id, record.record_type, record.description, record.doctor,
                  record.hospital, record.date, record.notes, record.created_at))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating medical record: {e}")
            return False
    
    def get_medical_records_by_user(self, user_id: int) -> List[MedicalRecord]:
        """Get all medical records for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("""
                SELECT * FROM medical_records 
                WHERE user_id = ? 
                ORDER BY date DESC
            """, (user_id,))
            rows = c.fetchall()
            conn.close()
            
            return [MedicalRecord(
                id=row['id'],
                user_id=row['user_id'],
                record_type=row['record_type'],
                description=row['description'],
                doctor=row['doctor'],
                hospital=row['hospital'],
                date=row['date'],
                notes=row['notes'],
                created_at=row['created_at']
            ) for row in rows]
        except Exception as e:
            print(f"Error getting medical records: {e}")
            return []
    
    def update_medical_record(self, record: MedicalRecord) -> bool:
        """Update a medical record"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                UPDATE medical_records 
                SET record_type = ?, description = ?, doctor = ?, hospital = ?, date = ?, notes = ?
                WHERE id = ?
            """, (record.record_type, record.description, record.doctor, record.hospital,
                  record.date, record.notes, record.id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating medical record: {e}")
            return False
    
    def delete_medical_record(self, record_id: int) -> bool:
        """Delete a medical record"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("DELETE FROM medical_records WHERE id = ?", (record_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting medical record: {e}")
            return False
    
    # Appointment Methods
    def create_appointment(self, appointment: Appointment) -> bool:
        """Create a new appointment"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                INSERT INTO appointments (user_id, doctor, hospital, appointment_date, appointment_time, purpose, notes, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (appointment.user_id, appointment.doctor, appointment.hospital, appointment.appointment_date,
                  appointment.appointment_time, appointment.purpose, appointment.notes, appointment.status, appointment.created_at))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating appointment: {e}")
            return False
    
    def get_appointments_by_user(self, user_id: int) -> List[Appointment]:
        """Get all appointments for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("""
                SELECT * FROM appointments 
                WHERE user_id = ? 
                ORDER BY appointment_date DESC, appointment_time DESC
            """, (user_id,))
            rows = c.fetchall()
            conn.close()
            
            return [Appointment(
                id=row['id'],
                user_id=row['user_id'],
                doctor=row['doctor'],
                hospital=row['hospital'],
                appointment_date=row['appointment_date'],
                appointment_time=row['appointment_time'],
                purpose=row['purpose'],
                notes=row['notes'],
                status=row['status'],
                created_at=row['created_at']
            ) for row in rows]
        except Exception as e:
            print(f"Error getting appointments: {e}")
            return []
    
    def update_appointment(self, appointment: Appointment) -> bool:
        """Update an appointment"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                UPDATE appointments 
                SET doctor = ?, hospital = ?, appointment_date = ?, appointment_time = ?, 
                    purpose = ?, notes = ?, status = ?
                WHERE id = ?
            """, (appointment.doctor, appointment.hospital, appointment.appointment_date, appointment.appointment_time,
                  appointment.purpose, appointment.notes, appointment.status, appointment.id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating appointment: {e}")
            return False
    
    def delete_appointment(self, appointment_id: int) -> bool:
        """Delete an appointment"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting appointment: {e}")
            return False