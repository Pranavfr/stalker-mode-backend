from flask import Blueprint, request, jsonify
import requests
import hashlib
import logging
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)
email_bp = Blueprint('email', __name__)

def get_gravatar_url(email: str, size: int = 200) -> str:
    """
    Generate Gravatar URL for email address
    """
    try:
        # Create MD5 hash of email (lowercase)
        email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=404"
    except Exception as e:
        logger.error(f"Error generating Gravatar URL for {email}: {str(e)}")
        return ""

def get_email_reputation(email: str) -> Dict:
    """
    Get email reputation from emailrep.io API
    """
    try:
        # Get API key from environment
        api_key = os.getenv('EMAILREP_API_KEY')
        
        headers = {
            'User-Agent': 'OSINT-Dashboard/1.0'
        }
        
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
        
        # Make request to emailrep.io
        response = requests.get(
            f'https://emailrep.io/{email}',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Email reputation retrieved for {email}")
            return {
                'success': True,
                'email': email,
                'reputation': data
            }
        elif response.status_code == 404:
            logger.warning(f"Email not found in reputation database: {email}")
            return {
                'success': True,
                'email': email,
                'reputation': {
                    'email': email,
                    'reputation': 'unknown',
                    'suspicious': False,
                    'references': 0
                }
            }
        else:
            logger.error(f"Emailrep API error for {email}: {response.status_code}")
            return {
                'success': False,
                'error': f'Emailrep API error: {response.status_code}',
                'email': email
            }
            
    except requests.exceptions.Timeout:
        logger.error(f"Emailrep API timeout for {email}")
        return {
            'success': False,
            'error': 'Emailrep API timeout',
            'email': email
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Emailrep API request error for {email}: {str(e)}")
        return {
            'success': False,
            'error': f'Emailrep API request error: {str(e)}',
            'email': email
        }
    except Exception as e:
        logger.error(f"Unexpected error getting email reputation for {email}: {str(e)}")
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}',
            'email': email
        }

def validate_email(email: str) -> bool:
    """
    Basic email validation
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@email_bp.route('/email', methods=['GET'])
def email_lookup():
    """
    GET /api/email?email=...
    Return Gravatar URL and email reputation
    """
    try:
        # Log incoming request
        logger.info(f"Email lookup request received: {request.args}")
        
        # Get email from query parameters
        email = request.args.get('email')
        
        if not email:
            return jsonify({
                'success': False,
                'error': 'Email parameter is required'
            }), 400
        
        # Clean and validate email
        email = email.strip().lower()
        
        if not validate_email(email):
            return jsonify({
                'success': False,
                'error': 'Invalid email format'
            }), 400
        
        # Get Gravatar URL
        gravatar_url = get_gravatar_url(email)
        
        # Get email reputation
        reputation_result = get_email_reputation(email)
        
        # Combine results
        result = {
            'success': True,
            'email': email,
            'gravatar_url': gravatar_url,
            'reputation': reputation_result.get('reputation', {}) if reputation_result['success'] else None,
            'reputation_error': reputation_result.get('error') if not reputation_result['success'] else None
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in email_lookup: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500 