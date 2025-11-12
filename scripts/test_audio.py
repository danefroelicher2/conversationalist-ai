import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from services.audio_service import AudioService

def main():
    print("Testing audio recording + transcription...\n")

    audio = AudioService()

    print("Ready to record!")
    print("When you press ENTER, you'll have 5 seconds to speak.")
    print("Try saying: 'My name is Dane'\n")
    input("Press ENTER to start...")

    result = audio.record_and_transcribe(duration=5)

    print(f"\n✅ Recording complete!")
    print(f"📁 Audio saved: {result['audio_path']}")
    print(f"💬 You said: {result['text']}")

    audio.cleanup()

if __name__ == "__main__":
    main()
