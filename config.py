import os
import streamlit as st
from typing import Dict, List

class Config:
    """Configuration class for the CitySense application"""
    
    # Application Settings
    APP_TITLE = os.getenv('APP_TITLE', 'CitySense')
    APP_ICON = "🤖"
    
    # Model Settings
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'gpt-3.5-turbo')
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '2000'))
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Available Models
    OPENAI_MODELS = [
        'gpt-4-turbo-preview',
        'gpt-4',
        'gpt-3.5-turbo',
        'gpt-3.5-turbo-16k'
    ]
    
    GEMINI_MODELS = [
        'gemini-pro',
        'gemini-pro-vision'
    ]
    
    # UI Settings
    SIDEBAR_WIDTH = 300
    CHAT_INPUT_HEIGHT = 100
    
    # Vector Database Settings
    PINECONE_INDEX_NAME = "citysense-conversations"
    EMBEDDING_DIMENSION = 1536  # OpenAI embedding dimension
    SIMILARITY_THRESHOLD = 0.7
    MAX_CONTEXT_CHUNKS = 3
    
    # Session State Keys
    SESSION_KEYS = {
        'messages': 'messages',
        'conversation_id': 'conversation_id',
        'model_settings': 'model_settings',
        'api_keys_configured': 'api_keys_configured',
        'vector_service': 'vector_service',
        'llm_service': 'llm_service'
    }
    
    # Default Model Settings
    DEFAULT_MODEL_SETTINGS = {
        'provider': 'openai',
        'model': 'gpt-3.5-turbo',
        'temperature': 0.7,
        'max_tokens': 2000,
        'use_context': True,
        'system_prompt': "You are a helpful AI assistant. Provide clear, accurate, and helpful responses."
    }
    
    # System Prompts
    SYSTEM_PROMPTS = {
        'default': "You are a helpful AI assistant. Provide clear, accurate, and helpful responses.",
        'creative': "You are a creative AI assistant. Think outside the box and provide imaginative, innovative responses.",
        'analytical': "You are an analytical AI assistant. Provide detailed, logical, and well-reasoned responses with supporting evidence.",
        'concise': "You are a concise AI assistant. Provide brief, to-the-point responses while maintaining accuracy.",
        'friendly': "You are a friendly AI assistant. Respond in a warm, conversational, and approachable manner."
    }
    
    # Export Formats
    EXPORT_FORMATS = ['JSON', 'TXT', 'CSV']
    
    # Styling
    CUSTOM_CSS = """
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid;
    }
    
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #1f77b4;
    }
    
    .assistant-message {
        background-color: #f9f9f9;
        border-left-color: #ff7f0e;
    }
    
    .sidebar-section {
        padding: 1rem 0;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .model-info {
        background-color: #e8f4f8;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-size: 0.9em;
    }
    
    .stats-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .error-message {
        background-color: #ffe6e6;
        color: #d32f2f;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #d32f2f;
    }
    
    .success-message {
        background-color: #e8f5e8;
        color: #2e7d32;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #2e7d32;
    }
    
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
    </style>
    """
    
    @classmethod
    def get_api_key(cls, service: str) -> str:
        """Get API key for a service from environment or Streamlit secrets"""
        key_name = f"{service.upper()}_API_KEY"
        # First try environment variables
        env_key = os.getenv(key_name)
        if env_key:
            return env_key
        
        # Then try Streamlit secrets if available
        try:
            return st.secrets.get(key_name, "")
        except (FileNotFoundError, KeyError):
            return ""
    
    @classmethod
    def is_api_configured(cls, service: str) -> bool:
        """Check if API key is configured for a service"""
        return bool(cls.get_api_key(service))
    
    @classmethod
    def get_available_providers(cls) -> List[str]:
        """Get list of available LLM providers based on configured API keys"""
        providers = []
        if cls.is_api_configured('openai'):
            providers.append('openai')
        if cls.is_api_configured('gemini'):
            providers.append('gemini')
        return providers
    
    @classmethod
    def get_models_for_provider(cls, provider: str) -> List[str]:
        """Get available models for a provider"""
        if provider == 'openai':
            return cls.OPENAI_MODELS
        elif provider == 'gemini':
            return cls.GEMINI_MODELS
        return []
    
    @classmethod
    def validate_model_settings(cls, settings: Dict) -> Dict:
        """Validate and sanitize model settings"""
        validated = cls.DEFAULT_MODEL_SETTINGS.copy()
        
        if 'provider' in settings and settings['provider'] in ['openai', 'gemini']:
            validated['provider'] = settings['provider']
        
        if 'model' in settings:
            available_models = cls.get_models_for_provider(validated['provider'])
            if settings['model'] in available_models:
                validated['model'] = settings['model']
        
        if 'temperature' in settings:
            validated['temperature'] = max(0.0, min(2.0, float(settings['temperature'])))
        
        if 'max_tokens' in settings:
            validated['max_tokens'] = max(1, min(4000, int(settings['max_tokens'])))
        
        if 'use_context' in settings:
            validated['use_context'] = bool(settings['use_context'])
        
        if 'system_prompt' in settings and settings['system_prompt'].strip():
            validated['system_prompt'] = settings['system_prompt'].strip()
        
        return validated