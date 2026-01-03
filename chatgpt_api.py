"""
ChatGPT API Module
Handles communication with OpenAI's ChatGPT API (GPT-4o)
"""

import logging
from typing import List, Dict, Optional
from openai import OpenAI
from openai import APIError, APIConnectionError, RateLimitError
from config import Config

logger = logging.getLogger(__name__)


class ChatGPTClient:
    """
    Manages conversation with OpenAI's ChatGPT API.
    Maintains conversation history and handles API communication.
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        max_tokens: int = 500,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ):
        """
        Initialize ChatGPT client.
        
        Args:
            api_key: OpenAI API key
            model: Model identifier (gpt-4o, gpt-4o-mini, etc.)
            max_tokens: Maximum tokens in response
            temperature: Response randomness (0.0 to 2.0)
            system_prompt: System message to set assistant behavior
        """
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)
        
        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
        
        # Set system prompt
        if system_prompt:
            self.conversation_history.append({
                "role": "system",
                "content": system_prompt
            })
        
        logger.info(f"ChatGPT client initialized with model: {model}")
    
    def send_message(self, user_message: str) -> Optional[str]:
        """
        Send a message to ChatGPT and get response.
        
        Args:
            user_message: User's message text
        
        Returns:
            str: ChatGPT's response text, or None if request failed
        """
        if not user_message.strip():
            logger.warning("Empty message, skipping API call")
            return None
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        logger.info(f"📤 Sending to ChatGPT: '{user_message}'")
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                timeout=Config.CHATGPT_TIMEOUT
            )
            
            # Extract response text
            assistant_message = response.choices[0].message.content.strip()
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Trim history if too long
            self._trim_history()
            
            logger.info(f"📥 ChatGPT response: '{assistant_message}'")
            return assistant_message
            
        except RateLimitError as e:
            logger.error(f"Rate limit exceeded: {e}")
            return "I'm receiving too many requests right now. Please try again in a moment."
        
        except APIConnectionError as e:
            logger.error(f"Connection error: {e}")
            return "I'm having trouble connecting to my servers. Please check your internet connection."
        
        except APIError as e:
            logger.error(f"API error: {e}")
            return "I encountered an error processing your request. Please try again."
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return "An unexpected error occurred. Please try again."
    
    def _trim_history(self) -> None:
        """
        Trim conversation history to prevent context overflow.
        Keeps system message and most recent messages.
        """
        max_history = Config.MAX_CONVERSATION_HISTORY
        
        if len(self.conversation_history) > max_history:
            # Keep system message (if exists) and recent messages
            system_msgs = [msg for msg in self.conversation_history if msg["role"] == "system"]
            other_msgs = [msg for msg in self.conversation_history if msg["role"] != "system"]
            
            # Keep most recent messages
            trimmed_msgs = other_msgs[-(max_history - len(system_msgs)):]
            
            self.conversation_history = system_msgs + trimmed_msgs
            logger.info(f"Conversation history trimmed to {len(self.conversation_history)} messages")
    
    def reset_conversation(self) -> None:
        """
        Reset conversation history (keeps system prompt).
        """
        system_msgs = [msg for msg in self.conversation_history if msg["role"] == "system"]
        self.conversation_history = system_msgs
        logger.info("Conversation history reset")
    
    def get_conversation_summary(self) -> str:
        """
        Get a formatted summary of the conversation.
        
        Returns:
            str: Formatted conversation history
        """
        summary = []
        for msg in self.conversation_history:
            role = msg["role"].upper()
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            summary.append(f"{role}: {content}")
        
        return "\n".join(summary)
    
    def get_token_usage_estimate(self) -> int:
        """
        Estimate approximate token usage of current conversation.
        
        Returns:
            int: Estimated token count
        """
        # Rough estimation: ~4 characters per token
        total_chars = sum(len(msg["content"]) for msg in self.conversation_history)
        return total_chars // 4


def test_chatgpt():
    """Test ChatGPT API standalone."""
    logging.basicConfig(
        level=logging.INFO,
        format=Config.LOG_FORMAT
    )
    
    print("\n" + "="*60)
    print("💬 ChatGPT API Test")
    print("="*60)
    
    # Initialize client
    client = ChatGPTClient(
        api_key=Config.OPENAI_API_KEY,
        model=Config.CHATGPT_MODEL,
        max_tokens=Config.CHATGPT_MAX_TOKENS,
        temperature=Config.CHATGPT_TEMPERATURE,
        system_prompt=Config.SYSTEM_PROMPT
    )
    
    # Test messages
    test_messages = [
        "Hello, who are you?",
        "What can you help me with?",
        "Tell me a short joke."
    ]
    
    for msg in test_messages:
        print(f"\n👤 User: {msg}")
        response = client.send_message(msg)
        if response:
            print(f"🤖 Assistant: {response}")
        else:
            print("✗ No response received")
    
    # Show conversation summary
    print("\n" + "="*60)
    print("Conversation Summary:")
    print("="*60)
    print(client.get_conversation_summary())
    print(f"\nEstimated tokens used: {client.get_token_usage_estimate()}")


if __name__ == "__main__":
    test_chatgpt()