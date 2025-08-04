# OSINT Dashboard Backend

A Flask-based REST API backend for an OSINT (Open Source Intelligence) Dashboard. This backend provides endpoints for social media account discovery, email analysis, domain WHOIS lookup, and IP geolocation.

## Features

- **Social Media Discovery**: Run Sherlock tool to find social media accounts by username
- **Email Analysis**: Get Gravatar URL and email reputation from emailrep.io
- **Domain WHOIS**: Retrieve comprehensive WHOIS data for domains
- **IP Geolocation**: Get detailed geolocation and ISP information for IP addresses
- **Production Ready**: Configured for Railway deployment with proper error handling and logging

## API Endpoints

### 1. Social Media Discovery
```
GET /api/sherlock?username=<username>
```
Runs the Sherlock tool to find social media accounts associated with a username.

**Response:**
```json
{
  "success": true,
  "username": "johndoe",
  "results": [...],
  "total_found": 15
}
```

### 2. Email Analysis
```
GET /api/email?email=<email_address>
```
Returns Gravatar URL and email reputation data.

**Response:**
```json
{
  "success": true,
  "email": "user@example.com",
  "gravatar_url": "https://www.gravatar.com/avatar/...",
  "reputation": {
    "email": "user@example.com",
    "reputation": "good",
    "suspicious": false,
    "references": 5
  }
}
```

### 3. Domain WHOIS
```
GET /api/domain?domain=<domain_name>
```
Returns comprehensive WHOIS data for a domain.

**Response:**
```json
{
  "success": true,
  "domain": "example.com",
  "ip_address": "93.184.216.34",
  "whois_data": {
    "registrar": "ICANN",
    "creation_date": "1995-08-14T04:00:00Z",
    "expiration_date": "2024-08-13T04:00:00Z",
    "status": ["clientTransferProhibited"],
    "name_servers": ["a.iana-servers.net", "b.iana-servers.net"]
  }
}
```

### 4. IP Geolocation
```
GET /api/ip?ip=<ip_address>
```
Returns detailed geolocation and ISP information for an IP address.

**Response:**
```json
{
  "success": true,
  "ip": "8.8.8.8",
  "geolocation": {
    "country": "United States",
    "city": "Mountain View",
    "region": "California",
    "isp": "Google LLC",
    "latitude": 37.4056,
    "longitude": -122.0775
  }
}
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- Sherlock tool (for social media discovery)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd osint-backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Sherlock (optional - for social media discovery):**
   ```bash
   pip install sherlock-project
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

### Environment Variables

Create a `.env` file with the following variables:

```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False

# API Keys (optional)
EMAILREP_API_KEY=your_emailrep_api_key_here

# Server Configuration
PORT=5000
HOST=0.0.0.0

# CORS Origins
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,https://your-frontend.vercel.app

# Logging
LOG_LEVEL=INFO
```

### Running Locally

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Testing Endpoints

```bash
# Health check
curl http://localhost:5000/health

# Social media discovery
curl "http://localhost:5000/api/sherlock?username=johndoe"

# Email analysis
curl "http://localhost:5000/api/email?email=user@example.com"

# Domain WHOIS
curl "http://localhost:5000/api/domain?domain=example.com"

# IP geolocation
curl "http://localhost:5000/api/ip?ip=8.8.8.8"
```

## Deployment

### Railway Deployment

1. **Connect your repository to Railway**
2. **Set environment variables in Railway dashboard**
3. **Deploy automatically on push**

The application is configured with:
- `Procfile` for Railway deployment
- `runtime.txt` specifying Python version
- Gunicorn as WSGI server
- Proper CORS configuration for Vercel frontend

### Environment Variables for Production

Set these in your Railway dashboard:

- `EMAILREP_API_KEY` (optional)
- `ALLOWED_ORIGINS` (your Vercel frontend URL)

## Error Handling

All endpoints include comprehensive error handling:

- **400 Bad Request**: Invalid parameters
- **404 Not Found**: Endpoint not found
- **500 Internal Server Error**: Server-side errors

Error responses follow this format:
```json
{
  "success": false,
  "error": "Error description"
}
```

## Logging

The application logs all requests and errors for debugging:

- Request logging for all endpoints
- Error logging with stack traces
- Timeout handling for long-running operations

## Security Features

- CORS configuration for frontend access
- Input validation for all parameters
- Timeout protection for external API calls
- Error message sanitization

## Dependencies

- **Flask**: Web framework
- **flask-cors**: CORS support
- **python-dotenv**: Environment variable management
- **requests**: HTTP client for external APIs
- **python-whois**: WHOIS data retrieval
- **gunicorn**: WSGI server for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details 