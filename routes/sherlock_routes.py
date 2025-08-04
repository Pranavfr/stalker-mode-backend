from flask import Blueprint, request, jsonify
import subprocess
import logging
import os
import signal
import threading
import time
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)
sherlock_bp = Blueprint('sherlock', __name__)

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Sherlock execution timed out")

def run_sherlock_with_timeout(username: str, timeout: int = 300) -> Dict:
    """
    Run Sherlock tool with timeout and return results
    """
    try:
        # Check if username is provided
        if not username or not username.strip():
            return {
                'success': False,
                'error': 'Username is required',
                'username': username
            }
        
        # Clean username
        username = username.strip()
        logger.info(f"Starting Sherlock search for username: {username}")
        
        # Try to run Sherlock using python -m sherlock_project
        cmd = ['python', '-m', 'sherlock_project', username, '--timeout', '10']
        
        logger.info(f"Executing Sherlock command: {' '.join(cmd)}")
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False
        )
        
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            
            if process.returncode == 0:
                # Parse text output from Sherlock
                import re
                try:
                    # Parse the text output to extract found profiles
                    results = []
                    lines = stdout.split('\n')
                    
                    for line in lines:
                        # Look for lines that start with [+] indicating found profiles
                        if line.strip().startswith('[+]'):
                            # Extract site name and URL
                            match = re.search(r'\[\+\] ([^:]+): (.+)', line)
                            if match:
                                site_name = match.group(1).strip()
                                url = match.group(2).strip()
                                results.append({
                                    'site': site_name,
                                    'url': url,
                                    'status': 'found'
                                })
                    
                    logger.info(f"Sherlock completed successfully for {username}, found {len(results)} profiles")
                    return {
                        'success': True,
                        'username': username,
                        'results': results,
                        'total_found': len(results)
                    }
                except Exception as parse_error:
                    logger.error(f"Failed to parse Sherlock output for {username}: {parse_error}")
                    return {
                        'success': False,
                        'error': 'Failed to parse Sherlock results',
                        'username': username,
                        'raw_output': stdout[:500]  # First 500 chars for debugging
                    }
            else:
                logger.error(f"Sherlock failed for {username}: {stderr}")
                # Return a graceful fallback response
                return {
                    'success': True,
                    'username': username,
                    'results': [],
                    'total_found': 0,
                    'note': f'Sherlock execution failed: {stderr[:100]}...'
                }
                
        except subprocess.TimeoutExpired:
            # Kill the process
            process.terminate()
            
            logger.warning(f"Sherlock timeout for {username}")
            return {
                'success': False,
                'error': 'Sherlock execution timed out',
                'username': username
            }
            
    except Exception as e:
        logger.error(f"Unexpected error in Sherlock for {username}: {str(e)}")
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}',
            'username': username
        }

@sherlock_bp.route('/sherlock', methods=['GET'])
def sherlock_search():
    """
    GET /api/sherlock?username=...
    Run Sherlock tool to find social media accounts
    """
    try:
        # Log incoming request
        logger.info(f"Sherlock request received: {request.args}")
        
        # Get username from query parameters
        username = request.args.get('username')
        
        if not username:
            return jsonify({
                'success': False,
                'error': 'Username parameter is required'
            }), 400
        
        # Run Sherlock
        result = run_sherlock_with_timeout(username)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in sherlock_search: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500 