from flask import Flask
from flask_cors import CORS
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory pattern for Flask app"""
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://*.vercel.app",
        "https://*.railway.app"
    ])
    
    # Register blueprints
    from routes.sherlock_routes import sherlock_bp
    from routes.email_routes import email_bp
    from routes.domain_routes import domain_bp
    from routes.ip_routes import ip_bp
    
    app.register_blueprint(sherlock_bp, url_prefix='/api')
    app.register_blueprint(email_bp, url_prefix='/api')
    app.register_blueprint(domain_bp, url_prefix='/api')
    app.register_blueprint(ip_bp, url_prefix='/api')
    
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return {'status': 'healthy', 'message': 'OSINT Backend is running'}
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Endpoint not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return {'error': 'Internal server error'}, 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 