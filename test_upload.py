"""
File Upload Test Script
"""

import requests
import json
from pathlib import Path
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

def test_file_upload():
    """Test file upload endpoint"""
    print_test("File Upload Functionality")
    
    # First register and login a user
    print_info("Step 1: Registering user...")
    try:
        payload = {
            "email": f"uploadtest_{datetime.now().timestamp()}@example.com",
            "password": "TestPassword123!",
            "full_name": "Upload Test User"
        }
        response = requests.post(f"{API_V1}/auth/register", json=payload)
        if response.status_code != 200:
            print_error(f"Registration failed: {response.status_code}")
            return False
        
        token = response.json().get("access_token")
        print_success(f"User registered successfully")
        
        # Test file upload
        print_info("Step 2: Creating test file...")
        test_file = Path("test_answer_sheet.txt")
        test_file.write_text("This is a test answer sheet\nWith some sample content")
        print_success(f"Test file created: {test_file.absolute()}")
        
        print_info("Step 3: Uploading file...")
        headers = {"Authorization": f"Bearer {token}"}
        
        with open(test_file, "rb") as f:
            files = {"file": ("test_answer_sheet.txt", f)}
            data = {"exam_id": 1}
            response = requests.post(
                f"{API_V1}/",
                headers=headers,
                files=files,
                data=data
            )
        
        print_info(f"Status Code: {response.status_code}")
        print_info(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print_success("File uploaded successfully")
            return True
        else:
            print_error(f"Upload failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Upload test error: {str(e)}")
        return False

if __name__ == "__main__":
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}FILE UPLOAD TEST SUITE{RESET}")
    print(f"{BLUE}Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    result = test_file_upload()
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    if result:
        print(f"{GREEN}File upload test PASSED{RESET}")
    else:
        print(f"{RED}File upload test FAILED{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
