from flask import Blueprint, request, jsonify
import whois
import logging
from typing import Dict, Optional
import socket

logger = logging.getLogger(__name__)
domain_bp = Blueprint('domain', __name__)

def validate_domain(domain: str) -> bool:
    """
    Basic domain validation
    """
    import re
    # Simple domain validation pattern
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    return re.match(pattern, domain) is not None

def get_domain_ip(domain: str) -> Optional[str]:
    """
    Get IP address for domain
    """
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return None
    except Exception as e:
        logger.error(f"Error getting IP for domain {domain}: {str(e)}")
        return None

def get_whois_data(domain: str) -> Dict:
    """
    Get WHOIS data for domain using python-whois
    """
    try:
        logger.info(f"Starting WHOIS lookup for domain: {domain}")
        
        # Perform WHOIS lookup
        w = whois.whois(domain)
        
        # Extract relevant information
        whois_data = {
            'domain': domain,
            'registrar': w.registrar,
            'creation_date': w.creation_date,
            'expiration_date': w.expiration_date,
            'updated_date': w.updated_date,
            'status': w.status,
            'name_servers': w.name_servers,
            'dnssec': w.dnssec,
            'registrant': {
                'name': w.registrant_name,
                'organization': w.registrant_organization,
                'email': w.registrant_email,
                'phone': w.registrant_phone,
                'address': w.registrant_address
            },
            'admin': {
                'name': w.admin_name,
                'organization': w.admin_organization,
                'email': w.admin_email,
                'phone': w.admin_phone,
                'address': w.admin_address
            },
            'tech': {
                'name': w.tech_name,
                'organization': w.tech_organization,
                'email': w.tech_email,
                'phone': w.tech_phone,
                'address': w.tech_address
            }
        }
        
        # Clean up None values
        cleaned_data = {}
        for key, value in whois_data.items():
            if value is not None:
                if isinstance(value, list):
                    # Filter out None values from lists
                    cleaned_value = [item for item in value if item is not None]
                    if cleaned_value:
                        cleaned_data[key] = cleaned_value
                else:
                    cleaned_data[key] = value
        
        logger.info(f"WHOIS lookup completed for {domain}")
        return {
            'success': True,
            'whois_data': cleaned_data
        }
        
    except whois.parser.PywhoisError as e:
        logger.error(f"WHOIS parser error for {domain}: {str(e)}")
        return {
            'success': False,
            'error': f'WHOIS parser error: {str(e)}',
            'domain': domain
        }
    except Exception as e:
        logger.error(f"Unexpected error in WHOIS lookup for {domain}: {str(e)}")
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}',
            'domain': domain
        }

@domain_bp.route('/domain', methods=['GET'])
def domain_lookup():
    """
    GET /api/domain?domain=...
    Return WHOIS data for the domain
    """
    try:
        # Log incoming request
        logger.info(f"Domain lookup request received: {request.args}")
        
        # Get domain from query parameters
        domain = request.args.get('domain')
        
        if not domain:
            return jsonify({
                'success': False,
                'error': 'Domain parameter is required'
            }), 400
        
        # Clean domain
        domain = domain.strip().lower()
        
        # Remove protocol if present
        if domain.startswith(('http://', 'https://')):
            domain = domain.split('://', 1)[1]
        
        # Remove path if present
        domain = domain.split('/')[0]
        
        # Remove port if present
        domain = domain.split(':')[0]
        
        if not validate_domain(domain):
            return jsonify({
                'success': False,
                'error': 'Invalid domain format'
            }), 400
        
        # Get IP address
        ip_address = get_domain_ip(domain)
        
        # Get WHOIS data
        whois_result = get_whois_data(domain)
        
        # Combine results
        result = {
            'success': True,
            'domain': domain,
            'ip_address': ip_address,
            'whois_data': whois_result.get('whois_data', {}) if whois_result['success'] else None,
            'whois_error': whois_result.get('error') if not whois_result['success'] else None
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in domain_lookup: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500 