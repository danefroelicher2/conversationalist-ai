import ollama
from typing import List, Dict, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

class LLMService:
    def __init__(self, model_name: str = "llama3.1:8b"):
        self.model_name = model_name
        print(f"🤖 LLM Service initialized with model: {model_name}")

    def generate_response(
        self,
        user_input: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Generate AI response using Ollama

        Args:
            user_input: The user's message
            conversation_history: List of previous messages with roles

        Returns:
            AI response as string
        """
        try:
            print("🤖 Generating response...")

            # Build messages list
            messages = []

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)

            # Add current user input
            messages.append({
                'role': 'user',
                'content': user_input
            })

            # Call Ollama API
            response = ollama.chat(
                model=self.model_name,
                messages=messages,
                options={
                    'temperature': 0.7
                }
            )

            # Extract response text
            ai_response = response['message']['content']
            print(f"✅ Response generated ({len(ai_response)} chars)")

            return ai_response

        except Exception as e:
            error_msg = f"❌ Error generating response: {str(e)}"
            print(error_msg)
            return f"I apologize, but I encountered an error: {str(e)}"

    def test_connection(self) -> bool:
        """Test if Ollama is accessible"""
        try:
            print("🔍 Testing Ollama connection...")

            # Simple test with ollama.generate
            ollama.generate(
                model=self.model_name,
                prompt="test"
            )

            print("✅ Ollama connection successful")
            return True

        except Exception as e:
            print(f"❌ Ollama connection failed: {str(e)}")
            return False
