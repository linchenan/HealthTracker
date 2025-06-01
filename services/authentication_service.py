"""
Authentication service implementation following SOLID principles
"""
import hashlib
from typing import Optional
from datetime import datetime
from interfaces.services import IAuthenticationService
from interfaces.repositories import IUserRepository
from models.domain import User


class AuthenticationService(IAuthenticationService):
    """Implementation of authentication service"""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, password: str, email: Optional[str] = None, 
                     gender: Optional[str] = None, birthday: Optional[str] = None) -> bool:
        """Register a new user"""
        try:
            # Check if user already exists
            existing_user = self.user_repository.get_user_by_username(username)
            if existing_user:
                return False
            
            # Hash password and create user
            password_hash = self.hash_password(password)
            user = User(
                username=username,
                password=password_hash,
                email=email,
                gender=gender,
                birthday=birthday,
                created_at=datetime.now().isoformat()
            )
            
            return self.user_repository.create_user(user)
        except Exception as e:
            print(f"Error registering user: {e}")
            return False
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user credentials"""
        try:
            user = self.user_repository.get_user_by_username(username)
            if not user:
                return None
            
            password_hash = self.hash_password(password)
            if user.password == password_hash:
                return user
            
            return None
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            return self.user_repository.get_user_by_username(username)
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None
        
    def update_user_password(self, username: str, new_password: str) -> bool:
        """Update user's password (for password reset)"""
        try:
            user = self.user_repository.get_user_by_username(username)
            if not user:
                return False
            password_hash = self.hash_password(new_password)
            # 直接更新密碼欄位
            import sqlite3
            conn = sqlite3.connect(self.user_repository.db_path)
            c = conn.cursor()
            c.execute("UPDATE users SET password=? WHERE username=?", (password_hash, username))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating user password: {e}")
            return False