# CitySense - AI Chat Application

A feature-rich AI chat application built with Streamlit, supporting multiple LLM providers (OpenAI, Google Gemini) and vector database integration with Pinecone for conversation context and search.

## 🚀 Features

- **Multiple LLM Providers**: Support for OpenAI GPT models and Google Gemini
- **Vector Database Integration**: Pinecone integration for conversation history and context
- **Rich Chat Interface**: Modern chat UI with message history and export capabilities
- **Conversation Management**: Start new chats, clear history, and export conversations
- **Context-Aware Responses**: Uses previous conversations as context for better responses
- **Flexible Configuration**: Customizable model settings, temperature, and system prompts
- **Search Functionality**: Search through previous conversations using vector similarity
- **Export Options**: Export conversations in JSON, TXT, or CSV formats
- **Real-time Statistics**: Track conversation metrics and usage

## 📋 Prerequisites

- Python 3.8 or higher
- API keys for at least one of the following:
  - OpenAI API key
  - Google Gemini API key
- Pinecone API key (optional, for vector database features)

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   
   Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file and add your API keys:
   ```env
   # Required: At least one LLM provider
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # Optional: For vector database features
   PINECONE_API_KEY=your_pinecone_api_key_here
   
   # Optional: Application settings
   APP_TITLE=CitySense
   DEFAULT_MODEL=gpt-3.5-turbo
   MAX_TOKENS=2000
   TEMPERATURE=0.7
   ```

   **⚠️ SECURITY NOTE:** Never commit your `.env` file or API keys to version control. See [SECURITY.md](SECURITY.md) for detailed security guidelines.

## 🚀 Running the Application

### Local Development

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### Streamlit Community Cloud Deployment

1. **Push your code to GitHub** (make sure to exclude `.env` file)

2. **Deploy on Streamlit Community Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Set up secrets in the Streamlit dashboard:
     ```toml
     [secrets]
     OPENAI_API_KEY = "your_openai_api_key"
     GEMINI_API_KEY = "your_gemini_api_key"
     PINECONE_API_KEY = "your_pinecone_api_key"
     ```

## 📖 Usage Guide

### Getting Started

1. **Configure API Keys**: Ensure at least one LLM provider (OpenAI or Gemini) is configured
2. **Select Model**: Choose your preferred provider and model from the sidebar
3. **Adjust Settings**: Customize temperature, max tokens, and system prompt
4. **Start Chatting**: Type your message in the chat input at the bottom

### Key Features

#### Model Settings
- **Provider**: Choose between OpenAI and Google Gemini
- **Model**: Select from available models (GPT-3.5, GPT-4, Gemini Pro, etc.)
- **Temperature**: Control response creativity (0.0 = deterministic, 2.0 = very creative)
- **Max Tokens**: Set maximum response length
- **System Prompt**: Define the AI's behavior and personality

#### Vector Database Features
- **Context-Aware Responses**: Enable "Use Vector Context" to use previous conversations
- **Conversation Search**: Search through your chat history using natural language
- **Automatic Storage**: Conversations are automatically stored for future context

#### Chat Management
- **New Chat**: Start a fresh conversation
- **Clear History**: Remove all messages from current session
- **Export Options**: Download conversations in multiple formats

### Advanced Features

#### System Prompts
Choose from predefined system prompts or create custom ones:
- **Default**: General helpful assistant
- **Creative**: Imaginative and innovative responses
- **Analytical**: Detailed, logical responses with evidence
- **Concise**: Brief, to-the-point answers
- **Friendly**: Warm, conversational tone

#### Export Formats
- **JSON**: Complete conversation data with metadata
- **TXT**: Human-readable text format
- **CSV**: Spreadsheet-compatible format

## 🏗️ Architecture

### Core Components

1. **app.py**: Main Streamlit application and UI
2. **llm_service.py**: LLM provider integration (OpenAI, Gemini)
3. **vector_service.py**: Pinecone vector database operations
4. **config.py**: Application configuration and constants

### Data Flow

1. User input → LLM Service → Response generation
2. Conversation → Vector Service → Embedding storage
3. New query → Vector search → Context retrieval → Enhanced response

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | One of OpenAI/Gemini |
| `GEMINI_API_KEY` | Google Gemini API key | One of OpenAI/Gemini |
| `PINECONE_API_KEY` | Pinecone API key | Optional |
| `APP_TITLE` | Application title | Optional |
| `DEFAULT_MODEL` | Default LLM model | Optional |
| `MAX_TOKENS` | Default max tokens | Optional |
| `TEMPERATURE` | Default temperature | Optional |

### Model Support

#### OpenAI Models
- `gpt-4-turbo-preview`
- `gpt-4`
- `gpt-3.5-turbo`
- `gpt-3.5-turbo-16k`

#### Google Gemini Models
- `gemini-pro`
- `gemini-pro-vision`

## 🐛 Troubleshooting

### Common Issues

1. **"No API keys configured"**
   - Ensure your `.env` file contains valid API keys
   - Check that environment variables are properly loaded

2. **"Vector database not configured"**
   - Add your Pinecone API key to the `.env` file
   - Vector features will be disabled without Pinecone

3. **"Failed to generate response"**
   - Verify your API keys are valid and have sufficient credits
   - Check your internet connection
   - Try a different model or provider

4. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility (3.8+)

### Performance Tips

- Use `gpt-3.5-turbo` for faster responses and lower costs
- Adjust max tokens based on your needs (lower = faster)
- Disable vector context if not needed to improve response speed

## 📝 Development

### Adding New Features

1. **New LLM Provider**: Extend `llm_service.py` with new provider integration
2. **Custom UI Components**: Add new sections to the sidebar or main interface
3. **Export Formats**: Add new export options in the `export_conversation` method

### Code Structure

```
citysense/
├── app.py              # Main Streamlit application
├── llm_service.py      # LLM provider integrations
├── vector_service.py   # Vector database operations
├── config.py           # Configuration and constants
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md          # This file
```

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the configuration settings
3. Ensure all API keys are valid and properly configured
4. Check the Streamlit logs for detailed error messages

---

**Happy Chatting! 🤖💬**