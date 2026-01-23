import sys
sys.dont_write_bytecode = True

import os
from dotenv import load_dotenv
from openai import OpenAI
import logging

load_dotenv()

class llmRequester:
    def __init__(self):
        """Initialize the GPT client with API key from .env"""
        self.api_key = os.getenv("GPT_KEY")
        
        if not self.api_key:
            raise ValueError("GPT_KEY not found in .env file")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"  # or "gpt-4o" for more powerful model
        self.temperature = 0.1
        self.max_tokens = 512
        
        logging.info("GPT client initialized successfully")
    
    def run_llama(self, prompt: str, text: str) -> str:
        """
        Run GPT with the given prompt and text.
        Maintains the same interface as the original for compatibility.
        
        Args:
            prompt: The prompt template with {text} placeholder
            text: The text to insert into the prompt
        
        Returns:
            The GPT response as a string
        """
        try:
            # Replace the {text} placeholder in the prompt
            full_prompt = prompt.replace("{text}", text)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that analyzes articles about technology and its societal impacts."
                    },
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Extract the response text
            answer = response.choices[0].message.content.strip()
            
            return answer
            
        except Exception as e:
            logging.error(f"Error calling GPT API: {e}")
            raise
    
    def set_model(self, model: str):
        """
        Change the GPT model being used.
        
        Options:
        - "gpt-4o-mini": Faster, cheaper (recommended for your use case)
        - "gpt-4o": More powerful, more expensive
        - "gpt-3.5-turbo": Legacy, cheapest
        """
        self.model = model
        logging.info(f"Model changed to: {model}")
    
    def set_temperature(self, temperature: float):
        """Set the temperature for response generation (0.0-2.0)"""
        self.temperature = temperature
    
    def set_max_tokens(self, max_tokens: int):
        """Set the maximum number of tokens in the response"""
        self.max_tokens = max_tokens


# Backwards compatibility - if other code expects these classes
class TogetherLLM:
    """Deprecated: Use llmRequester instead"""
    def __init__(self, *args, **kwargs):
        logging.warning("TogetherLLM is deprecated. Use llmRequester instead.")
        raise NotImplementedError("Please use llmRequester class instead")