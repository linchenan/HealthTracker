from abc import ABC, abstractmethod
from typing import List, Optional
from models.domain import User, BloodPressureRecord, HeightWeightRecord, MedicalRecord, Appointment, ExerciseRecord, DietRecord


class IUserRepository(ABC):
    """Interface for user repository operations"""
    
    @abstractmethod
    def create_user(self, user: User) -> bool:
        """Create a new user"""
        pass
    
    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass
    
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    def update_user(self, user: User) -> bool:
        """Update user information"""
        pass
    
    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID"""
        pass
    
    @abstractmethod
    def get_all_users(self) -> List[User]:
        """Get all users"""
        pass


class IHealthDataRepository(ABC):
    """Interface for health data repository operations"""
    
    # Blood Pressure Methods
    @abstractmethod
    def create_blood_pressure_record(self, record: BloodPressureRecord) -> bool:
        """Create a new blood pressure record"""
        pass
    
    @abstractmethod
    def get_blood_pressure_records_by_user(self, user_id: int) -> List[BloodPressureRecord]:
        """Get all blood pressure records for a user"""
        pass
    
    @abstractmethod
    def update_blood_pressure_record(self, record: BloodPressureRecord) -> bool:
        """Update a blood pressure record"""
        pass
    
    @abstractmethod
    def delete_blood_pressure_record(self, record_id: int) -> bool:
        """Delete a blood pressure record"""
        pass
    
    # Height Weight Methods
    @abstractmethod
    def create_height_weight_record(self, record: HeightWeightRecord) -> bool:
        """Create a new height/weight record"""
        pass
    
    @abstractmethod
    def get_height_weight_records_by_user(self, user_id: int) -> List[HeightWeightRecord]:
        """Get all height/weight records for a user"""
        pass
    
    @abstractmethod
    def update_height_weight_record(self, record: HeightWeightRecord) -> bool:
        """Update a height/weight record"""
        pass
    
    @abstractmethod
    def delete_height_weight_record(self, record_id: int) -> bool:
        """Delete a height/weight record"""
        pass


class IMedicalRepository(ABC):
    """Interface for medical repository operations"""
    
    # Medical Record Methods
    @abstractmethod
    def create_medical_record(self, record: MedicalRecord) -> bool:
        """Create a new medical record"""
        pass
    
    @abstractmethod
    def get_medical_records_by_user(self, user_id: int) -> List[MedicalRecord]:
        """Get all medical records for a user"""
        pass
    
    @abstractmethod
    def update_medical_record(self, record: MedicalRecord) -> bool:
        """Update a medical record"""
        pass
    
    @abstractmethod
    def delete_medical_record(self, record_id: int) -> bool:
        """Delete a medical record"""
        pass
    
    # Appointment Methods
    @abstractmethod
    def create_appointment(self, appointment: Appointment) -> bool:
        """Create a new appointment"""
        pass
    
    @abstractmethod
    def get_appointments_by_user(self, user_id: int) -> List[Appointment]:
        """Get all appointments for a user"""
        pass
    
    @abstractmethod
    def update_appointment(self, appointment: Appointment) -> bool:
        """Update an appointment"""
        pass
    
    @abstractmethod
    def delete_appointment(self, appointment_id: int) -> bool:
        """Delete an appointment"""
        pass


class ILifestyleRepository(ABC):
    """Interface for lifestyle repository operations"""
    
    # Exercise Record Methods
    @abstractmethod
    def create_exercise_record(self, record: ExerciseRecord) -> bool:
        """Create a new exercise record"""
        pass
    
    @abstractmethod
    def get_exercise_records_by_user(self, user_id: int) -> List[ExerciseRecord]:
        """Get all exercise records for a user"""
        pass
    
    @abstractmethod
    def update_exercise_record(self, record: ExerciseRecord) -> bool:
        """Update an exercise record"""
        pass
    
    @abstractmethod
    def delete_exercise_record(self, record_id: int) -> bool:
        """Delete an exercise record"""
        pass
    
    # Diet Record Methods
    @abstractmethod
    def create_diet_record(self, record: DietRecord) -> bool:
        """Create a new diet record"""
        pass
    
    @abstractmethod
    def get_diet_records_by_user(self, user_id: int) -> List[DietRecord]:
        """Get all diet records for a user"""
        pass
    
    @abstractmethod
    def update_diet_record(self, record: DietRecord) -> bool:
        """Update a diet record"""
        pass
    
    @abstractmethod
    def delete_diet_record(self, record_id: int) -> bool:
        """Delete a diet record"""
        pass