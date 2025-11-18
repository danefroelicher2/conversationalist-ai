CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_seen TIMESTAMP,
    voice_embedding BYTEA,
    face_embedding BYTEA,
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    timestamp TIMESTAMP DEFAULT NOW(),
    location VARCHAR(100),
    trigger_type VARCHAR(50),
    user_input TEXT,
    ai_response TEXT,
    audio_path TEXT,
    video_file_path TEXT,
    metadata JSONB DEFAULT '{}'
);

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

CREATE INDEX IF NOT EXISTS idx_users_name ON users(name);
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
