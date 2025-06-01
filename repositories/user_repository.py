import sqlite3
from typing import Optional, List
from interfaces.repositories import IUserRepository
from models.domain import User


class UserRepository(IUserRepository):
    """SQLite implementation of user repository"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def create_user(self, user: User) -> bool:
        """Create a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                INSERT INTO users (username, password, email, gender, birthday, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user.username, user.password, user.email, user.gender, 
                  user.birthday, user.created_at))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = c.fetchone()
            conn.close()
            
            if row:
                return User(
                    id=row['id'],
                    username=row['username'],
                    password=row['password'],
                    email=row['email'],
                    gender=row['gender'],
                    birthday=row['birthday'],
                    created_at=row['created_at']
                )
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = c.fetchone()
            conn.close()
            
            if row:
                return User(
                    id=row['id'],
                    username=row['username'],
                    password=row['password'],
                    email=row['email'],
                    gender=row['gender'],
                    birthday=row['birthday'],
                    created_at=row['created_at']
                )
            return None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    def update_user(self, user: User) -> bool:
        """Update user information"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                UPDATE users 
                SET username = ?, email = ?, gender = ?, birthday = ?
                WHERE id = ?
            """, (user.username, user.email, user.gender, user.birthday, user.id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
    
    def get_all_users(self) -> List[User]:
        """Get all users"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM users")
            rows = c.fetchall()
            conn.close()
            
            return [User(
                id=row['id'],
                username=row['username'],
                password=row['password'],
                email=row['email'],
                gender=row['gender'],
                birthday=row['birthday'],
                created_at=row['created_at']
            ) for row in rows]
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []