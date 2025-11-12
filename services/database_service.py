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

    def create_user(self, name: str) -> str:
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO users (name, created_at, last_seen) VALUES (%s, %s, %s) RETURNING id",
                (name, datetime.now(), datetime.now())
            )
            user_id = cur.fetchone()[0]
            self.conn.commit()
            cur.close()
            return str(user_id)
        except Exception as e:
            print(f"❌ Failed to create user: {e}")
            self.conn.rollback()
            raise

    def get_user_by_name(self, name: str) -> Optional[Dict]:
        try:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM users WHERE name ILIKE %s", (name,))
            user = cur.fetchone()
            cur.close()
            return dict(user) if user else None
        except Exception as e:
            print(f"❌ Failed to get user: {e}")
            return None

    def create_conversation(self, user_id: str, user_input: str, ai_response: str = None) -> str:
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO conversations (user_id, timestamp, user_input, ai_response) VALUES (%s, %s, %s, %s) RETURNING id",
                (user_id, datetime.now(), user_input, ai_response)
            )
            conv_id = cur.fetchone()[0]
            self.conn.commit()
            cur.close()
            return str(conv_id)
        except Exception as e:
            print(f"❌ Failed to create conversation: {e}")
            self.conn.rollback()
            raise

    def close(self):
        if self.conn:
            self.conn.close()
