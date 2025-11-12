import pyaudio
import wave
from pathlib import Path
from datetime import datetime
import sys
import whisper

sys.path.append(str(Path(__file__).parent.parent))
from config.config import config

class AudioService:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.audio = pyaudio.PyAudio()
        self.whisper_model = whisper.load_model("base")
        print("🎙️ Whisper model loaded")
        print("🎤 Audio service initialized")

    def record_audio(self, duration=5, filename=None):
        print(f"🔴 Recording for {duration} seconds...")

        stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        frames = []
        for i in range(0, int(self.RATE / self.CHUNK * duration)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_recording.wav"

        filepath = config.AUDIO_PATH / filename
        config.AUDIO_PATH.mkdir(parents=True, exist_ok=True)

        with wave.open(str(filepath), 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))

        print(f"✅ Audio saved: {filepath}")
        return str(filepath)

    def transcribe_audio(self, audio_path):
        print("🔄 Transcribing audio...")
        result = self.whisper_model.transcribe(audio_path)
        text = result['text'].strip()
        print(f"📝 Transcribed: {text}")
        return text

    def record_and_transcribe(self, duration=5):
        filepath = self.record_audio(duration)
        text = self.transcribe_audio(filepath)
        return {'audio_path': filepath, 'text': text}

    def cleanup(self):
        self.audio.terminate()
