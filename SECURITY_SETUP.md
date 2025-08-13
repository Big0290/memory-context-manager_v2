# 🔒 Security Setup Guide

## 🚨 **CRITICAL: Environment Variables Required**

Your `docker-compose.yml` has been sanitized and now requires environment variables to be set.

---

## 📋 **REQUIRED SETUP:**

### **1. Create .env file:**

```bash
# Copy the template
cp env.template .env

# Edit with your actual values
nano .env
```

### **2. Fill in your actual values:**

```bash
# Google Custom Search API
GOOGLE_CUSTOM_SEARCH_API_KEY=AIzaSyB_k-j9MKKr-tNiTa-qvWod2EeKc5E7cfQ
GOOGLE_CUSTOM_SEARCH_ENGINE_ID=c740d6e6b33e947e7

# WebUI Secret Key (generate a secure one)
WEBUI_SECRET_KEY=your_actual_secret_key_here

# Optional: Bing Search API
BING_SEARCH_API_KEY=your_bing_api_key_here
```

---

## 🔐 **SECURITY BEST PRACTICES:**

### **✅ DO:**

- Use `.env` file for sensitive data
- Keep `.env` in `.gitignore`
- Use strong, unique secret keys
- Rotate API keys regularly

### **❌ DON'T:**

- Commit API keys to git
- Share `.env` files
- Use weak secret keys
- Expose keys in docker-compose.yml

---

## 🚀 **STARTING THE SYSTEM:**

```bash
# 1. Set up environment variables
cp env.template .env
# Edit .env with your actual values

# 2. Start the system
docker-compose up -d

# 3. Verify it's working
docker-compose logs memory_mcp_server
```

---

## 🔍 **VERIFICATION:**

After setup, verify no sensitive data is exposed:

```bash
# Check docker-compose.yml (should show ${VARIABLE_NAME})
grep -r "AIzaSy\|your-secret" docker-compose.yml

# Check environment variables are loaded
docker-compose exec memory_mcp_server env | grep GOOGLE
```

---

## 🆘 **TROUBLESHOOTING:**

If you get errors about missing environment variables:

1. Ensure `.env` file exists
2. Check all required variables are set
3. Restart docker-compose after changes
4. Verify no typos in variable names

---

**🔒 Your system is now secure and follows security best practices!**
