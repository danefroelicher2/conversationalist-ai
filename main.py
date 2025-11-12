import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from services.audio_service import AudioService
from services.database_service import DatabaseService

def main():
    print("=" * 50)
    print("🎤 CONVERSATIONALIST AI - Voice Recognition System")
    print("=" * 50)
    print()

    # Initialize services
    audio = AudioService()
    db = DatabaseService()

    print("👋 Hello! I'm your AI security assistant.")
    print("📝 I learn who you are by your voice.")
    print()
    print("Please tell me your name when ready...")
    input("Press ENTER to start recording (5 seconds)...\n")

    # Record and transcribe
    result = audio.record_and_transcribe(duration=5)
    name = result['text'].strip()

    print(f"\n🔍 Checking if I know '{name}'...")

    # Check if user exists
    user = db.get_user_by_name(name)

    if user:
        # Existing user
        user_id = user['id']
        last_seen = user['last_seen']
        print(f"\n✅ Welcome back, {name}!")
        print(f"📅 Last seen: {last_seen}")
        db.update_user_last_seen(user_id)
    else:
        # New user
        user_id = db.create_user(name)
        print(f"\n🎉 Nice to meet you, {name}!")
        print(f"✅ I've created your profile (ID: {user_id})")

    # Store conversation
    conv_id = db.create_conversation(
        user_id=user_id,
        user_input=name,
        ai_response=f"Hello {name}!",
        audio_path=result['audio_path']
    )

    print(f"\n💾 Conversation saved (ID: {conv_id})")
    print(f"📁 Audio file: {result['audio_path']}")

    # Show user's conversation history
    conversations = db.get_user_conversations(user_id, limit=5)
    if len(conversations) > 1:
        print(f"\n📜 Your conversation history ({len(conversations)} total):")
        for conv in conversations[:3]:
            print(f"   - {conv['timestamp']}: '{conv['user_input']}'")

    print("\n" + "=" * 50)
    print("✅ Session complete!")
    print("=" * 50)

    # Cleanup
    audio.cleanup()
    db.close()

if __name__ == "__main__":
    main()
