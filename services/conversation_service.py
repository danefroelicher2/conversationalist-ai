import sys
from pathlib import Path
from typing import Optional, List, Dict

sys.path.append(str(Path(__file__).parent.parent))
from services.database_service import DatabaseService


def parse_user_id(transcription: str) -> Optional[int]:
    """
    Convert transcribed speech to 4-digit user ID integer

    Handles multiple formats:
    - Direct digits: "1234" → 1234
    - Spelled out: "one two three four" → 1234
    - Mixed: "12 thirty four" → 1234

    Args:
        transcription: Text from Whisper transcription

    Returns:
        4-digit integer user ID, or None if parsing fails
    """
    # Strip whitespace and lowercase
    text = transcription.lower().strip()

    # Try direct conversion first
    try:
        user_id = int(text)
        if 1000 <= user_id <= 9999:  # Valid 4-digit range
            return user_id
    except ValueError:
        pass

    # Map words to digits (common speech-to-text variations)
    word_to_digit = {
        'zero': '0', 'oh': '0',
        'one': '1', 'won': '1',
        'two': '2', 'to': '2', 'too': '2',
        'three': '3', 'tree': '3',
        'four': '4', 'for': '4', 'fore': '4',
        'five': '5',
        'six': '6', 'sicks': '6',
        'seven': '7',
        'eight': '8', 'ate': '8',
        'nine': '9', 'niner': '9'
    }

    # Replace words with digits
    for word, digit in word_to_digit.items():
        text = text.replace(word, digit)

    # Remove spaces and non-digits
    digits_only = ''.join(c for c in text if c.isdigit())

    # Try conversion again
    try:
        user_id = int(digits_only)
        if 1000 <= user_id <= 9999:
            return user_id
    except ValueError:
        pass

    return None  # Could not parse


def is_exit_command(text: str) -> bool:
    """
    Check if user wants to exit the conversation

    Args:
        text: Transcribed user input

    Returns:
        True if exit command detected, False otherwise
    """
    exit_keywords = ['goodbye', 'exit', 'quit', 'stop', 'logout', 'bye']
    text_lower = text.lower().strip()

    return any(keyword in text_lower for keyword in exit_keywords)


def build_conversation_history(db: DatabaseService, user_id: int, current_input: str) -> List[Dict]:
    """
    Build full conversation history for LLM context

    Loads all past conversations for the user and formats them
    as a message list suitable for Ollama chat API

    Args:
        db: Database service instance
        user_id: Integer user ID
        current_input: The user's current message

    Returns:
        List of message dicts with 'role' and 'content' keys
    """
    # System prompt
    system_prompt = f"""You are an intelligent AI desk assistant for User {user_id}.

CAPABILITIES:
- Remember all past conversations with this user
- Provide helpful, conversational responses
- Keep responses concise (2-3 sentences unless more detail is requested)
- Be friendly and natural

PERSONALITY:
- Professional but warm
- Attentive to context and patterns
- Proactive in offering help based on past interactions"""

    messages = [
        {'role': 'system', 'content': system_prompt}
    ]

    # Load past conversations (all of them, as requested)
    past_conversations = db.get_user_conversations(user_id, limit=1000)

    # Format past conversations (they come back newest-first, so reverse)
    past_conversations.reverse()

    for conv in past_conversations:
        # Add user input
        if conv.get('user_input'):
            messages.append({
                'role': 'user',
                'content': conv['user_input']
            })

        # Add AI response
        if conv.get('ai_response'):
            messages.append({
                'role': 'assistant',
                'content': conv['ai_response']
            })

    # Add current user input
    messages.append({
        'role': 'user',
        'content': current_input
    })

    return messages
