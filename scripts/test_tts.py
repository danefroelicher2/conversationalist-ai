import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).parent.parent))
from services.tts_service import TTSService


def main():
    print("=" * 50)
    print("🔊 TESTING TTS SERVICE")
    print("=" * 50)
    print()

    # Initialize
    start_init = time.time()
    tts = TTSService()
    init_time = time.time() - start_init
    print(f"⏱️  Initialization time: {init_time:.3f}s")
    print()

    # Test 1: List voices
    print("Test 1: Available Voices")
    print("-" * 50)
    start = time.time()
    voices = tts.list_voices()
    elapsed = time.time() - start
    print(f"⏱️  Time: {elapsed:.3f}s")
    print(f"✅ Found {len(voices)} voice(s)")
    print()

    # Test 2: Short phrase
    print("Test 2: Short Phrase")
    print("-" * 50)
    test_phrase = "Hello, this is a test."
    start = time.time()
    tts.speak(test_phrase)
    elapsed = time.time() - start
    print(f"⏱️  Time: {elapsed:.3f}s")
    print(f"✅ Short phrase complete")
    print()

    # Test 3: Longer sentence
    print("Test 3: Natural Speech")
    print("-" * 50)
    test_sentence = "Nice to meet you! I'm your personal AI assistant. How can I help you today?"
    start = time.time()
    tts.speak(test_sentence)
    elapsed = time.time() - start
    print(f"⏱️  Time: {elapsed:.3f}s")
    print(f"✅ Natural speech complete")
    print()

    # Cleanup
    tts.cleanup()

    print("=" * 50)
    print("✅ All tests complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
