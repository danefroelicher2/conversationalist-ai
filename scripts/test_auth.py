import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from services.auth_service import AuthService

def main():
    print("=" * 50)
    print("🔐 TESTING AUTH SERVICE")
    print("=" * 50)
    print()

    auth = AuthService()

    # Test 1: Register new user
    print("Test 1: Register New User")
    print("-" * 50)
    user_id = 1234
    password = "blue sky mountain"
    
    success = auth.register_user(user_id, password)
    if success:
        print(f"✅ PASS: User {user_id} registered")
    else:
        print(f"❌ FAIL: Could not register user {user_id}")
    print()

    # Test 2: Try to register same user again (should fail)
    print("Test 2: Prevent Duplicate Registration")
    print("-" * 50)
    success = auth.register_user(user_id, "different password")
    if not success:
        print(f"✅ PASS: Duplicate registration blocked")
    else:
        print(f"❌ FAIL: Duplicate registration allowed (BAD)")
    print()

    # Test 3: Verify correct password
    print("Test 3: Login with Correct Password")
    print("-" * 50)
    verified = auth.verify_user(user_id, password)
    if verified:
        print(f"✅ PASS: Correct password accepted")
    else:
        print(f"❌ FAIL: Correct password rejected")
    print()

    # Test 4: Verify incorrect password
    print("Test 4: Reject Incorrect Password")
    print("-" * 50)
    verified = auth.verify_user(user_id, "wrong password")
    if not verified:
        print(f"✅ PASS: Incorrect password rejected")
    else:
        print(f"❌ FAIL: Incorrect password accepted (BAD)")
    print()

    # Test 5: Case insensitivity
    print("Test 5: Password Normalization (Case Insensitivity)")
    print("-" * 50)
    verified = auth.verify_user(user_id, "BLUE SKY MOUNTAIN")
    if verified:
        print(f"✅ PASS: Uppercase password accepted (normalized)")
    else:
        print(f"❌ FAIL: Normalization not working")
    print()

    # Test 6: Get user info
    print("Test 6: Retrieve User Info")
    print("-" * 50)
    user_info = auth.get_user_info(user_id)
    if user_info:
        print(f"✅ PASS: User info retrieved")
        print(f"   User ID: {user_info['user_id']}")
        print(f"   Created: {user_info['created_at']}")
        print(f"   Last Seen: {user_info['last_seen']}")
    else:
        print(f"❌ FAIL: Could not retrieve user info")
    print()

    # Test 7: Check non-existent user
    print("Test 7: Non-Existent User")
    print("-" * 50)
    exists = auth.user_exists(9999)
    if not exists:
        print(f"✅ PASS: Non-existent user correctly identified")
    else:
        print(f"❌ FAIL: Non-existent user reported as existing")
    print()

    print("=" * 50)
    print("✅ All tests complete!")
    print("=" * 50)

    auth.close()

if __name__ == "__main__":
    main()