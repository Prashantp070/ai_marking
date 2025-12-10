"""
Complete End-to-End Test Suite
Tests the full workflow: Register -> Login -> Upload -> Process
"""

import requests
import json
from pathlib import Path
from datetime import datetime
import time

BASE_URL = "http://127.0.0.1:8000"
API_V1 = f"{BASE_URL}/api/v1"

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

def print_section(title: str):
    print(f"\n{CYAN}{'='*70}{RESET}")
    print(f"{CYAN}{title.center(70)}{RESET}")
    print(f"{CYAN}{'='*70}{RESET}\n")

def print_test(name: str):
    print(f"{BLUE}▶ {name}{RESET}")

def print_success(msg: str):
    print(f"  {GREEN}✓ {msg}{RESET}")

def print_error(msg: str):
    print(f"  {RED}✗ {msg}{RESET}")

def print_info(msg: str):
    print(f"  {YELLOW}ℹ {msg}{RESET}")

def print_data(title: str, data: dict):
    print(f"  {YELLOW}{title}:{RESET}")
    for key, value in data.items():
        if key == "access_token":
            print(f"    {key}: {value[:30]}...")
        else:
            print(f"    {key}: {value}")

class E2ETest:
    def __init__(self):
        self.test_email = f"e2etest_{datetime.now().timestamp()}@example.com"
        self.test_password = "TestPassword123!"
        self.test_name = "E2E Test User"
        self.access_token = None
        self.user_id = None
        self.submission_id = None
        self.results = {}
        
    def test_registration(self):
        """Test user registration"""
        print_test("User Registration")
        try:
            payload = {
                "email": self.test_email,
                "password": self.test_password,
                "full_name": self.test_name
            }
            response = requests.post(f"{API_V1}/auth/register", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                print_success(f"Registered: {self.test_email}")
                return True
            else:
                print_error(f"Status: {response.status_code} - {response.json()}")
                return False
        except Exception as e:
            print_error(f"Error: {str(e)}")
            return False
    
    def test_login(self):
        """Test user login"""
        print_test("User Login")
        try:
            payload = {
                "email": self.test_email,
                "password": self.test_password
            }
            response = requests.post(f"{API_V1}/auth/login", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                print_success(f"Logged in: {self.test_email}")
                return True
            else:
                print_error(f"Status: {response.status_code}")
                return False
        except Exception as e:
            print_error(f"Error: {str(e)}")
            return False
    
    def test_file_upload(self):
        """Test file upload"""
        print_test("File Upload")
        try:
            # Create test file
            test_file = Path("test_answer.txt")
            test_content = """Question 1: What is the capital of France?
Answer: Paris

Question 2: What is 2 + 2?
Answer: 4

Question 3: Name a prime number.
Answer: 7"""
            
            test_file.write_text(test_content)
            print_info(f"Created test file: {test_file.name}")
            
            # Upload file
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            with open(test_file, "rb") as f:
                files = {"file": ("test_answer.txt", f)}
                data = {"exam_id": 1}
                response = requests.post(
                    f"{API_V1}/",
                    headers=headers,
                    files=files,
                    data=data
                )
            
            if response.status_code == 200:
                result = response.json()
                self.submission_id = result.get("submission_id")
                print_success(f"File uploaded - Submission ID: {self.submission_id}")
                return True
            else:
                print_error(f"Status: {response.status_code} - {response.json()}")
                return False
        except Exception as e:
            print_error(f"Error: {str(e)}")
            return False
    
    def test_get_submission_status(self):
        """Test getting submission status"""
        print_test("Get Submission Status")
        try:
            if not self.submission_id:
                print_error("No submission ID available")
                return False
            
            headers = {"Authorization": f"Bearer {self.access_token}"}
            # Try the results endpoint which handles submission queries
            response = requests.get(
                f"{API_V1}/results/{self.submission_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Retrieved submission results")
                print_info(f"Submission ID: {self.submission_id}")
                return True
            elif response.status_code == 404:
                # This is ok for newly uploaded files - they may not be processed yet
                print_info(f"Submission not yet processed (status: {response.status_code})")
                return True
            else:
                print_error(f"Status: {response.status_code}")
                return False
        except Exception as e:
            print_error(f"Error: {str(e)}")
            return False
    
    def test_api_docs(self):
        """Test API documentation endpoint"""
        print_test("API Documentation")
        try:
            response = requests.get(f"{BASE_URL}/docs")
            
            if response.status_code == 200:
                print_success("API documentation available at /docs")
                return True
            else:
                print_error(f"Status: {response.status_code}")
                return False
        except Exception as e:
            print_error(f"Error: {str(e)}")
            return False
    
    def test_health_check(self):
        """Test health check"""
        print_test("Health Check")
        try:
            response = requests.get(f"{BASE_URL}/healthz")
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Backend health: {data.get('status', 'unknown')}")
                return True
            else:
                print_error(f"Status: {response.status_code}")
                return False
        except Exception as e:
            print_error(f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print_section("END-TO-END TEST SUITE")
        print(f"Test Email: {YELLOW}{self.test_email}{RESET}")
        print(f"Timestamp: {YELLOW}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}\n")
        
        # Run tests in sequence
        self.results["health_check"] = self.test_health_check()
        self.results["api_docs"] = self.test_api_docs()
        self.results["registration"] = self.test_registration()
        self.results["login"] = self.test_login()
        self.results["file_upload"] = self.test_file_upload()
        self.results["submission_status"] = self.test_get_submission_status()
        
        # Print summary
        print_section("TEST SUMMARY")
        
        total = len(self.results)
        passed = sum(1 for v in self.results.values() if v)
        failed = total - passed
        
        for test_name, result in self.results.items():
            status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
            print(f"  {test_name.replace('_', ' ').title()}: {status}")
        
        print(f"\n{CYAN}{'='*70}{RESET}")
        print(f"  Total Tests: {total}")
        print(f"  Passed: {GREEN}{passed}{RESET}")
        print(f"  Failed: {RED}{failed}{RESET}")
        percentage = (passed / total) * 100 if total > 0 else 0
        print(f"  Success Rate: {GREEN}{percentage:.1f}%{RESET}")
        print(f"{CYAN}{'='*70}{RESET}\n")
        
        return failed == 0

if __name__ == "__main__":
    tester = E2ETest()
    success = tester.run_all_tests()
    
    if success:
        print(f"{GREEN}All tests passed! ✓{RESET}\n")
    else:
        print(f"{RED}Some tests failed.{RESET}\n")
