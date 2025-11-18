import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from services.conversation_service import parse_user_id, is_exit_command, build_conversation_history
from services.database_service import DatabaseService


def test_parse_user_id():
    """Test user ID parsing from various transcription formats"""
    print("=" * 50)
    print("TEST: parse_user_id()")
    print("=" * 50)

    test_cases = [
        ("1234", 1234, "Direct digits"),
        ("5678", 5678, "Direct digits"),
        ("one two three four", 1234, "Spelled out"),
        ("five six seven eight", 5678, "Spelled out"),
        ("12 34", 1234, "Digits with space"),
        ("one two 3 four", 1234, "Mixed"),
        ("for five six seven", 4567, "Homophones"),
        ("invalid", None, "Invalid input"),
        ("123", None, "Too short"),
        ("12345", None, "Too long"),
    ]

    passed = 0
    failed = 0

    for input_text, expected, description in test_cases:
        result = parse_user_id(input_text)
        status = "✅ PASS" if result == expected else "❌ FAIL"

        if result == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status} | {description}")
        print(f"  Input: '{input_text}'")
        print(f"  Expected: {expected}, Got: {result}")
        print()

    print(f"Results: {passed} passed, {failed} failed")
    print()


def test_is_exit_command():
    """Test exit command detection"""
    print("=" * 50)
    print("TEST: is_exit_command()")
    print("=" * 50)

    test_cases = [
        ("goodbye", True, "Simple goodbye"),
        ("Goodbye!", True, "Goodbye with punctuation"),
        ("exit", True, "Exit command"),
        ("quit", True, "Quit command"),
        ("I want to logout", True, "Contains logout"),
        ("stop", True, "Stop command"),
        ("Hello", False, "Normal greeting"),
        ("What's the weather?", False, "Normal question"),
        ("Bye bye", True, "Contains bye"),
    ]

    passed = 0
    failed = 0

    for input_text, expected, description in test_cases:
        result = is_exit_command(input_text)
        status = "✅ PASS" if result == expected else "❌ FAIL"

        if result == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status} | {description}")
        print(f"  Input: '{input_text}'")
        print(f"  Expected: {expected}, Got: {result}")
        print()

    print(f"Results: {passed} passed, {failed} failed")
    print()


def test_build_conversation_history():
    """Test conversation history building"""
    print("=" * 50)
    print("TEST: build_conversation_history()")
    print("=" * 50)

    # This test requires database access
    db = DatabaseService()

    # Use test user 1234 (created in auth tests)
    user_id = 1234
    current_input = "What did we talk about before?"

    try:
        messages = build_conversation_history(db, user_id, current_input)

        print(f"✅ Successfully built conversation history")
        print(f"   Total messages: {len(messages)}")
        print(f"   System prompt present: {messages[0]['role'] == 'system'}")
        print(f"   Current input added: {messages[-1]['content'] == current_input}")
        print()

        # Show first few messages
        print("First 3 messages:")
        for i, msg in enumerate(messages[:3]):
            preview = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
            print(f"  [{i}] {msg['role']}: {preview}")
        print()

    except Exception as e:
        print(f"❌ FAIL: {e}")
    finally:
        db.close()


def main():
    print("\n")
    print("🧪 TESTING CONVERSATION SERVICE")
    print("=" * 50)
    print()

    # Run tests
    test_parse_user_id()
    test_is_exit_command()
    test_build_conversation_history()

    print("=" * 50)
    print("✅ All conversation service tests complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
