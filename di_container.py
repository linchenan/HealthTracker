"""
Dependency Injection Container
Implements Dependency Inversion Principle (DIP)
"""
from typing import Dict, Any

# Repository imports
from repositories.user_repository import UserRepository
from repositories.health_data_repository import HealthDataRepository
from repositories.medical_repository import MedicalRepository
from repositories.lifestyle_repository import LifestyleRepository

# Service imports
from services.authentication_service import AuthenticationService
from services.health_evaluation_service import HealthEvaluationService
from services.calorie_calculation_service import CalorieCalculationService
from services.notification_service import NotificationService


class DIContainer:
    """Dependency Injection Container"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._repositories = {}
        self._services = {}
        self._initialize_dependencies()
    
    def _initialize_dependencies(self):
        """Initialize all dependencies"""
        # Initialize repositories
        self._repositories['user'] = UserRepository(self.db_path)
        self._repositories['health_data'] = HealthDataRepository(self.db_path)
        self._repositories['medical'] = MedicalRepository(self.db_path)
        self._repositories['lifestyle'] = LifestyleRepository(self.db_path)
        
        # Initialize services with repository dependencies
        self._services['auth'] = AuthenticationService(self._repositories['user'])
        self._services['health'] = HealthEvaluationService(
            self._repositories['user'], 
            self._repositories['health_data']
        )
        self._services['calorie'] = CalorieCalculationService(
            self._repositories['lifestyle']
        )
        self._services['notification'] = NotificationService(
            self._repositories['user'],
            self._repositories['health_data'],
            self._repositories['medical']
        )
    
    def get_repository(self, name: str):
        """Get repository by name"""
        return self._repositories.get(name)
    
    def get_service(self, name: str):
        """Get service by name"""
        return self._services.get(name)
    
    def get_auth_service(self):
        """Get authentication service"""
        return self._services['auth']
    
    def get_health_service(self):
        """Get health evaluation service"""
        return self._services['health']
    
    def get_calorie_service(self):
        """Get calorie calculation service"""
        return self._services['calorie']
    
    def get_notification_service(self):
        """Get notification service"""
        return self._services['notification']


# Global container instance
_container = None


def initialize_container(db_path: str):
    """Initialize the global DI container"""
    global _container
    _container = DIContainer(db_path)


def get_container() -> DIContainer:
    """Get the global DI container"""
    if _container is None:
        raise RuntimeError("Container not initialized. Call initialize_container() first.")
    return _container


def get_auth_service():
    """Get authentication service from container"""
    return get_container().get_auth_service()


def get_health_service():
    """Get health evaluation service from container"""
    return get_container().get_health_service()


def get_calorie_service():
    """Get calorie calculation service from container"""
    return get_container().get_calorie_service()


def get_notification_service():
    """Get notification service from container"""
    return get_container().get_notification_service()


def get_repository(name: str):
    """Get repository by name from container"""
    return get_container().get_repository(name)


def get_service(name: str):
    """Get service by name from container"""
    return get_container().get_service(name)