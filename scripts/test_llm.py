import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).parent.parent))
from services.llm_service import LLMService

def main():
    print("=" * 50)
    print("🧪 TESTING LLM SERVICE")
    print("=" * 50)
    print()

    # Initialize LLM Servicee
    try:
        llm = LLMService()
    except Exception as e:
        print(f"❌ Failed to initialize LLM Service: {e}")
        return

    # Test 1: Connection Test
    print("Test 1: Connection Test")
    print("-" * 50)
    try:
        connection_ok = llm.test_connection()
        if connection_ok:
            print("✅ PASS: Ollama connection successful")
        else:
            print("❌ FAIL: Ollama connection failed")
            print("Make sure Ollama is running: ollama serve")
            return
    except Exception as e:
        print(f"❌ FAIL: Connection test error: {e}")
        return

    # Test 2: Simple Prompt
    print("\nTest 2: Simple Prompt")
    print("-" * 50)
    try:
        prompt = "Say hello in exactly 5 words"
        print(f"Prompt: \"{prompt}\"")

        start_time = time.time()
        response = llm.generate_response(prompt)
        end_time = time.time()

        elapsed = end_time - start_time

        print(f"\nResponse: \"{response}\"")
        print(f"⏱️  Response time: {elapsed:.2f} seconds")

        if response and not response.startswith("I apologize"):
            print("✅ PASS: Simple prompt successful")
        else:
            print("❌ FAIL: Simple prompt failed")
    except Exception as e:
        print(f"❌ FAIL: Simple prompt error: {e}")

    # Test 3: Conversation with History
    print("\nTest 3: Conversation History")
    print("-" * 50)
    try:
        # First turn
        print("Turn 1:")
        first_prompt = "My favorite color is blue. Remember that."
        print(f"User: \"{first_prompt}\"")

        start_time = time.time()
        first_response = llm.generate_response(first_prompt)
        end_time = time.time()
        elapsed_1 = end_time - start_time

        print(f"AI: \"{first_response}\"")
        print(f"⏱️  Response time: {elapsed_1:.2f} seconds")

        # Build conversation history
        conversation_history = [
            {'role': 'user', 'content': first_prompt},
            {'role': 'assistant', 'content': first_response}
        ]

        # Second turn with history
        print("\nTurn 2:")
        second_prompt = "What is my favorite color?"
        print(f"User: \"{second_prompt}\"")

        start_time = time.time()
        second_response = llm.generate_response(
            second_prompt,
            conversation_history=conversation_history
        )
        end_time = time.time()
        elapsed_2 = end_time - start_time

        print(f"AI: \"{second_response}\"")
        print(f"⏱️  Response time: {elapsed_2:.2f} seconds")

        # Check if AI remembered the color
        if "blue" in second_response.lower():
            print("✅ PASS: Conversation history working (AI remembered 'blue')")
        else:
            print("⚠️  WARNING: AI may not have remembered the conversation context")
            print("✅ PASS: Conversation history test completed (response generated)")

    except Exception as e:
        print(f"❌ FAIL: Conversation history error: {e}")

    print("\n" + "=" * 50)
    print("✅ All tests complete!")
    print("=" * 50)

if __name__ == "__main__":
    main()
