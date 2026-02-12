"""
LLM Provider Configuration and Management.

This module provides a flexible system for supporting multiple LLM providers
including DeepSeek, OpenAI, Anthropic, and local models.
"""

import os
from typing import Optional, Dict, List
from dataclasses import dataclass
from utils.logger import setup_logger

logger = setup_logger("llm_providers")

@dataclass
class ModelConfig:
    """Configuration for a specific model."""
    name: str
    provider: str
    base_url: str
    supports_reasoning: bool = False
    context_window: int = 4096
    description: str = ""


@dataclass
class ProviderConfig:
    """Configuration for an LLM provider."""
    name: str
    base_url: str
    api_key_env_var: str
    models: Dict[str, ModelConfig]
    requires_api_key: bool = True


class LLMProviderRegistry:
    """Registry of supported LLM providers and their configurations."""
    
    PROVIDERS: Dict[str, ProviderConfig] = {
        'deepseek': ProviderConfig(
            name='DeepSeek',
            base_url='https://api.deepseek.com/v1',
            api_key_env_var='DEEPSEEK_API_KEY',
            models={
                'deepseek-chat': ModelConfig(
                    name='deepseek-chat',
                    provider='deepseek',
                    base_url='https://api.deepseek.com/v1',
                    supports_reasoning=False,
                    context_window=16384,
                    description='Fast chat model for general queries'
                ),
                'deepseek-reasoner': ModelConfig(
                    name='deepseek-reasoner',
                    provider='deepseek',
                    base_url='https://api.deepseek.com/v1',
                    supports_reasoning=True,
                    context_window=16384,
                    description='Advanced reasoning model for complex analysis'
                )
            }
        ),
        'openai': ProviderConfig(
            name='OpenAI',
            base_url='https://api.openai.com/v1',
            api_key_env_var='OPENAI_API_KEY',
            models={
                'gpt-4': ModelConfig(
                    name='gpt-4',
                    provider='openai',
                    base_url='https://api.openai.com/v1',
                    supports_reasoning=True,
                    context_window=8192,
                    description='Most capable GPT-4 model'
                ),
                'gpt-4-turbo': ModelConfig(
                    name='gpt-4-turbo',
                    provider='openai',
                    base_url='https://api.openai.com/v1',
                    supports_reasoning=True,
                    context_window=128000,
                    description='GPT-4 Turbo with large context window'
                ),
                'gpt-3.5-turbo': ModelConfig(
                    name='gpt-3.5-turbo',
                    provider='openai',
                    base_url='https://api.openai.com/v1',
                    supports_reasoning=False,
                    context_window=16385,
                    description='Fast and cost-effective chat model'
                )
            }
        ),
        'anthropic': ProviderConfig(
            name='Anthropic',
            base_url='https://api.anthropic.com/v1',
            api_key_env_var='ANTHROPIC_API_KEY',
            models={
                'claude-3-opus': ModelConfig(
                    name='claude-3-opus-20240229',
                    provider='anthropic',
                    base_url='https://api.anthropic.com/v1',
                    supports_reasoning=True,
                    context_window=200000,
                    description='Most capable Claude model'
                ),
                'claude-3-sonnet': ModelConfig(
                    name='claude-3-sonnet-20240229',
                    provider='anthropic',
                    base_url='https://api.anthropic.com/v1',
                    supports_reasoning=True,
                    context_window=200000,
                    description='Balanced performance and speed'
                ),
                'claude-3-haiku': ModelConfig(
                    name='claude-3-haiku-20240307',
                    provider='anthropic',
                    base_url='https://api.anthropic.com/v1',
                    supports_reasoning=False,
                    context_window=200000,
                    description='Fast and compact model'
                )
            }
        ),
        'local': ProviderConfig(
            name='Local (Ollama)',
            base_url='http://localhost:11434/v1',
            api_key_env_var='LOCAL_API_KEY',
            requires_api_key=False,
            models={
                'llama3': ModelConfig(
                    name='llama3',
                    provider='local',
                    base_url='http://localhost:11434/v1',
                    supports_reasoning=True,
                    context_window=8192,
                    description='Meta Llama 3 running locally'
                ),
                'mistral': ModelConfig(
                    name='mistral',
                    provider='local',
                    base_url='http://localhost:11434/v1',
                    supports_reasoning=False,
                    context_window=8192,
                    description='Mistral 7B running locally'
                ),
                'codellama': ModelConfig(
                    name='codellama',
                    provider='local',
                    base_url='http://localhost:11434/v1',
                    supports_reasoning=False,
                    context_window=16384,
                    description='Code Llama specialized for code generation'
                )
            }
        )
    }
    
    @classmethod
    def get_provider(cls, provider_name: str) -> Optional[ProviderConfig]:
        """Get provider configuration by name."""
        return cls.PROVIDERS.get(provider_name.lower())
    
    @classmethod
    def get_model(cls, provider_name: str, model_name: str) -> Optional[ModelConfig]:
        """Get model configuration."""
        provider = cls.get_provider(provider_name)
        if provider:
            return provider.models.get(model_name)
        return None
    
    @classmethod
    def list_providers(cls) -> List[str]:
        """List all available providers."""
        return list(cls.PROVIDERS.keys())
    
    @classmethod
    def list_models(cls, provider_name: str) -> List[str]:
        """List all models for a provider."""
        provider = cls.get_provider(provider_name)
        if provider:
            return list(provider.models.keys())
        return []
    
    @classmethod
    def get_available_providers(cls) -> List[str]:
        """Get list of providers with API keys configured."""
        available = []
        for provider_name, provider_config in cls.PROVIDERS.items():
            if not provider_config.requires_api_key:
                available.append(provider_name)
            elif os.environ.get(provider_config.api_key_env_var):
                available.append(provider_name)
        return available
    
    @classmethod
    def get_api_key(cls, provider_name: str) -> Optional[str]:
        """Get API key for a provider."""
        provider = cls.get_provider(provider_name)
        if provider:
            if not provider.requires_api_key:
                return "not-required"
            return os.environ.get(provider.api_key_env_var)
        return None
    
    @classmethod
    def auto_select_model(cls, provider_name: str, is_complex_task: bool) -> Optional[str]:
        """Automatically select appropriate model based on task complexity."""
        provider = cls.get_provider(provider_name)
        if not provider:
            return None
        
        # Filter models by reasoning capability
        suitable_models = [
            (name, config) for name, config in provider.models.items()
            if is_complex_task == config.supports_reasoning or not is_complex_task
        ]
        
        if not suitable_models:
            # Fallback to any model
            suitable_models = list(provider.models.items())
        
        if suitable_models:
            # Return first suitable model
            return suitable_models[0][0]
        
        return None


