# Security Guidelines

## 🔐 API Key Management

### Local Development

For local development, use environment variables or Streamlit secrets:

#### Option 1: Environment Variables
Create a `.env` file in your project root (already excluded by .gitignore):

```bash
# .env file (NEVER commit this file)
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

#### Option 2: Streamlit Secrets
Create a `.streamlit/secrets.toml` file (already excluded by .gitignore):

```toml
# .streamlit/secrets.toml (NEVER commit this file)
OPENAI_API_KEY = "your_openai_api_key_here"
GEMINI_API_KEY = "your_gemini_api_key_here"
PINECONE_API_KEY = "your_pinecone_api_key_here"
```

### Production Deployment (Streamlit Community Cloud)

1. **Never commit API keys to your repository**
2. **Use Streamlit Community Cloud's secrets management**:
   - Go to your app's settings in Streamlit Community Cloud
   - Navigate to the "Secrets" section
   - Add your secrets in TOML format:

```toml
OPENAI_API_KEY = "your_openai_api_key_here"
GEMINI_API_KEY = "your_gemini_api_key_here"
PINECONE_API_KEY = "your_pinecone_api_key_here"
```

## 🛡️ Security Best Practices

### Code Security
- ✅ No hardcoded API keys in source code
- ✅ Proper error handling to prevent information leakage
- ✅ Input validation and sanitization
- ✅ Secure secrets management

### Repository Security
- ✅ Comprehensive `.gitignore` file
- ✅ Secrets excluded from version control
- ✅ No sensitive data in commit history

### Deployment Security
- ✅ Environment-based configuration
- ✅ Secure secrets management in production
- ✅ HTTPS enforcement (handled by Streamlit Community Cloud)

## 🚨 Security Checklist

Before deploying or sharing your repository:

- [ ] Verify no API keys are hardcoded in source files
- [ ] Ensure `.env` and `.streamlit/secrets.toml` are in `.gitignore`
- [ ] Check git history for accidentally committed secrets
- [ ] Test application works with environment variables
- [ ] Configure secrets in Streamlit Community Cloud before deployment

## 🔍 Security Audit Commands

Run these commands to check for potential security issues:

```bash
# Check for potential API keys in code
grep -r "sk-\|gsk_\|pc-\|AIza" . --exclude-dir=.git

# Check for hardcoded secrets patterns
grep -r "api_key\|secret\|password\|token" . --include="*.py" --exclude-dir=.git

# Verify .gitignore is working
git status --ignored
```

## 📞 Security Contact

If you discover a security vulnerability, please report it responsibly:
- Do not create public issues for security vulnerabilities
- Contact the repository maintainer directly
- Provide detailed information about the vulnerability

## 🔄 Regular Security Maintenance

- Regularly rotate API keys
- Monitor API usage for unusual activity
- Keep dependencies updated
- Review access logs periodically
- Audit code changes for security implications