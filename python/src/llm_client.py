"""
Unified LLM Client for LAEV Agents
Provides a consistent interface for all LLM providers
"""

import os
from typing import Optional
from openai import OpenAI

# Auto-load .env file if exists
try:
    from dotenv import load_dotenv
    # Try multiple locations
    env_paths = ['.env', '../.env', '../../.env', '/data1/xh/workspace/white-paper/.env']
    for env_path in env_paths:
        if os.path.exists(env_path):
            load_dotenv(env_path)
            break
except ImportError:
    pass


class LLMClient:
    """
    Unified LLM client wrapper for all agents.
    
    Usage:
        llm = LLMClient(provider="deepseek")
        response = llm.generate(
            system_prompt="You are a helpful assistant",
            user_prompt="Hello",
            temperature=0.3
        )
    """
    
    def __init__(self, provider: str = "deepseek", api_key: Optional[str] = None):
        """
        Initialize LLM client
        
        Args:
            provider: Provider name ('deepseek', 'openai', 'anthropic')
            api_key: API key. If None, loads from environment
        """
        self.provider = provider
        
        # Import here to avoid circular dependencies
        from llm_providers import LLMProviderRegistry
        
        self.config = LLMProviderRegistry.get_provider(provider)
        if not self.config:
            raise ValueError(f"Unknown provider: {provider}")
        
        # Get API key
        self.api_key = api_key or LLMProviderRegistry.get_api_key(provider)
        if not self.api_key and self.config.requires_api_key:
            raise ValueError(f"API key required for {provider}. Set {self.config.api_key_env_var}")
        
        # Get base URL
        self.base_url = self.config.base_url
        base_url_env = f"{provider.upper()}_BASE_URL"
        self.base_url = os.environ.get(base_url_env, self.base_url)
        
        # Create client
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        self.model = self._get_default_model()
    
    def _get_default_model(self) -> str:
        """Get default model for provider"""
        from llm_providers import LLMProviderRegistry
        
        # Default to first available model
        if self.config.models:
            return list(self.config.models.keys())[0]
        
        # Fallback defaults
        defaults = {
            "deepseek": "deepseek-chat",
            "openai": "gpt-3.5-turbo",
            "anthropic": "claude-3-sonnet-20240229"
        }
        return defaults.get(self.provider, "gpt-3.5-turbo")
    
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        model: Optional[str] = None,
        response_format: Optional[str] = None
    ) -> str:
        """
        Generate text from LLM
        
        Args:
            system_prompt: System instructions
            user_prompt: User query
            temperature: Sampling temperature (0-2)
            model: Model name (uses default if None)
            response_format: "json" for JSON mode
            
        Returns:
            Generated text response
        """
        model = model or self.model
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        kwargs = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        
        # Add JSON mode if requested
        if response_format == "json":
            if self.provider == "openai":
                kwargs["response_format"] = {"type": "json_object"}
            # Note: DeepSeek may not support JSON mode, will parse manually
        
        try:
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"LLM generation failed: {e}")
    
    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        model: Optional[str] = None
    ) -> str:
        """
        Generate JSON from LLM (adds JSON instruction to prompt)
        
        Returns:
            JSON string
        """
        # Enhance prompt with JSON instruction
        json_prompt = user_prompt + "\n\nRespond with valid JSON only."
        json_system = system_prompt + "\nAlways respond with valid JSON."
        
        return self.generate(
            system_prompt=json_system,
            user_prompt=json_prompt,
            temperature=temperature,
            model=model,
            response_format="json"
        )


# Factory function for convenience
def get_llm_client(provider: str = "deepseek") -> LLMClient:
    """Get LLM client for provider"""
    return LLMClient(provider=provider)
