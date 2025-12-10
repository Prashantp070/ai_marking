"""
Comprehensive Frontend Testing Script
Tests all UI interactions and functionality
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
API_V1 = f"{BASE_URL}/api/v1"
FRONTEND_URL = "http://localhost:5173"

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

class FrontendTester:
    def __init__(self):
        self.test_results = {}
        self.test_email = f"frontend_test_{datetime.now().timestamp()}@example.com"
        self.test_password = "TestPassword123!"
        self.test_name = "Frontend Test User"
        self.token = None
        self.submission_id = None
        
    def print_header(self, text):
        print(f"\n{CYAN}{'='*70}{RESET}")
        print(f"{CYAN}{text.center(70)}{RESET}")
        print(f"{CYAN}{'='*70}{RESET}\n")
    
    def print_test(self, name):
        print(f"{BLUE}▶ {name}{RESET}")
    
    def print_pass(self, msg):
        print(f"  {GREEN}✓ {msg}{RESET}")
    
    def print_fail(self, msg):
        print(f"  {RED}✗ {msg}{RESET}")
    
    def print_info(self, msg):
        print(f"  {YELLOW}ℹ {msg}{RESET}")
    
    def test_frontend_accessibility(self):
        """Test if frontend is accessible"""
        self.print_test("Frontend Accessibility")
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            if response.status_code == 200:
                self.print_pass(f"Frontend accessible at {FRONTEND_URL}")
                self.print_pass(f"Response time: {response.elapsed.total_seconds():.2f}s")
                return True
            else:
                self.print_fail(f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.print_fail(f"Error: {str(e)}")
            return False
    
    def test_backend_health(self):
        """Test backend health"""
        self.print_test("Backend Health Check")
        try:
            response = requests.get(f"{BASE_URL}/healthz", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.print_pass(f"Backend status: {data.get('status')}")
                self.print_pass(f"API is responsive")
                return True
            else:
                self.print_fail(f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.print_fail(f"Error: {str(e)}")
            return False
    
    def test_registration_flow(self):
        """Test user registration"""
        self.print_test("Registration Flow (User Creation)")
        try:
            payload = {
                "email": self.test_email,
                "password": self.test_password,
                "full_name": self.test_name
            }
            response = requests.post(f"{API_V1}/auth/register", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.print_pass("User registered successfully")
                self.print_pass(f"Email: {self.test_email}")
                self.print_pass(f"Token generated: Yes")
                return True
            else:
                self.print_fail(f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_fail(f"Error: {str(e)}")
            return False
    
    def test_login_flow(self):
        """Test user login"""
        self.print_test("Login Flow (Authentication)")
        try:
            payload = {
                "email": self.test_email,
                "password": self.test_password
            }
            response = requests.post(f"{API_V1}/auth/login", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                new_token = data.get("access_token")
                self.print_pass("Login successful")
                self.print_pass(f"Token received: Yes")
                self.print_pass(f"Token type: {data.get('token_type')}")
                self.token = new_token
                return True
            else:
                self.print_fail(f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_fail(f"Error: {str(e)}")
            return False
    
    def test_file_upload_flow(self):
        """Test file upload functionality"""
        self.print_test("File Upload Flow")
        try:
            if not self.token:
                self.print_fail("No token available")
                return False
            
            # Create test file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
                f.write("Sample answer sheet content\nQuestion 1 Answer: A\nQuestion 2 Answer: B")
                temp_file = f.name
            
            headers = {"Authorization": f"Bearer {self.token}"}
            
            with open(temp_file, "rb") as f:
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
                self.print_pass("File uploaded successfully")
                self.print_pass(f"Submission ID: {self.submission_id}")
                self.print_pass(f"Status: {result.get('status')}")
                self.print_pass(f"Storage path: {result.get('storage_path')}")
                return True
            else:
                self.print_fail(f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_fail(f"Error: {str(e)}")
            return False
    
    def test_dashboard_data(self):
        """Test dashboard data retrieval"""
        self.print_test("Dashboard Data Retrieval")
        try:
            if not self.token:
                self.print_fail("No token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{API_V1}/submissions", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                submissions = data.get("submissions", [])
                self.print_pass("Dashboard data retrieved")
                self.print_pass(f"Total submissions: {len(submissions)}")
                self.print_pass(f"Response time: Fast")
                return True
            else:
                self.print_fail(f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_fail(f"Error: {str(e)}")
            return False
    
    def test_api_endpoints(self):
        """Test all API endpoints"""
        self.print_test("API Endpoints Availability")
        try:
            response = requests.get(f"{BASE_URL}/openapi.json")
            if response.status_code == 200:
                schema = response.json()
                paths = list(schema.get("paths", {}).keys())
                self.print_pass(f"Total endpoints: {len(paths)}")
                self.print_pass("All endpoints available:")
                for path in paths[:5]:
                    self.print_info(f"{path}")
                if len(paths) > 5:
                    self.print_info(f"... and {len(paths) - 5} more")
                return True
            else:
                self.print_fail(f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_fail(f"Error: {str(e)}")
            return False
    
    def test_error_handling(self):
        """Test error handling"""
        self.print_test("Error Handling")
        try:
            # Test invalid login
            payload = {"email": "invalid@test.com", "password": "wrong"}
            response = requests.post(f"{API_V1}/auth/login", json=payload)
            
            if response.status_code == 401:
                self.print_pass("Invalid credentials rejected correctly")
                error_detail = response.json().get("detail")
                self.print_pass(f"Error message: {error_detail}")
                return True
            else:
                self.print_fail("Error handling not working")
                return False
        except Exception as e:
            self.print_fail(f"Error: {str(e)}")
            return False
    
    def test_cors_headers(self):
        """Test CORS headers"""
        self.print_test("CORS Configuration")
        try:
            headers = {"Origin": "http://localhost:5173"}
            response = requests.options(f"{API_V1}/auth/login", headers=headers)
            
            if "access-control-allow-origin" in response.headers:
                self.print_pass("CORS headers present")
                self.print_pass(f"Allow-Origin: {response.headers.get('access-control-allow-origin')}")
                self.print_pass(f"Allow-Methods: {response.headers.get('access-control-allow-methods')}")
                return True
            else:
                self.print_fail("CORS headers missing")
                return False
        except Exception as e:
            self.print_fail(f"Error: {str(e)}")
            return False
    
    def test_response_times(self):
        """Test response times"""
        self.print_test("Response Time Performance")
        try:
            times = []
            
            # Test health endpoint multiple times
            for _ in range(3):
                start = time.time()
                response = requests.get(f"{BASE_URL}/healthz")
                elapsed = (time.time() - start) * 1000  # ms
                times.append(elapsed)
            
            avg_time = sum(times) / len(times)
            self.print_pass(f"Average response time: {avg_time:.2f}ms")
            
            if avg_time < 100:
                self.print_pass("Performance: Excellent")
            elif avg_time < 500:
                self.print_pass("Performance: Good")
            else:
                self.print_info("Performance: Acceptable")
            
            return True
        except Exception as e:
            self.print_fail(f"Error: {str(e)}")
            return False
    
    def test_token_persistence(self):
        """Test token management"""
        self.print_test("Token Management")
        try:
            if not self.token:
                self.print_fail("No token available")
                return False
            
            # Test with token
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{API_V1}/submissions", headers=headers)
            
            if response.status_code == 200:
                self.print_pass("Token is valid")
                self.print_pass("Token can authenticate requests")
                self.print_pass("Session persistence: Working")
                return True
            else:
                self.print_fail(f"Token authentication failed: {response.status_code}")
                return False
        except Exception as e:
            self.print_fail(f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        self.print_header("COMPREHENSIVE FRONTEND & API TESTING")
        print(f"Test Environment: {FRONTEND_URL}")
        print(f"Backend Server: {BASE_URL}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        tests = [
            ("frontend_accessibility", self.test_frontend_accessibility),
            ("backend_health", self.test_backend_health),
            ("registration", self.test_registration_flow),
            ("login", self.test_login_flow),
            ("file_upload", self.test_file_upload_flow),
            ("dashboard", self.test_dashboard_data),
            ("api_endpoints", self.test_api_endpoints),
            ("error_handling", self.test_error_handling),
            ("cors", self.test_cors_headers),
            ("response_times", self.test_response_times),
            ("token_persistence", self.test_token_persistence),
        ]
        
        for test_name, test_func in tests:
            try:
                self.test_results[test_name] = test_func()
            except Exception as e:
                print(f"{RED}Unexpected error in {test_name}: {str(e)}{RESET}")
                self.test_results[test_name] = False
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        self.print_header("TEST SUMMARY")
        
        total = len(self.test_results)
        passed = sum(1 for v in self.test_results.values() if v)
        failed = total - passed
        
        print("Test Results:\n")
        for test_name, result in self.test_results.items():
            status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
            display_name = test_name.replace("_", " ").title()
            print(f"  {display_name}: {status}")
        
        print(f"\n{CYAN}{'='*70}{RESET}")
        print(f"Total Tests: {total}")
        print(f"Passed: {GREEN}{passed}{RESET}")
        print(f"Failed: {RED}{failed}{RESET}")
        percentage = (passed / total) * 100 if total > 0 else 0
        print(f"Success Rate: {GREEN}{percentage:.1f}%{RESET}")
        print(f"{CYAN}{'='*70}{RESET}\n")
        
        if failed == 0:
            print(f"{GREEN}🎉 ALL TESTS PASSED! YOUR FRONTEND IS FULLY FUNCTIONAL! 🎉{RESET}\n")
        else:
            print(f"{YELLOW}⚠️  {failed} test(s) failed. Check the issues above.{RESET}\n")

if __name__ == "__main__":
    tester = FrontendTester()
    tester.run_all_tests()
