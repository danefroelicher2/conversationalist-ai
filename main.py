import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from services.audio_service import AudioService
from services.database_service import DatabaseService
from services.llm_service import LLMService
from services.tts_service import TTSService

def main():
    print("=" * 50)
    print("🎤 CONVERSATIONALIST AI - Voice Recognition System")
    print("=" * 50)
    print()

    # Initialize servicess
    audio = AudioService()
    db = DatabaseService()
    llm = LLMService()
    tts = TTSService()

    print("👋 Hello! I'm your AI security assistant.")
    print("📝 I learn who you are by your voice.")
    print()
    print("Please tell me your name when ready...")
    input("Press ENTER to start recording (5 seconds)...\n")

    # Record and transcribe with error handling
    max_attempts = 3
    result = None

    for attempt in range(1, max_attempts + 1):
        try:
            result = audio.record_and_transcribe(duration=5)
            name = result['text'].strip()

            # Validate that we got actual text
            if not name or len(name) < 2:
                print(f"⚠️ Transcription unclear (attempt {attempt}/{max_attempts})")
                if attempt < max_attempts:
                    print("Let's try again. Please speak more clearly...")
                    input("Press ENTER to retry...")
                    continue
                else:
                    print("❌ Could not understand audio after 3 attempts")
                    print("Please check your microphone and try running the program again")
                    audio.cleanup()
                    db.close()
                    return

            # Success - we have a valid name
            break

        except Exception as e:
            print(f"❌ Error during recording/transcription: {e}")
            if attempt < max_attempts:
                print(f"Retrying... (attempt {attempt + 1}/{max_attempts})")
                input("Press ENTER to retry...")
            else:
                print("❌ Failed after 3 attempts")
                audio.cleanup()
                db.close()
                return

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

    # Generate intelligent response using LLM
    print("\n🤖 Thinking...")

    # Build context from past conversations
    past_conversations = db.get_user_conversations(user_id, limit=5)
    context_info = ""
    if past_conversations and len(past_conversations) > 1:
        context_info = "\n\nPrevious conversations:\n"
        for conv in past_conversations[:3]:
            context_info += f"- {conv['timestamp'].strftime('%Y-%m-%d %H:%M')}: User said '{conv['user_input']}'\n"

    # Create system prompt with context
    system_prompt = f"""You are Dane's personal AI desk assistant.

USER INFO:
- Name: {name}
- Status: {"Returning user" if user else "New user"}
- Last seen: {user.get('last_seen').strftime('%Y-%m-%d %H:%M') if user and user.get('last_seen') else "First time"}
{context_info}

PERSONALITY:
- Friendly and natural
- Concise responses (2-3 sentences max)
- Remember context from past conversations
- Be helpful and conversational

The user just said: "{name}"
Respond naturally as their AI assistant."""

    # Build conversation for LLM
    conversation_history = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': name}
    ]

    # Get intelligent response
    ai_response = llm.generate_response(name, conversation_history)

    print(f"💬 AI Response: {ai_response}\n")

    # Speak the response
    tts.speak(ai_response)

    # Store conversation
    conv_id = db.create_conversation(
        user_id=user_id,
        user_input=name,
        ai_response=ai_response,
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
    tts.cleanup()
    audio.cleanup()
    db.close()

if __name__ == "__main__":
    main()
