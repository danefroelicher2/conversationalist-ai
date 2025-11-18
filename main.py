import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from services.audio_service import AudioService
from services.database_service import DatabaseService
from services.auth_service import AuthService
from services.llm_service import LLMService
from services.tts_service import TTSService
from services.conversation_service import parse_user_id, is_exit_command, build_conversation_history


def authenticate_user(audio: AudioService, db: DatabaseService, auth: AuthService, tts: TTSService) -> int:
    """
    Handle user authentication flow (new or existing user)

    Returns:
        user_id (int) on success, None on failure
    """
    print("\n" + "=" * 50)
    print("🔐 AUTHENTICATION")
    print("=" * 50)

    # Step 1: Get user ID
    max_attempts = 3
    user_id = None

    for attempt in range(1, max_attempts + 1):
        tts.speak("Please state your four digit user I D")
        print("\n🎤 Listening for user ID...")
        input("Press ENTER when ready to speak your user ID (5 seconds)...")

        result = audio.record_and_transcribe(duration=5)
        transcription = result['text']

        print(f"📝 You said: '{transcription}'")

        # Parse user ID
        user_id = parse_user_id(transcription)

        if user_id:
            print(f"✅ Parsed user ID: {user_id}")
            break
        else:
            print(f"⚠️  Could not parse user ID (attempt {attempt}/{max_attempts})")
            if attempt < max_attempts:
                tts.speak("I didn't catch that. Please try again.")

    if not user_id:
        print("❌ Failed to get valid user ID after 3 attempts")
        tts.speak("Authentication failed. Goodbye.")
        return None

    # Step 2: Check if user exists
    user_exists = auth.user_exists(user_id)

    if user_exists:
        # Existing user - login flow
        print(f"\n👤 User {user_id} found. Verifying password...")
        tts.speak(f"User {user_id} found. Please state your password.")

        # Allow unlimited password attempts (as requested)
        while True:
            print("\n🎤 Listening for password...")
            input("Press ENTER when ready to speak your password (5 seconds)...")

            result = audio.record_and_transcribe(duration=5)
            password = result['text'].strip()

            if not password:
                print("⚠️  No password detected. Try again.")
                tts.speak("I didn't hear anything. Please try again.")
                continue

            print(f"📝 Verifying password...")

            # Verify password
            if auth.verify_user(user_id, password):
                print(f"✅ Authentication successful!")
                tts.speak(f"Welcome back, User {user_id}.")
                return user_id
            else:
                print(f"❌ Incorrect password")
                tts.speak("Incorrect password. Please try again.")

    else:
        # New user - registration flow
        print(f"\n🆕 User {user_id} not found. Creating new account...")
        tts.speak(f"User {user_id} is new. Please create a password.")

        print("\n🎤 Listening for password...")
        input("Press ENTER when ready to speak your password (5 seconds)...")

        result = audio.record_and_transcribe(duration=5)
        password = result['text'].strip()

        if not password:
            print("❌ No password detected. Registration failed.")
            tts.speak("Password creation failed. Goodbye.")
            return None

        print(f"📝 Password received: '{password}'")

        # Register user
        if auth.register_user(user_id, password):
            print(f"✅ Account created successfully!")
            tts.speak(f"Account created. Welcome, User {user_id}.")
            return user_id
        else:
            print(f"❌ Registration failed")
            tts.speak("Registration failed. Goodbye.")
            return None


def conversation_session(user_id: int, audio: AudioService, db: DatabaseService, llm: LLMService, tts: TTSService):
    """
    Run multi-turn conversation loop after authentication

    Args:
        user_id: Authenticated user's ID
        audio: Audio service for recording
        db: Database service for storing conversations
        llm: LLM service for generating responses
        tts: TTS service for speaking responses
    """
    print("\n" + "=" * 50)
    print(f"💬 CONVERSATION SESSION - User {user_id}")
    print("=" * 50)
    print("\n💡 Say 'goodbye', 'exit', or 'quit' to end the session\n")

    tts.speak("How can I help you?")

    # Conversation loop
    while True:
        print("\n🎤 Listening...")
        input("Press ENTER when ready to speak (5 seconds)...")

        # Record and transcribe user input
        result = audio.record_and_transcribe(duration=5)
        user_input = result['text'].strip()
        audio_path = result['audio_path']

        if not user_input:
            print("⚠️  No input detected. Try again.")
            tts.speak("I didn't hear anything. Please try again.")
            continue

        print(f"💬 You: {user_input}")

        # Check for exit command
        if is_exit_command(user_input):
            print(f"\n👋 User {user_id} logged out")
            tts.speak(f"Goodbye, User {user_id}.")
            break

        # Build conversation history with full context
        print("🤖 Generating response...")
        conversation_history = build_conversation_history(db, user_id, user_input)

        # Generate AI response
        ai_response = llm.generate_response(user_input, conversation_history)

        print(f"🤖 AI: {ai_response}\n")

        # Speak response
        tts.speak(ai_response)

        # Save conversation to database
        try:
            conv_id = db.create_conversation(
                user_id=user_id,
                user_input=user_input,
                ai_response=ai_response,
                audio_path=audio_path
            )
            print(f"💾 Conversation saved (ID: {conv_id})")
        except Exception as e:
            print(f"⚠️  Failed to save conversation: {e}")


def main():
    print("=" * 50)
    print("🎤 CONVERSATIONALIST AI")
    print("=" * 50)
    print()

    # Initialize all services
    print("🔧 Initializing services...")
    audio = AudioService()
    db = DatabaseService()
    auth = AuthService()
    llm = LLMService()
    tts = TTSService()
    print("✅ All services initialized\n")

    # Authentication phase
    user_id = authenticate_user(audio, db, auth, tts)

    if not user_id:
        print("\n❌ Authentication failed. Exiting.")
        # Cleanup
        tts.cleanup()
        audio.cleanup()
        auth.close()
        db.close()
        return

    # Conversation phase
    conversation_session(user_id, audio, db, llm, tts)

    # Cleanup
    print("\n🧹 Cleaning up...")
    tts.cleanup()
    audio.cleanup()
    auth.close()
    db.close()

    print("\n" + "=" * 50)
    print("✅ Session complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
