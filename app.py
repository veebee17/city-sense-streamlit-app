import streamlit as st
import uuid
import json
import csv
from datetime import datetime
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from llm_service import LLMService
from vector_service import VectorService
from config import Config

class CitySense:
    def __init__(self):
        self.setup_page_config()
        self.initialize_session_state()
        self.setup_services()
    
    def setup_page_config(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title=Config.APP_TITLE,
            page_icon=Config.APP_ICON,
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Apply custom CSS
        st.markdown(Config.CUSTOM_CSS, unsafe_allow_html=True)
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        # Initialize messages
        if Config.SESSION_KEYS['messages'] not in st.session_state:
            st.session_state[Config.SESSION_KEYS['messages']] = []
        
        # Initialize conversation ID
        if Config.SESSION_KEYS['conversation_id'] not in st.session_state:
            st.session_state[Config.SESSION_KEYS['conversation_id']] = str(uuid.uuid4())
        
        # Initialize model settings
        if Config.SESSION_KEYS['model_settings'] not in st.session_state:
            st.session_state[Config.SESSION_KEYS['model_settings']] = Config.DEFAULT_MODEL_SETTINGS.copy()
    
    def setup_services(self):
        """Initialize LLM and Vector services"""
        if Config.SESSION_KEYS['llm_service'] not in st.session_state:
            st.session_state[Config.SESSION_KEYS['llm_service']] = LLMService()
        
        if Config.SESSION_KEYS['vector_service'] not in st.session_state:
            st.session_state[Config.SESSION_KEYS['vector_service']] = VectorService()
        
        self.llm_service = st.session_state[Config.SESSION_KEYS['llm_service']]
        self.vector_service = st.session_state[Config.SESSION_KEYS['vector_service']]
    
    def render_sidebar(self):
        """Render the sidebar with model settings and chat history"""
        with st.sidebar:
            # Header
            st.markdown(f"<div class='main-header'><h1>{Config.APP_ICON} {Config.APP_TITLE}</h1></div>", 
                       unsafe_allow_html=True)
            
            # API Configuration Status
            self.render_api_status()
            
            # Model Settings Section
            self.render_model_settings()
            
            st.divider()
            
            # Vector Database Settings
            self.render_vector_settings()
            
            st.divider()
            
            # Chat Management
            self.render_chat_management()
            
            st.divider()
            
            # Statistics and Info
            self.render_statistics()
    
    def render_api_status(self):
        """Render API configuration status"""
        st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
        st.subheader("🔑 API Status")
        
        # Check API configurations
        openai_configured = Config.is_api_configured('openai')
        gemini_configured = Config.is_api_configured('gemini')
        pinecone_configured = Config.is_api_configured('pinecone')
        
        # Display status
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**OpenAI:** {'✅' if openai_configured else '❌'}")
            st.markdown(f"**Gemini:** {'✅' if gemini_configured else '❌'}")
        with col2:
            st.markdown(f"**Pinecone:** {'✅' if pinecone_configured else '❌'}")
            st.markdown(f"**Vector DB:** {'✅' if self.vector_service.is_available() else '❌'}")
        
        if not (openai_configured or gemini_configured):
            st.markdown("<div class='error-message'>⚠️ No LLM API configured!</div>", 
                       unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def render_model_settings(self):
        """Render model settings section"""
        st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
        st.subheader("⚙️ Model Settings")
        
        # Get available providers
        available_providers = Config.get_available_providers()
        if not available_providers:
            st.error("No API keys configured! Please set up your API keys.")
            st.info("Add your API keys to the .env file or Streamlit secrets.")
            st.markdown("</div>", unsafe_allow_html=True)
            return
        
        current_settings = st.session_state[Config.SESSION_KEYS['model_settings']]
        
        # Provider selection
        provider = st.selectbox(
            "Provider",
            available_providers,
            index=0 if current_settings['provider'] not in available_providers 
            else available_providers.index(current_settings['provider'])
        )
        
        # Model selection based on provider
        available_models = Config.get_models_for_provider(provider)
        model = st.selectbox(
            "Model",
            available_models,
            index=0 if current_settings['model'] not in available_models
            else available_models.index(current_settings['model'])
        )
        
        # Model parameters
        temperature = st.slider("Temperature", 0.0, 2.0, current_settings['temperature'], 0.1)
        max_tokens = st.slider("Max Tokens", 100, 4000, current_settings['max_tokens'], 100)
        
        # Use context toggle
        use_context = st.checkbox(
            "Use Vector Context", 
            value=current_settings.get('use_context', True),
            help="Use previous conversations as context (requires Pinecone)"
        )
        
        # System prompt selection
        prompt_type = st.selectbox(
            "System Prompt Type",
            list(Config.SYSTEM_PROMPTS.keys()),
            index=0
        )
        
        if prompt_type == 'default':
            system_prompt = st.text_area(
                "Custom System Prompt",
                value=current_settings['system_prompt'],
                height=100,
                help="This message sets the behavior of the AI assistant"
            )
        else:
            system_prompt = Config.SYSTEM_PROMPTS[prompt_type]
            st.text_area(
                "System Prompt (Preview)",
                value=system_prompt,
                height=100,
                disabled=True
            )
        
        # Update session state
        new_settings = {
            'provider': provider,
            'model': model,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'use_context': use_context,
            'system_prompt': system_prompt
        }
        
        st.session_state[Config.SESSION_KEYS['model_settings']] = Config.validate_model_settings(new_settings)
        
        # Display current model info
        st.markdown(f"<div class='model-info'>Current: {provider} - {model}</div>", 
                   unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def render_vector_settings(self):
        """Render vector database settings"""
        st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
        st.subheader("🗄️ Vector Database")
        
        if self.vector_service.is_available():
            stats = self.vector_service.get_conversation_stats()
            st.markdown(f"**Status:** {stats['status']}")
            st.markdown(f"**Stored Conversations:** {stats['total_vectors']}")
            
            # Search conversations
            search_query = st.text_input("Search Conversations", placeholder="Enter search terms...")
            if search_query:
                with st.spinner("Searching..."):
                    results = self.vector_service.search_conversations(search_query, limit=5)
                    if results:
                        st.write("**Search Results:**")
                        for i, result in enumerate(results[:3]):
                            with st.expander(f"Result {i+1} (Score: {result['score']:.2f})"):
                                st.write(f"**User:** {result['user_input'][:100]}...")
                                st.write(f"**Assistant:** {result['assistant_response'][:100]}...")
                    else:
                        st.info("No matching conversations found.")
            
            # Clear vector database
            if st.button("Clear Vector DB", help="Clear all stored conversations"):
                self.vector_service.clear_conversation_history()
                st.rerun()
        else:
            st.markdown("<div class='warning-message'>Vector database not configured</div>", 
                       unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def render_chat_management(self):
        """Render chat management section"""
        st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
        st.subheader("💬 Chat Management")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("New Chat", use_container_width=True):
                self.start_new_conversation()
        
        with col2:
            if st.button("Clear History", use_container_width=True):
                self.clear_chat_history()
        
        # Export options
        messages = st.session_state[Config.SESSION_KEYS['messages']]
        if messages:
            st.subheader("📤 Export Chat")
            export_format = st.selectbox("Format", Config.EXPORT_FORMATS)
            
            if st.button("Export", use_container_width=True):
                self.export_conversation(export_format)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def render_statistics(self):
        """Render chat statistics"""
        messages = st.session_state[Config.SESSION_KEYS['messages']]
        if not messages:
            return
        
        st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
        st.subheader("📊 Chat Statistics")
        
        total_messages = len(messages)
        user_messages = len([msg for msg in messages if msg['role'] == 'user'])
        assistant_messages = len([msg for msg in messages if msg['role'] == 'assistant'])
        
        # Calculate total characters
        total_chars = sum(len(msg['content']) for msg in messages)
        
        st.markdown(f"<div class='stats-container'>", unsafe_allow_html=True)
        st.metric("Total Messages", total_messages)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("User", user_messages)
        with col2:
            st.metric("Assistant", assistant_messages)
        
        st.metric("Total Characters", f"{total_chars:,}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def start_new_conversation(self):
        """Start a new conversation"""
        st.session_state[Config.SESSION_KEYS['messages']] = []
        st.session_state[Config.SESSION_KEYS['conversation_id']] = str(uuid.uuid4())
        st.rerun()
    
    def clear_chat_history(self):
        """Clear chat history"""
        st.session_state[Config.SESSION_KEYS['messages']] = []
        st.rerun()
    
    def export_conversation(self, format_type: str):
        """Export conversation in specified format"""
        messages = st.session_state[Config.SESSION_KEYS['messages']]
        if not messages:
            st.warning("No messages to export")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_export_{timestamp}"
        
        if format_type == "JSON":
            data = {
                'conversation_id': st.session_state[Config.SESSION_KEYS['conversation_id']],
                'timestamp': datetime.now().isoformat(),
                'model_settings': st.session_state[Config.SESSION_KEYS['model_settings']],
                'messages': messages
            }
            content = json.dumps(data, indent=2)
            st.download_button(
                label="Download JSON",
                data=content,
                file_name=f"{filename}.json",
                mime="application/json"
            )
        
        elif format_type == "TXT":
            settings = st.session_state[Config.SESSION_KEYS['model_settings']]
            content = f"Chat Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            content += f"Model: {settings['provider']} - {settings['model']}\n"
            content += "=" * 50 + "\n\n"
            
            for msg in messages:
                role = msg['role'].title()
                content += f"{role}: {msg['content']}\n\n"
            
            st.download_button(
                label="Download TXT",
                data=content,
                file_name=f"{filename}.txt",
                mime="text/plain"
            )
        
        elif format_type == "CSV":
            import io
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['Timestamp', 'Role', 'Content'])
            
            for msg in messages:
                writer.writerow([datetime.now().isoformat(), msg['role'], msg['content']])
            
            st.download_button(
                label="Download CSV",
                data=output.getvalue(),
                file_name=f"{filename}.csv",
                mime="text/csv"
            )
    
    def display_chat_messages(self):
        """Display chat messages with custom styling"""
        messages = st.session_state[Config.SESSION_KEYS['messages']]
        
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    def process_user_input(self, user_input: str):
        """Process user input and generate response"""
        messages = st.session_state[Config.SESSION_KEYS['messages']]
        settings = st.session_state[Config.SESSION_KEYS['model_settings']]
        conversation_id = st.session_state[Config.SESSION_KEYS['conversation_id']]
        
        # Add user message to chat
        messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Get context from vector database if enabled
                    context = None
                    if settings.get('use_context', True) and self.vector_service.is_available():
                        context = self.vector_service.get_relevant_context(user_input)
                    
                    # Generate response
                    response = self.llm_service.generate_response(
                        messages=messages,
                        context=context,
                        **settings
                    )
                    
                    if response:
                        st.markdown(response)
                        messages.append({"role": "assistant", "content": response})
                        
                        # Store in vector database
                        if self.vector_service.is_available():
                            self.vector_service.store_conversation_chunk(
                                user_input, response, conversation_id
                            )
                    else:
                        error_msg = "Sorry, I couldn't generate a response. Please check your API configuration."
                        st.error(error_msg)
                        messages.append({"role": "assistant", "content": error_msg})
                
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    messages.append({"role": "assistant", "content": error_msg})
    
    def run(self):
        """Main application loop"""
        # Render sidebar
        self.render_sidebar()
        
        # Main chat interface
        st.title("💬 Chat")
        
        # Display existing messages
        self.display_chat_messages()
        
        # Chat input
        if prompt := st.chat_input("What would you like to know?"):
            self.process_user_input(prompt)

if __name__ == "__main__":
    app = CitySense()
    app.run()