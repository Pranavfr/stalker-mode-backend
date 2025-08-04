# OSINT Backend Deployment Guide

## Railway Deployment

### Prerequisites
- GitHub account
- Railway account (free tier available)

### Step 1: Prepare Your Repository

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial OSINT backend commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/osint-backend.git
   git push -u origin main
   ```

### Step 2: Deploy to Railway

1. **Connect to Railway:**
   - Go to [Railway.app](https://railway.app)
   - Sign in with your GitHub account
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `osint-backend` repository

2. **Configure Environment Variables:**
   - In your Railway project dashboard, go to "Variables"
   - Add the following environment variables:
   ```
   EMAILREP_API_KEY=your_emailrep_api_key_here
   ALLOWED_ORIGINS=https://your-frontend.vercel.app
   ```

3. **Deploy:**
   - Railway will automatically detect the Python project
   - It will use the `Procfile` and `runtime.txt` for configuration
   - The deployment will start automatically

### Step 3: Verify Deployment

1. **Check the deployment logs** in Railway dashboard
2. **Test the health endpoint:**
   ```bash
   curl https://your-app-name.railway.app/health
   ```

3. **Test all endpoints:**
   ```bash
   # Email analysis
   curl "https://your-app-name.railway.app/api/email?email=test@example.com"
   
   # Domain WHOIS
   curl "https://your-app-name.railway.app/api/domain?domain=google.com"
   
   # IP geolocation
   curl "https://your-app-name.railway.app/api/ip?ip=8.8.8.8"
   
   # Social media discovery
   curl "https://your-app-name.railway.app/api/sherlock?username=testuser123"
   ```

### Step 4: Connect to Frontend

1. **Update your React frontend** to use the Railway URL:
   ```javascript
   const API_BASE_URL = 'https://your-app-name.railway.app';
   ```

2. **Test CORS** by making requests from your Vercel frontend

## Environment Variables

### Required Variables
- `PORT`: Railway sets this automatically
- `HOST`: Railway sets this automatically

### Optional Variables
- `EMAILREP_API_KEY`: API key for emailrep.io (free tier available)
- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins

## Monitoring

### Railway Dashboard
- **Logs**: View real-time application logs
- **Metrics**: Monitor CPU, memory, and network usage
- **Deployments**: Track deployment history

### Health Checks
- The `/health` endpoint provides basic health monitoring
- Railway automatically monitors the application

## Troubleshooting

### Common Issues

1. **Build Failures:**
   - Check that all dependencies are in `requirements.txt`
   - Verify Python version in `runtime.txt`

2. **Runtime Errors:**
   - Check Railway logs for error messages
   - Verify environment variables are set correctly

3. **CORS Issues:**
   - Ensure `ALLOWED_ORIGINS` includes your frontend URL
   - Check that the frontend is making requests to the correct URL

4. **API Timeouts:**
   - Sherlock endpoint has a 5-minute timeout
   - Other endpoints have 10-second timeouts

### Debugging

1. **Local Testing:**
   ```bash
   python app.py
   python test_backend.py
   ```

2. **Railway Logs:**
   - Use Railway dashboard to view real-time logs
   - Check for any error messages or warnings

## Performance Optimization

### For Production
1. **Enable caching** for external API calls
2. **Implement rate limiting** to prevent abuse
3. **Add monitoring** for API usage
4. **Consider upgrading** Railway plan for better performance

### Sherlock Integration
- The current implementation uses mock responses
- To enable real Sherlock functionality:
  1. Install Sherlock in the Railway environment
  2. Update the Sherlock route to use subprocess calls
  3. Handle timeouts and errors appropriately

## Security Considerations

1. **API Keys:** Store sensitive keys in Railway environment variables
2. **CORS:** Only allow trusted origins
3. **Rate Limiting:** Implement to prevent abuse
4. **Input Validation:** All endpoints validate input parameters
5. **Error Handling:** Sensitive information is not exposed in error messages

## Support

If you encounter issues:
1. Check the Railway logs
2. Verify all environment variables are set
3. Test endpoints locally first
4. Review the README.md for detailed API documentation 