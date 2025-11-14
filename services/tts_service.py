import pyttsx3
from typing import List
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


class TTSService:
    def __init__(self):
        """Initialize text-to-speech engine"""
        try:
            self.engine = pyttsx3.init()

            # Set properties
            self.engine.setProperty('rate', 165)  # Speed of speech
            self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

            print("🔊 TTS Service initialized")
        except Exception as e:
            print(f"❌ Error initializing TTS engine: {e}")
            raise

    def speak(self, text: str):
        """
        Convert text to speech and play it

        Args:
            text: The text to speak
        """
        try:
            if not text:
                print("⚠️  No text provided to speak")
                return

            # Show what we're speaking (first 50 chars)
            preview = text[:50] + "..." if len(text) > 50 else text
            print(f"🔊 Speaking: {preview}")

            self.engine.say(text)
            self.engine.runAndWait()

        except Exception as e:
            print(f"❌ Error speaking text: {e}")

    def list_voices(self) -> List:
        """
        List available voices

        Returns:
            List of available voice objects
        """
        try:
            voices = self.engine.getProperty('voices')
            print(f"\n📋 Available voices ({len(voices)}):")
            for idx, voice in enumerate(voices):
                print(f"  [{idx}] {voice.name} - {voice.id}")
            return voices
        except Exception as e:
            print(f"❌ Error listing voices: {e}")
            return []

    def set_voice(self, voice_index: int = 0):
        """
        Set voice by index

        Args:
            voice_index: Index of the voice to use (default: 0)
        """
        try:
            voices = self.engine.getProperty('voices')

            if 0 <= voice_index < len(voices):
                self.engine.setProperty('voice', voices[voice_index].id)
                print(f"✅ Voice set to: {voices[voice_index].name}")
            else:
                print(f"⚠️  Invalid voice index {voice_index}. Available: 0-{len(voices)-1}")

        except Exception as e:
            print(f"❌ Error setting voice: {e}")

    def cleanup(self):
        """Clean up TTS engine"""
        try:
            if hasattr(self, 'engine') and self.engine:
                self.engine.stop()
                print("🔇 TTS Service stopped")
        except Exception as e:
            print(f"❌ Error cleaning up TTS engine: {e}")


# Test code
if __name__ == "__main__":
    print("=== Testing TTS Service ===\n")

    # Initialize service
    tts = TTSService()

    # List available voices
    tts.list_voices()

    # Test speech
    print("\n--- Testing speech ---")
    tts.speak("Hello! This is a test of the text to speech service.")

    # Test with different voice (if available)
    print("\n--- Testing voice change ---")
    tts.set_voice(1)
    tts.speak("This is the second voice.")

    # Cleanup
    tts.cleanup()

    print("\n=== Test complete ===")
