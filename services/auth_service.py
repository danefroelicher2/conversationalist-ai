import bcrypt
import sys
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))
from services.database_service import DatabaseService

class AuthService:
    def __init__(self):
        """Initialize authentication service"""
        self.db = DatabaseService()
        print("🔐 Auth Service initialized")

    def _hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt
        
        Args:
            password: Plain text password (will be normalized)
        
        Returns:
            Hashed password as string
        """
        # Normalize: lowercase, strip whitespace
        normalized = password.lower().strip()
        
        # Convert to bytes and hash
        password_bytes = normalized.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        return hashed.decode('utf-8')

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash
        
        Args:
            password: Plain text password attempt
            password_hash: Stored bcrypt hash
        
        Returns:
            True if password matches, False otherwise
        """
        # Normalize the same way
        normalized = password.lower().strip()
        password_bytes = normalized.encode('utf-8')
        hash_bytes = password_hash.encode('utf-8')
        
        return bcrypt.checkpw(password_bytes, hash_bytes)

    def user_exists(self, user_id: int) -> bool:
        """
        Check if a user ID exists in the database
        
        Args:
            user_id: 4-digit user ID
        
        Returns:
            True if user exists, False otherwise
        """
        try:
            cur = self.db.conn.cursor()
            cur.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
            result = cur.fetchone()
            cur.close()
            return result is not None
        except Exception as e:
            print(f"❌ Error checking user existence: {e}")
            return False

    def register_user(self, user_id: int, password: str) -> bool:
        """
        Register a new user with ID and password
        
        Args:
            user_id: 4-digit user ID
            password: Plain text password (will be hashed)
        
        Returns:
            True if registration successful, False if user already exists
        """
        try:
            # Check if user already exists
            if self.user_exists(user_id):
                print(f"⚠️  User {user_id} already exists")
                return False

            # Hash the password
            password_hash = self._hash_password(password)

            # Insert into database
            cur = self.db.conn.cursor()
            cur.execute(
                """
                INSERT INTO users (user_id, password_hash, created_at, last_seen, failed_attempts)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (user_id, password_hash, datetime.now(), datetime.now(), 0)
            )
            self.db.conn.commit()
            cur.close()

            print(f"✅ User {user_id} registered successfully")
            return True

        except Exception as e:
            print(f"❌ Error registering user: {e}")
            self.db.conn.rollback()
            return False

    def verify_user(self, user_id: int, password: str) -> bool:
        """
        Verify user credentials (login)
        
        Args:
            user_id: 4-digit user ID
            password: Plain text password attempt
        
        Returns:
            True if credentials are correct, False otherwise
        """
        try:
            # Get user from database
            cur = self.db.conn.cursor()
            cur.execute("SELECT password_hash FROM users WHERE user_id = %s", (user_id,))
            result = cur.fetchone()
            cur.close()

            if result is None:
                print(f"⚠️  User {user_id} not found")
                return False

            password_hash = result[0]

            # Verify password
            if self._verify_password(password, password_hash):
                print(f"✅ User {user_id} authenticated")
                
                # Update last_seen
                cur = self.db.conn.cursor()
                cur.execute(
                    "UPDATE users SET last_seen = %s WHERE user_id = %s",
                    (datetime.now(), user_id)
                )
                self.db.conn.commit()
                cur.close()
                
                return True
            else:
                print(f"❌ Invalid password for user {user_id}")
                return False

        except Exception as e:
            print(f"❌ Error verifying user: {e}")
            return False

    def get_user_info(self, user_id: int) -> Optional[Dict]:
        """
        Get user information
        
        Args:
            user_id: 4-digit user ID
        
        Returns:
            User dict or None if not found
        """
        try:
            from psycopg2.extras import RealDictCursor
            cur = self.db.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cur.fetchone()
            cur.close()
            return dict(user) if user else None
        except Exception as e:
            print(f"❌ Error getting user info: {e}")
            return None

    def close(self):
        """Close database connection"""
        self.db.close()