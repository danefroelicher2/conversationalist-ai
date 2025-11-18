import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, List
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from config.config import config

class DatabaseService:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=config.DB_HOST,
                port=config.DB_PORT,
                database=config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASSWORD
            )
            print("✅ Database connected")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise

    def execute_sql_file(self, sql_file_path: str):
        try:
            with open(sql_file_path, 'r') as f:
                sql = f.read()
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            cur.close()
            print(f"✅ Executed {sql_file_path}")
        except Exception as e:
            print(f"❌ Failed to execute SQL: {e}")
            self.conn.rollback()
            raise

    def update_user_last_seen(self, user_id: int):
        """Update the last_seen timestamp for a user.

        Args:
            user_id: Integer ID of the user
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                "UPDATE users SET last_seen = %s WHERE user_id = %s",
                (datetime.now(), user_id)
            )
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"❌ Failed to update last_seen: {e}")
            self.conn.rollback()

    def create_conversation(self, user_id: int, user_input: str, ai_response: str = None, audio_path: str = None) -> str:
        """Create a new conversation record.

        Args:
            user_id: Integer ID of the user
            user_input: User's input text
            ai_response: AI's response text (optional)
            audio_path: Path to audio file (optional)

        Returns:
            String representation of the conversation ID
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO conversations (user_id, timestamp, user_input, ai_response, audio_path) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (user_id, datetime.now(), user_input, ai_response, audio_path)
            )
            conv_id = cur.fetchone()[0]
            self.conn.commit()
            cur.close()
            return str(conv_id)
        except Exception as e:
            print(f"❌ Failed to create conversation: {e}")
            self.conn.rollback()
            raise

    def get_user_conversations(self, user_id: int, limit: int = 10):
        """Get conversation history for a user.

        Args:
            user_id: Integer ID of the user
            limit: Maximum number of conversations to return (default: 10)

        Returns:
            List of conversation dictionaries
        """
        try:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(
                "SELECT * FROM conversations WHERE user_id = %s ORDER BY timestamp DESC LIMIT %s",
                (user_id, limit)
            )
            conversations = cur.fetchall()
            cur.close()
            return [dict(conv) for conv in conversations]
        except Exception as e:
            print(f"❌ Failed to get conversations: {e}")
            return []

    def close(self):
        if self.conn:
            self.conn.close()
