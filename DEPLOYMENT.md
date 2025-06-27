# Deployment Guide - LLM Stock Analyst

This guide explains how to deploy the LLM Stock Analyst backend and connect it to your existing Streamlit frontend at `https://finchanalytics-rag.streamlit.app/`.

## 🚀 Backend Deployment Options

### Option 1: Deploy to Railway (Recommended)

1. **Create Railway Account**
   - Sign up at [railway.app](https://railway.app)
   - Connect your GitHub repository

2. **Deploy Backend**
   ```bash
   # Clone the repository
   git clone <your-repo-url>
   cd llm-stock-analyst
   
   # Deploy to Railway
   railway login
   railway init
   railway up
   ```

3. **Configure Environment Variables**
   - Go to Railway dashboard
   - Add environment variables:
     ```
     OPENAI_API_KEY=your_openai_api_key
     OPENAI_MODEL=gpt-4
     POWERBI_CLIENT_ID=your_powerbi_client_id
     POWERBI_CLIENT_SECRET=your_powerbi_client_secret
     POWERBI_TENANT_ID=your_powerbi_tenant_id
     POWERBI_WORKSPACE_ID=your_powerbi_workspace_id
     ```

4. **Get Backend URL**
   - Railway will provide a URL like: `https://your-app-name.railway.app`
   - Your API will be available at: `https://your-app-name.railway.app/api/v1`

### Option 2: Deploy to Render

1. **Create Render Account**
   - Sign up at [render.com](https://render.com)
   - Connect your GitHub repository

2. **Create Web Service**
   - Choose "Web Service"
   - Select your repository
   - Set build command: `pip install -r backend/requirements.txt`
   - Set start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Configure Environment Variables**
   - Add the same environment variables as above

### Option 3: Deploy to Heroku

1. **Create Heroku Account**
   - Sign up at [heroku.com](https://heroku.com)

2. **Deploy Backend**
   ```bash
   # Install Heroku CLI
   heroku create your-app-name
   git push heroku main
   ```

3. **Configure Environment Variables**
   ```bash
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   heroku config:set OPENAI_MODEL=gpt-4
   # Add other variables...
   ```

## 🔗 Connect Frontend to Backend

### Update Your Streamlit Frontend

1. **Access Your Streamlit App**
   - Go to `https://finchanalytics-rag.streamlit.app/`
   - Navigate to Settings page

2. **Configure Backend URL**
   - In the "Backend API URL" field, enter your deployed backend URL
   - Example: `https://your-app-name.railway.app/api/v1`
   - Click "Save API URL"

3. **Test Connection**
   - Click "Test API Connection" to verify the connection
   - You should see "✅ API connection successful!"

### Alternative: Update Code Directly

If you want to update the code directly in your Streamlit repository:

1. **Update API Configuration**
   ```python
   # In your Streamlit app
   API_BASE_URL = "https://your-app-name.railway.app/api/v1"
   ```

2. **Redeploy Frontend**
   - Commit and push changes to your repository
   - Streamlit Cloud will automatically redeploy

## 🔧 Environment Variables

### Required Variables
```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
```

### Optional Variables
```bash
POWERBI_CLIENT_ID=your_powerbi_client_id
POWERBI_CLIENT_SECRET=your_powerbi_client_secret
POWERBI_TENANT_ID=your_powerbi_tenant_id
POWERBI_WORKSPACE_ID=your_powerbi_workspace_id
```

## 🧪 Testing the Connection

### Test Backend Health
```bash
curl https://your-app-name.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "llm-stock-analyst"
}
```

### Test Chat Endpoint
```bash
curl -X POST https://your-app-name.railway.app/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the current price of AAPL?", "stock_symbol": "AAPL"}'
```

### Test Valuation Endpoint
```bash
curl -X POST https://your-app-name.railway.app/api/v1/valuation \
  -H "Content-Type: application/json" \
  -d '{"stock_symbol": "AAPL", "valuation_methods": ["dcf", "peg", "pe"]}'
```

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure your backend CORS configuration includes your Streamlit URL
   - Check that the frontend URL is exactly: `https://finchanalytics-rag.streamlit.app`

2. **API Connection Failed**
   - Verify the backend URL is correct
   - Check that the backend is running and accessible
   - Test with curl or Postman

3. **Environment Variables Missing**
   - Ensure all required environment variables are set
   - Check the backend logs for missing configuration errors

4. **Timeout Errors**
   - Increase timeout values in the frontend
   - Check backend performance and response times

### Debug Steps

1. **Check Backend Logs**
   ```bash
   # Railway
   railway logs
   
   # Render
   # Check logs in Render dashboard
   
   # Heroku
   heroku logs --tail
   ```

2. **Test API Endpoints**
   - Use the health check endpoint first
   - Test individual endpoints with curl or Postman
   - Check response status codes and error messages

3. **Verify CORS Configuration**
   - Ensure the frontend URL is in the allowed origins
   - Check browser developer tools for CORS errors

## 📊 Monitoring

### Backend Monitoring
- Set up logging and monitoring for your backend
- Monitor API response times and error rates
- Set up alerts for downtime or errors

### Frontend Monitoring
- Monitor user interactions and errors
- Track API call success rates
- Set up error reporting

## 🔄 Updates and Maintenance

### Backend Updates
1. Push changes to your repository
2. Your deployment platform will automatically redeploy
3. Test the updated endpoints

### Frontend Updates
1. Update your Streamlit app code
2. Push to your repository
3. Streamlit Cloud will automatically redeploy

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review backend logs for error messages
3. Test API endpoints individually
4. Verify environment variable configuration
5. Check CORS settings and frontend URL

## 🎯 Next Steps

Once connected:

1. **Test All Features**
   - Chat interface with stock queries
   - Valuation dashboard with different methods
   - Settings and configuration

2. **Customize and Enhance**
   - Add more valuation methods
   - Implement additional data sources
   - Enhance the UI and user experience

3. **Scale and Optimize**
   - Monitor performance
   - Add caching and optimization
   - Implement rate limiting if needed 