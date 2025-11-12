import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from services.database_service import DatabaseService

def main():
    print("Testing database connection...\n")
    db = DatabaseService()

    print("Test 1: Creating test user...")
    user_id = db.create_user("Dane")
    print(f"✅ Created user with ID: {user_id}\n")

    print("Test 2: Retrieving user...")
    user = db.get_user_by_name("Dane")
    print(f"✅ Found user: {user}\n")

    print("Test 3: Creating conversation...")
    conv_id = db.create_conversation(user_id, "Hello, system!", "Hi Dane!")
    print(f"✅ Created conversation with ID: {conv_id}\n")

    print("✅ All tests passed!")
    db.close()

if __name__ == "__main__":
    main()
