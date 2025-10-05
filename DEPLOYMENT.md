# Deployment Guide

## 🚀 Streamlit Community Cloud Deployment

This guide walks you through deploying your CitySense application to Streamlit Community Cloud while maintaining security best practices.

### Prerequisites

1. **GitHub Repository**: Your code must be in a GitHub repository
2. **Streamlit Community Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **API Keys**: Have your OpenAI, Gemini, and Pinecone API keys ready

### Step 1: Prepare Your Repository

1. **Ensure Security**:
   ```bash
   # Verify no secrets are committed
   git log --all --full-history -- "*.env" "*.toml" "*secrets*"
   
   # Check current status
   git status --ignored
   ```

2. **Verify Required Files**:
   - ✅ `requirements.txt` (dependencies)
   - ✅ `app.py` (main application)
   - ✅ `.gitignore` (excludes sensitive files)
   - ✅ `README.md` (documentation)
   - ✅ `SECURITY.md` (security guidelines)

### Step 2: Create GitHub Repository

1. **Create a new private repository** on GitHub
2. **Push your code**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: CitySense application"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

### Step 3: Deploy to Streamlit Community Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Click "New app"**
3. **Connect your GitHub repository**:
   - Repository: `yourusername/your-repo-name`
   - Branch: `main`
   - Main file path: `app.py`

4. **Configure Advanced Settings**:
   - Python version: `3.9` or higher
   - Keep default settings for other options

### Step 4: Configure Secrets

1. **In your Streamlit app dashboard**, click on your app
2. **Go to "Settings" → "Secrets"**
3. **Add your secrets in TOML format**:

```toml
# Add these secrets in the Streamlit Community Cloud secrets section
OPENAI_API_KEY = "your_openai_api_key_here"
GEMINI_API_KEY = "your_gemini_api_key_here"
PINECONE_API_KEY = "your_pinecone_api_key_here"
```

4. **Click "Save"**

### Step 5: Deploy and Test

1. **Click "Deploy"**
2. **Wait for deployment** (usually 2-5 minutes)
3. **Test your application**:
   - Verify API status shows ✅ for configured services
   - Test chat functionality
   - Check vector database integration

### Step 6: Make Repository Public (Optional)

If you want to make your repository public while keeping secrets secure:

1. **Verify security checklist**:
   - [ ] No API keys in code or commit history
   - [ ] `.gitignore` properly configured
   - [ ] Secrets only in Streamlit Community Cloud
   - [ ] Security documentation complete

2. **Change repository visibility**:
   - Go to GitHub repository settings
   - Scroll to "Danger Zone"
   - Click "Change repository visibility"
   - Select "Make public"

## 🔧 Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   - Check `requirements.txt` has all dependencies
   - Verify Python version compatibility

2. **API connection failures**:
   - Verify secrets are correctly configured
   - Check API key validity
   - Ensure no extra spaces in secret values

3. **Streamlit app won't start**:
   - Check logs in Streamlit Community Cloud dashboard
   - Verify `app.py` is the correct entry point
   - Check for syntax errors

### Debugging Steps

1. **Check application logs**:
   - Go to your app in Streamlit Community Cloud
   - Click "Manage app" → "Logs"

2. **Test locally first**:
   ```bash
   streamlit run app.py
   ```

3. **Verify dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🔄 Updates and Maintenance

### Updating Your App

1. **Make changes locally**
2. **Test thoroughly**
3. **Commit and push to GitHub**:
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push
   ```
4. **Streamlit Community Cloud will auto-deploy**

### Managing Secrets

- **Rotate API keys regularly**
- **Update secrets in Streamlit Community Cloud dashboard**
- **Never commit secrets to repository**

## 🌐 Custom Domain (Optional)

Streamlit Community Cloud provides a default URL like:
`https://your-app-name-your-username.streamlit.app`

For custom domains, consider:
- Streamlit for Teams (paid plan)
- Reverse proxy setup
- Alternative hosting platforms

## 📊 Monitoring

- **Monitor API usage** through provider dashboards
- **Check application logs** regularly
- **Monitor performance** and user feedback
- **Set up alerts** for critical issues

## 🔒 Security Maintenance

- **Regular security audits**
- **Dependency updates**
- **API key rotation**
- **Access log monitoring**

## 📞 Support

- **Streamlit Community**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **Documentation**: [docs.streamlit.io](https://docs.streamlit.io)
- **GitHub Issues**: For application-specific issues