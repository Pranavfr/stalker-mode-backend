from flask import Blueprint, request, jsonify
import requests
import logging
from typing import Dict, Optional
import ipaddress

logger = logging.getLogger(__name__)
ip_bp = Blueprint('ip', __name__)

def validate_ip(ip: str) -> bool:
    """
    Validate IP address format
    """
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def get_ip_geolocation(ip: str) -> Dict:
    """
    Get IP geolocation data from ipwho.is API
    """
    try:
        logger.info(f"Starting IP geolocation lookup for: {ip}")
        
        # Make request to ipwho.is API
        response = requests.get(
            f'https://ipwho.is/{ip}',
            headers={
                'User-Agent': 'OSINT-Dashboard/1.0'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if the API returned an error
            if data.get('success') == False:
                logger.error(f"IPwho.is API error for {ip}: {data.get('message', 'Unknown error')}")
                return {
                    'success': False,
                    'error': data.get('message', 'IPwho.is API error'),
                    'ip': ip
                }
            
            # Extract relevant information
            geolocation_data = {
                'ip': data.get('ip'),
                'type': data.get('type'),  # ipv4 or ipv6
                'continent': data.get('continent'),
                'continent_code': data.get('continent_code'),
                'country': data.get('country'),
                'country_code': data.get('country_code'),
                'region': data.get('region'),
                'region_code': data.get('region_code'),
                'city': data.get('city'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'timezone': {
                    'id': data.get('timezone', {}).get('id'),
                    'abbr': data.get('timezone', {}).get('abbr'),
                    'utc': data.get('timezone', {}).get('utc'),
                    'current_time': data.get('timezone', {}).get('current_time')
                },
                'isp': data.get('connection', {}).get('isp'),
                'org': data.get('connection', {}).get('org'),
                'as': data.get('connection', {}).get('as'),
                'asname': data.get('connection', {}).get('asname'),
                'domain': data.get('connection', {}).get('domain'),
                'mobile': data.get('connection', {}).get('mobile'),
                'proxy': data.get('connection', {}).get('proxy'),
                'hosting': data.get('connection', {}).get('hosting'),
                'vpn': data.get('connection', {}).get('vpn'),
                'tor': data.get('connection', {}).get('tor'),
                'relay': data.get('connection', {}).get('relay'),
                'service': data.get('connection', {}).get('service'),
                'postal': data.get('postal'),
                'calling_code': data.get('calling_code'),
                'flag': data.get('flag'),
                'flag_img': data.get('flag_img'),
                'flag_emoji': data.get('flag_emoji'),
                'flag_emoji_unicode': data.get('flag_emoji_unicode'),
                'currency': {
                    'name': data.get('currency', {}).get('name'),
                    'code': data.get('currency', {}).get('code'),
                    'symbol': data.get('currency', {}).get('symbol'),
                    'plural': data.get('currency', {}).get('plural'),
                    'exchange_rate': data.get('currency', {}).get('exchange_rate')
                },
                'security': {
                    'anonymous': data.get('security', {}).get('anonymous'),
                    'proxy': data.get('security', {}).get('proxy'),
                    'vpn': data.get('security', {}).get('vpn'),
                    'tor': data.get('security', {}).get('tor'),
                    'relay': data.get('security', {}).get('relay'),
                    'hosting': data.get('security', {}).get('hosting'),
                    'service': data.get('security', {}).get('service')
                }
            }
            
            # Clean up None values
            cleaned_data = {}
            for key, value in geolocation_data.items():
                if value is not None:
                    if isinstance(value, dict):
                        # Clean nested dictionaries
                        cleaned_nested = {k: v for k, v in value.items() if v is not None}
                        if cleaned_nested:
                            cleaned_data[key] = cleaned_nested
                    else:
                        cleaned_data[key] = value
            
            logger.info(f"IP geolocation lookup completed for {ip}")
            return {
                'success': True,
                'geolocation_data': cleaned_data
            }
            
        elif response.status_code == 404:
            logger.warning(f"IP not found in geolocation database: {ip}")
            return {
                'success': False,
                'error': 'IP not found in geolocation database',
                'ip': ip
            }
        else:
            logger.error(f"IPwho.is API error for {ip}: {response.status_code}")
            return {
                'success': False,
                'error': f'IPwho.is API error: {response.status_code}',
                'ip': ip
            }
            
    except requests.exceptions.Timeout:
        logger.error(f"IPwho.is API timeout for {ip}")
        return {
            'success': False,
            'error': 'IPwho.is API timeout',
            'ip': ip
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"IPwho.is API request error for {ip}: {str(e)}")
        return {
            'success': False,
            'error': f'IPwho.is API request error: {str(e)}',
            'ip': ip
        }
    except Exception as e:
        logger.error(f"Unexpected error getting IP geolocation for {ip}: {str(e)}")
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}',
            'ip': ip
        }

@ip_bp.route('/ip', methods=['GET'])
def ip_lookup():
    """
    GET /api/ip?ip=...
    Return IP geolocation information
    """
    try:
        # Log incoming request
        logger.info(f"IP lookup request received: {request.args}")
        
        # Get IP from query parameters
        ip = request.args.get('ip')
        
        if not ip:
            return jsonify({
                'success': False,
                'error': 'IP parameter is required'
            }), 400
        
        # Clean IP
        ip = ip.strip()
        
        # Validate IP format
        if not validate_ip(ip):
            return jsonify({
                'success': False,
                'error': 'Invalid IP address format'
            }), 400
        
        # Get geolocation data
        geolocation_result = get_ip_geolocation(ip)
        
        # Prepare response
        if geolocation_result['success']:
            result = {
                'success': True,
                'ip': ip,
                'geolocation': geolocation_result['geolocation_data']
            }
            return jsonify(result), 200
        else:
            return jsonify(geolocation_result), 500
        
    except Exception as e:
        logger.error(f"Error in ip_lookup: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500 