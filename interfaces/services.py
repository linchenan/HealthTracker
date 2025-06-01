from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, Tuple
from models.domain import User, BloodPressureRecord, HeightWeightRecord


class IAuthenticationService(ABC):
    """Interface for authentication service"""
    
    @abstractmethod
    def register_user(self, username: str, password: str, email: Optional[str] = None, 
                     gender: Optional[str] = None, birthday: Optional[str] = None) -> bool:
        """Register a new user"""
        pass
    
    @abstractmethod
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user login"""
        pass
    
    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        pass
    
    @abstractmethod
    def update_user_password(self, username: str, new_password: str) -> bool:
        """Update user's password (for password reset)"""
        pass


class IHealthEvaluationService(ABC):
    """Interface for health evaluation service"""
    
    @abstractmethod
    def calculate_bmi(self, height: float, weight: float) -> float:
        """Calculate BMI"""
        pass
    
    @abstractmethod
    def evaluate_bmi(self, bmi: float) -> str:
        """Evaluate BMI category"""
        pass
    
    @abstractmethod
    def evaluate_blood_pressure(self, systolic: int, diastolic: int) -> str:
        """Evaluate blood pressure category"""
        pass
    
    @abstractmethod
    def calculate_age(self, birthday: str) -> int:
        """Calculate age from birthday"""
        pass
    
    @abstractmethod
    def get_health_trends(self, user_id: int) -> Dict[str, Any]:
        """Get health trends for user"""
        pass
    
    @abstractmethod
    def get_health_summary(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive health summary"""
        pass
    
    @abstractmethod
    def get_user_profile(self, user_id: int) -> tuple:
        """Get user profile (gender, birthday)"""
        pass
    
    @abstractmethod
    def update_user_profile(self, user_id: int, gender: str, birthday: str) -> bool:
        """Update user profile"""
        pass


class ICalorieCalculationService(ABC):
    """Interface for calorie calculation service"""
    
    @abstractmethod
    def calculate_exercise_calories(self, exercise_type: str, duration: int, weight: float) -> int:
        """Calculate calories burned during exercise"""
        pass
    
    @abstractmethod
    def calculate_bmr(self, weight: float, height: float, age: int, gender: str) -> int:
        """Calculate Basal Metabolic Rate"""
        pass
    
    @abstractmethod
    def get_daily_calorie_recommendation(self, bmr: int, activity_level: str) -> int:
        """Get daily calorie recommendation"""
        pass


class INotificationService(ABC):
    """Interface for notification service"""
    
    @abstractmethod
    def send_health_reminder(self, user_id: int, message: str) -> bool:
        """Send health reminder to user"""
        pass
    
    @abstractmethod
    def send_appointment_reminder(self, user_id: int, appointment_details: Dict[str, Any]) -> bool:
        """Send appointment reminder"""
        pass
    
    @abstractmethod
    def check_health_alerts(self, user_id: int) -> List[str]:
        """Check for health alerts for user"""
        pass