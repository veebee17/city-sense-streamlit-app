import os
from typing import List, Dict, Any, Optional, Generator
import openai
import google.generativeai as genai
from config import Config

class LLMService:
    def __init__(self):
        self.openai_client = None
        self.gemini_model = None
        self.setup_services()
    
    def setup_services(self):
        """Setup OpenAI and Gemini services"""
        # Setup OpenAI
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key:
            self.openai_client = openai.OpenAI(api_key=openai_api_key)
        
        # Setup Gemini
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if gemini_api_key:
            genai.configure(api_key=gemini_api_key)
    
    def get_openai_response(self, messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo", 
                           temperature: float = 0.7, max_tokens: int = 1000, 
                           stream: bool = False) -> Any:
        """Get response from OpenAI"""
        try:
            if not self.openai_client:
                return {"error": "OpenAI client not initialized"}
            
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream
            )
            
            if stream:
                return response
            else:
                return {
                    "content": response.choices[0].message.content,
                    "usage": response.usage.dict() if response.usage else None
                }
                
        except Exception as e:
            return {"error": f"OpenAI API error: {str(e)}"}
    
    def get_gemini_response(self, messages: List[Dict[str, str]], model: str = "gemini-pro", 
                           temperature: float = 0.7, max_tokens: int = 1000) -> Dict[str, Any]:
        """Get response from Gemini"""
        try:
            # Convert messages to Gemini format
            gemini_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    # Gemini doesn't have system role, prepend to first user message
                    continue
                elif msg["role"] == "user":
                    gemini_messages.append({"role": "user", "parts": [msg["content"]]})
                elif msg["role"] == "assistant":
                    gemini_messages.append({"role": "model", "parts": [msg["content"]]})
            
            # Handle system message by prepending to first user message
            system_message = next((msg["content"] for msg in messages if msg["role"] == "system"), None)
            if system_message and gemini_messages:
                first_user_msg = gemini_messages[0]
                if first_user_msg["role"] == "user":
                    first_user_msg["parts"][0] = f"{system_message}\n\n{first_user_msg['parts'][0]}"
            
            model_instance = genai.GenerativeModel(model)
            
            # Configure generation
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            
            # Start chat or generate response
            if len(gemini_messages) > 1:
                chat = model_instance.start_chat(history=gemini_messages[:-1])
                response = chat.send_message(
                    gemini_messages[-1]["parts"][0],
                    generation_config=generation_config
                )
            else:
                response = model_instance.generate_content(
                    gemini_messages[0]["parts"][0] if gemini_messages else "Hello",
                    generation_config=generation_config
                )
            
            return {
                "content": response.text,
                "usage": {
                    "prompt_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else 0,
                    "completion_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else 0,
                    "total_tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0
                }
            }
            
        except Exception as e:
            return {"error": f"Gemini API error: {str(e)}"}
    
    def get_available_models(self, provider: str) -> List[str]:
        """Get available models for a provider"""
        if provider == "openai":
            return Config.OPENAI_MODELS
        elif provider == "gemini":
            return Config.GEMINI_MODELS
        else:
            return []
    
    def test_api_connection(self, provider: str) -> Dict[str, Any]:
        """Test API connection for a provider"""
        try:
            if provider == "openai":
                if not self.openai_client:
                    return {"status": "error", "message": "OpenAI API key not configured"}
                
                # Test with a simple request
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=5
                )
                return {"status": "success", "message": "OpenAI API connected successfully"}
                
            elif provider == "gemini":
                try:
                    model = genai.GenerativeModel("gemini-pro")
                    response = model.generate_content("Hello")
                    return {"status": "success", "message": "Gemini API connected successfully"}
                except Exception:
                    return {"status": "error", "message": "Gemini API key not configured or invalid"}
            
            else:
                return {"status": "error", "message": "Unknown provider"}
                
        except Exception as e:
            return {"status": "error", "message": f"Connection test failed: {str(e)}"}
    
    def generate_stream_response(self, messages: List[Dict[str, str]], provider: str, 
                               model: str, temperature: float = 0.7, 
                               max_tokens: int = 1000) -> Generator[str, None, None]:
        """Generate streaming response"""
        try:
            if provider == "openai":
                if not self.openai_client:
                    yield "Error: OpenAI client not initialized"
                    return
                
                stream = self.openai_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        yield chunk.choices[0].delta.content
                        
            elif provider == "gemini":
                # Gemini streaming is more complex, for now return non-streaming
                response = self.get_gemini_response(messages, model, temperature, max_tokens)
                if "error" in response:
                    yield f"Error: {response['error']}"
                else:
                    # Simulate streaming by yielding chunks
                    content = response["content"]
                    chunk_size = 10
                    for i in range(0, len(content), chunk_size):
                        yield content[i:i+chunk_size]
                        
        except Exception as e:
            yield f"Error: {str(e)}"