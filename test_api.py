"""
Comprehensive API Testing Script
This script tests all major API endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
API_V1 = f"{BASE_URL}/api/v1"

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(name: str):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Testing: {name}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

def print_success(msg: str):
    print(f"{GREEN}✓ {msg}{RESET}")

def print_error(msg: str):
    print(f"{RED}✗ {msg}{RESET}")

def print_info(msg: str):
    print(f"{YELLOW}ℹ {msg}{RESET}")

def test_health():
    """Test health check endpoint"""
    print_test("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/healthz")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check passed: {data}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {str(e)}")
        return False

def test_register_user():
    """Test user registration"""
    print_test("User Registration")
    try:
        payload = {
            "email": f"testuser_{datetime.now().timestamp()}@example.com",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        response = requests.post(f"{API_V1}/auth/register", json=payload)
        print_info(f"Status Code: {response.status_code}")
        print_info(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                print_success("User registered successfully")
                return data.get("access_token"), payload["email"], payload["password"]
            else:
                print_error("No access token in response")
                return None, None, None
        else:
            print_error(f"Registration failed with status {response.status_code}")
            return None, None, None
    except Exception as e:
        print_error(f"Registration error: {str(e)}")
        return None, None, None

def test_login(email: str, password: str):
    """Test user login"""
    print_test("User Login")
    try:
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(f"{API_V1}/auth/login", json=payload)
        print_info(f"Status Code: {response.status_code}")
        print_info(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                print_success("Login successful")
                return data.get("access_token")
            else:
                print_error("No access token in response")
                return None
        else:
            print_error(f"Login failed with status {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Login error: {str(e)}")
        return None

def test_api_routes():
    """Test available API routes"""
    print_test("API Routes Discovery")
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        if response.status_code == 200:
            data = response.json()
            print_success("OpenAPI schema retrieved")
            paths = data.get("paths", {})
            print_info(f"Found {len(paths)} API endpoints:")
            for path in list(paths.keys())[:10]:  # Show first 10
                print(f"  - {path}")
            return True
        else:
            print_error(f"Failed to get OpenAPI schema: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"API routes discovery error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}AI MARKING SYSTEM - COMPREHENSIVE API TEST SUITE{RESET}")
    print(f"{BLUE}Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    results = {
        "health": test_health(),
        "api_routes": test_api_routes(),
    }
    
    # Register and login
    token, email, password = test_register_user()
    if token:
        results["registration"] = True
        login_token = test_login(email, password)
        results["login"] = bool(login_token)
    else:
        results["registration"] = False
        results["login"] = False
    
    # Summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}TEST SUMMARY{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        status = f"{GREEN}PASSED{RESET}" if result else f"{RED}FAILED{RESET}"
        print(f"{test_name.upper()}: {status}")
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"Total: {passed_tests}/{total_tests} tests passed")
    print(f"Completion: {(passed_tests/total_tests)*100:.1f}%")
    print(f"{BLUE}{'='*60}{RESET}\n")

if __name__ == "__main__":
    run_all_tests()