def get_default_provider() -> str:
    """Get the default provider based on environment configuration."""
    # Check for explicit default
    default = os.environ.get('DEFAULT_LLM_PROVIDER', 'deepseek')
    
    # Verify it's available
    available = LLMProviderRegistry.get_available_providers()
    if default in available:
        return default
    
    # Fallback to first available
    if available:
        logger.info(f"Default provider '{default}' not available, using '{available[0]}'")
        return available[0]
    
    logger.warning("No LLM providers configured")
    return 'deepseek'  # Fallback default


def get_default_model(provider_name: Optional[str] = None, is_complex_task: bool = False) -> str:
    """Get default model for a provider."""
    if not provider_name:
        provider_name = get_default_provider()
    
    # Try auto-selection
    model = LLMProviderRegistry.auto_select_model(provider_name, is_complex_task)
    if model:
        return model
    
    # Fallback to environment or first model
    if provider_name == 'deepseek':
        return os.environ.get(
            'DEEPSEEK_REASONER_MODEL' if is_complex_task else 'DEEPSEEK_CHAT_MODEL',
            'deepseek-reasoner' if is_complex_task else 'deepseek-chat'
        )
    elif provider_name == 'openai':
        return 'gpt-4' if is_complex_task else 'gpt-3.5-turbo'
    elif provider_name == 'anthropic':
        return 'claude-3-opus' if is_complex_task else 'claude-3-haiku'
    elif provider_name == 'local':
        return 'llama3' if is_complex_task else 'mistral'
    
    return 'deepseek-chat'
