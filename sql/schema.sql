CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_seen TIMESTAMP,
    failed_attempts INTEGER DEFAULT 0,
    voice_embedding BYTEA,
    face_embedding BYTEA,
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER REFERENCES users(user_id),
    timestamp TIMESTAMP DEFAULT NOW(),
    location VARCHAR(100),
    trigger_type VARCHAR(50),
    user_input TEXT,
    ai_response TEXT,
    audio_path TEXT,
    video_file_path TEXT,
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);
