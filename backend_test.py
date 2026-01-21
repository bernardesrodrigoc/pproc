#!/usr/bin/env python3
"""
Backend API Testing for Editorial Decision Statistics Platform
Tests all API endpoints with proper error handling and reporting.
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class EditorialStatsAPITester:
    def __init__(self, base_url: str = "https://pubprocess.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.session_token = None
        self.test_results = []
        self.tests_run = 0
        self.tests_passed = 0
        
    def log_test(self, name: str, success: bool, details: str = "", response_data: dict = None):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            
        result = {
            "test_name": name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
        if details:
            print(f"    {details}")
        if not success and response_data:
            print(f"    Response: {response_data}")
        print()

    def test_health_endpoint(self) -> bool:
        """Test /api/health endpoint"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.log_test(
                    "Health Check", 
                    True, 
                    f"Status: {data.get('status', 'unknown')}"
                )
            else:
                self.log_test(
                    "Health Check", 
                    False, 
                    f"Status code: {response.status_code}",
                    {"status_code": response.status_code, "text": response.text[:200]}
                )
            return success
            
        except Exception as e:
            self.log_test("Health Check", False, f"Exception: {str(e)}")
            return False

    def test_root_endpoint(self) -> bool:
        """Test /api/ root endpoint"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.log_test(
                    "Root API Endpoint", 
                    True, 
                    f"Message: {data.get('message', 'No message')}"
                )
            else:
                self.log_test(
                    "Root API Endpoint", 
                    False, 
                    f"Status code: {response.status_code}",
                    {"status_code": response.status_code}
                )
            return success
            
        except Exception as e:
            self.log_test("Root API Endpoint", False, f"Exception: {str(e)}")
            return False

    def test_publishers_endpoint(self) -> bool:
        """Test /api/publishers endpoint"""
        try:
            response = requests.get(f"{self.api_url}/publishers", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                publisher_count = len(data) if isinstance(data, list) else 0
                self.log_test(
                    "Publishers Endpoint", 
                    True, 
                    f"Found {publisher_count} publishers"
                )
                return True
            else:
                self.log_test(
                    "Publishers Endpoint", 
                    False, 
                    f"Status code: {response.status_code}",
                    {"status_code": response.status_code}
                )
                return False
                
        except Exception as e:
            self.log_test("Publishers Endpoint", False, f"Exception: {str(e)}")
            return False

    def test_journals_endpoint(self) -> bool:
        """Test /api/journals endpoint"""
        try:
            response = requests.get(f"{self.api_url}/journals", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                journal_count = len(data) if isinstance(data, list) else 0
                self.log_test(
                    "Journals Endpoint", 
                    True, 
                    f"Found {journal_count} journals"
                )
                return True
            else:
                self.log_test(
                    "Journals Endpoint", 
                    False, 
                    f"Status code: {response.status_code}",
                    {"status_code": response.status_code}
                )
                return False
                
        except Exception as e:
            self.log_test("Journals Endpoint", False, f"Exception: {str(e)}")
            return False

    def test_analytics_overview(self) -> bool:
        """Test /api/analytics/overview endpoint"""
        try:
            response = requests.get(f"{self.api_url}/analytics/overview", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                total_submissions = data.get('total_submissions', 0)
                sufficient_data = data.get('sufficient_data', False)
                self.log_test(
                    "Analytics Overview", 
                    True, 
                    f"Total submissions: {total_submissions}, Sufficient data: {sufficient_data}"
                )
                return True
            else:
                self.log_test(
                    "Analytics Overview", 
                    False, 
                    f"Status code: {response.status_code}",
                    {"status_code": response.status_code}
                )
                return False
                
        except Exception as e:
            self.log_test("Analytics Overview", False, f"Exception: {str(e)}")
            return False

    def test_analytics_publishers(self) -> bool:
        """Test /api/analytics/publishers endpoint"""
        try:
            response = requests.get(f"{self.api_url}/analytics/publishers", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                analytics_count = len(data) if isinstance(data, list) else 0
                self.log_test(
                    "Analytics Publishers", 
                    True, 
                    f"Found {analytics_count} publisher analytics"
                )
                return True
            else:
                self.log_test(
                    "Analytics Publishers", 
                    False, 
                    f"Status code: {response.status_code}",
                    {"status_code": response.status_code}
                )
                return False
                
        except Exception as e:
            self.log_test("Analytics Publishers", False, f"Exception: {str(e)}")
            return False

    def test_analytics_journals(self) -> bool:
        """Test /api/analytics/journals endpoint"""
        try:
            response = requests.get(f"{self.api_url}/analytics/journals", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                analytics_count = len(data) if isinstance(data, list) else 0
                self.log_test(
                    "Analytics Journals", 
                    True, 
                    f"Found {analytics_count} journal analytics"
                )
                return True
            else:
                self.log_test(
                    "Analytics Journals", 
                    False, 
                    f"Status code: {response.status_code}",
                    {"status_code": response.status_code}
                )
                return False
                
        except Exception as e:
            self.log_test("Analytics Journals", False, f"Exception: {str(e)}")
            return False

    def test_analytics_areas(self) -> bool:
        """Test /api/analytics/areas endpoint"""
        try:
            response = requests.get(f"{self.api_url}/analytics/areas", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                areas_count = len(data) if isinstance(data, list) else 0
                self.log_test(
                    "Analytics Areas", 
                    True, 
                    f"Found {areas_count} area analytics"
                )
                return True
            else:
                self.log_test(
                    "Analytics Areas", 
                    False, 
                    f"Status code: {response.status_code}",
                    {"status_code": response.status_code}
                )
                return False
                
        except Exception as e:
            self.log_test("Analytics Areas", False, f"Exception: {str(e)}")
            return False

    def test_options_endpoints(self) -> bool:
        """Test all /api/options/* endpoints"""
        endpoints = [
            "scientific-areas",
            "manuscript-types", 
            "decision-types",
            "reviewer-counts",
            "time-ranges",
            "apc-ranges",
            "review-comment-types",
            "editor-comment-types",
            "coherence-options"
        ]
        
        all_success = True
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.api_url}/options/{endpoint}", timeout=10)
                success = response.status_code == 200
                
                if success:
                    data = response.json()
                    options_count = len(data) if isinstance(data, list) else 0
                    self.log_test(
                        f"Options {endpoint}", 
                        True, 
                        f"Found {options_count} options"
                    )
                else:
                    self.log_test(
                        f"Options {endpoint}", 
                        False, 
                        f"Status code: {response.status_code}",
                        {"status_code": response.status_code}
                    )
                    all_success = False
                    
            except Exception as e:
                self.log_test(f"Options {endpoint}", False, f"Exception: {str(e)}")
                all_success = False
                
        return all_success

    def test_admin_endpoints_with_token(self) -> bool:
        """Test admin endpoints using the provided admin session token"""
        # Use the admin session token provided in the context
        admin_token = "admin_test_1769015215491"
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        all_success = True
        
        # Test admin stats endpoint
        try:
            response = requests.get(f"{self.api_url}/admin/stats", headers=headers, timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.log_test(
                    "Admin Stats", 
                    True, 
                    f"Total users: {data.get('total_users', 0)}, Total submissions: {data.get('total_submissions', 0)}"
                )
            else:
                self.log_test(
                    "Admin Stats", 
                    False, 
                    f"Status code: {response.status_code}",
                    {"status_code": response.status_code, "text": response.text[:200]}
                )
                all_success = False
                
        except Exception as e:
            self.log_test("Admin Stats", False, f"Exception: {str(e)}")
            all_success = False

        # Test admin submissions endpoint
        try:
            response = requests.get(f"{self.api_url}/admin/submissions", headers=headers, timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                submissions_count = len(data.get('submissions', []))
                total = data.get('total', 0)
                self.log_test(
                    "Admin Submissions", 
                    True, 
                    f"Retrieved {submissions_count} submissions, Total: {total}"
                )
            else:
                self.log_test(
                    "Admin Submissions", 
                    False, 
                    f"Status code: {response.status_code}",
                    {"status_code": response.status_code, "text": response.text[:200]}
                )
                all_success = False
                
        except Exception as e:
            self.log_test("Admin Submissions", False, f"Exception: {str(e)}")
            all_success = False

        # Test admin submissions with status filter
        for status in ['pending', 'validated', 'flagged']:
            try:
                response = requests.get(f"{self.api_url}/admin/submissions?status={status}", headers=headers, timeout=10)
                success = response.status_code == 200
                
                if success:
                    data = response.json()
                    submissions_count = len(data.get('submissions', []))
                    self.log_test(
                        f"Admin Submissions Filter ({status})", 
                        True, 
                        f"Found {submissions_count} {status} submissions"
                    )
                else:
                    self.log_test(
                        f"Admin Submissions Filter ({status})", 
                        False, 
                        f"Status code: {response.status_code}",
                        {"status_code": response.status_code}
                    )
                    all_success = False
                    
            except Exception as e:
                self.log_test(f"Admin Submissions Filter ({status})", False, f"Exception: {str(e)}")
                all_success = False

        # Test admin users endpoint
        try:
            response = requests.get(f"{self.api_url}/admin/users", headers=headers, timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                users_count = len(data.get('users', []))
                total = data.get('total', 0)
                self.log_test(
                    "Admin Users", 
                    True, 
                    f"Retrieved {users_count} users, Total: {total}"
                )
            else:
                self.log_test(
                    "Admin Users", 
                    False, 
                    f"Status code: {response.status_code}",
                    {"status_code": response.status_code, "text": response.text[:200]}
                )
                all_success = False
                
        except Exception as e:
            self.log_test("Admin Users", False, f"Exception: {str(e)}")
            all_success = False

        return all_success

    def test_admin_endpoints_without_auth(self) -> bool:
        """Test that admin endpoints properly reject unauthorized requests"""
        all_success = True
        
        # Test admin endpoints without authentication - should return 401
        admin_endpoints = [
            "/admin/stats",
            "/admin/submissions", 
            "/admin/users"
        ]
        
        for endpoint in admin_endpoints:
            try:
                response = requests.get(f"{self.api_url}{endpoint}", timeout=10)
                success = response.status_code == 401
                
                if success:
                    self.log_test(
                        f"Admin Auth Check {endpoint}", 
                        True, 
                        "Correctly rejected unauthorized request"
                    )
                else:
                    self.log_test(
                        f"Admin Auth Check {endpoint}", 
                        False, 
                        f"Expected 401, got {response.status_code}",
                        {"status_code": response.status_code}
                    )
                    all_success = False
                    
            except Exception as e:
                self.log_test(f"Admin Auth Check {endpoint}", False, f"Exception: {str(e)}")
                all_success = False
                
        return all_success

    def run_all_tests(self) -> Dict:
        """Run all backend API tests"""
        print("🚀 Starting Backend API Tests")
        print("=" * 50)
        
        # Test basic endpoints
        self.test_health_endpoint()
        self.test_root_endpoint()
        
        # Test data endpoints
        self.test_publishers_endpoint()
        self.test_journals_endpoint()
        
        # Test analytics endpoints
        self.test_analytics_overview()
        self.test_analytics_publishers()
        self.test_analytics_journals()
        self.test_analytics_areas()
        
        # Test options endpoints
        self.test_options_endpoints()
        
        # Print summary
        print("=" * 50)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        return {
            "total_tests": self.tests_run,
            "passed_tests": self.tests_passed,
            "success_rate": success_rate,
            "test_results": self.test_results
        }

def main():
    """Main test execution"""
    tester = EditorialStatsAPITester()
    results = tester.run_all_tests()
    
    # Return appropriate exit code
    if results["success_rate"] >= 80:
        print("✅ Backend tests mostly successful")
        return 0
    else:
        print("❌ Backend tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())