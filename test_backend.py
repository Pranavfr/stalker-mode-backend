#!/usr/bin/env python3
"""
Test script for OSINT Backend
Run this to verify all endpoints are working correctly
"""

import requests
import json
import sys
from urllib.parse import urljoin

# Configuration
BASE_URL = "http://localhost:5000"
TEST_EMAIL = "test@example.com"
TEST_DOMAIN = "google.com"
TEST_IP = "8.8.8.8"
TEST_USERNAME = "testuser123"

def test_health():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_email_endpoint():
    """Test email analysis endpoint"""
    print(f"🔍 Testing email endpoint with {TEST_EMAIL}...")
    try:
        response = requests.get(f"{BASE_URL}/api/email?email={TEST_EMAIL}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Email endpoint passed")
                print(f"   Gravatar URL: {data.get('gravatar_url', 'N/A')}")
                return True
            else:
                print(f"❌ Email endpoint failed: {data.get('error')}")
                return False
        else:
            print(f"❌ Email endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Email endpoint error: {e}")
        return False

def test_domain_endpoint():
    """Test domain WHOIS endpoint"""
    print(f"🔍 Testing domain endpoint with {TEST_DOMAIN}...")
    try:
        response = requests.get(f"{BASE_URL}/api/domain?domain={TEST_DOMAIN}", timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Domain endpoint passed")
                print(f"   IP Address: {data.get('ip_address', 'N/A')}")
                return True
            else:
                print(f"❌ Domain endpoint failed: {data.get('error')}")
                return False
        else:
            print(f"❌ Domain endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Domain endpoint error: {e}")
        return False

def test_ip_endpoint():
    """Test IP geolocation endpoint"""
    print(f"🔍 Testing IP endpoint with {TEST_IP}...")
    try:
        response = requests.get(f"{BASE_URL}/api/ip?ip={TEST_IP}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ IP endpoint passed")
                geolocation = data.get('geolocation', {})
                print(f"   Country: {geolocation.get('country', 'N/A')}")
                print(f"   City: {geolocation.get('city', 'N/A')}")
                return True
            else:
                print(f"❌ IP endpoint failed: {data.get('error')}")
                return False
        else:
            print(f"❌ IP endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ IP endpoint error: {e}")
        return False

def test_sherlock_endpoint():
    """Test Sherlock endpoint (may take longer)"""
    print(f"🔍 Testing Sherlock endpoint with {TEST_USERNAME}...")
    print("   Note: This may take up to 5 minutes...")
    try:
        response = requests.get(f"{BASE_URL}/api/sherlock?username={TEST_USERNAME}", timeout=300)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Sherlock endpoint passed")
                print(f"   Total found: {data.get('total_found', 0)}")
                return True
            else:
                print(f"❌ Sherlock endpoint failed: {data.get('error')}")
                return False
        else:
            print(f"❌ Sherlock endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Sherlock endpoint error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting OSINT Backend Tests")
    print("=" * 50)
    
    tests = [
        test_health,
        test_email_endpoint,
        test_domain_endpoint,
        test_ip_endpoint,
        test_sherlock_endpoint
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready for deployment.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the backend configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 