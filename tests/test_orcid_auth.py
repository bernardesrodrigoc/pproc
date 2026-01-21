"""
ORCID OAuth 2.0 Authentication Tests
Tests for ORCID OAuth endpoints and configuration
"""
import pytest
import requests
import os
from urllib.parse import urlparse, parse_qs

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestOrcidOAuthEndpoints:
    """Test ORCID OAuth 2.0 endpoints"""
    
    def test_orcid_status_endpoint_returns_configured(self):
        """Test that ORCID status endpoint returns configured=true"""
        response = requests.get(f"{BASE_URL}/api/auth/orcid/status")
        assert response.status_code == 200
        
        data = response.json()
        assert "configured" in data
        assert data["configured"] == True
        assert "sandbox" in data
        # Should be using production ORCID (not sandbox)
        assert data["sandbox"] == False
    
    def test_orcid_authorize_returns_valid_url(self):
        """Test that ORCID authorize endpoint returns valid authorization URL"""
        response = requests.get(
            f"{BASE_URL}/api/auth/orcid/authorize",
            params={"redirect": "/dashboard"},
            headers={"Origin": BASE_URL}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "authorization_url" in data
        assert "state" in data
        
        # Verify authorization URL structure
        auth_url = data["authorization_url"]
        assert "orcid.org/oauth/authorize" in auth_url
        
        # Parse URL and verify parameters
        parsed = urlparse(auth_url)
        params = parse_qs(parsed.query)
        
        # Verify client_id is correct
        assert "client_id" in params
        assert params["client_id"][0] == "APP-PH83PDPJIO8UJUBZ"
        
        # Verify response_type
        assert "response_type" in params
        assert params["response_type"][0] == "code"
        
        # Verify scope
        assert "scope" in params
        assert params["scope"][0] == "/authenticate"
        
        # Verify redirect_uri
        assert "redirect_uri" in params
        assert "callback" in params["redirect_uri"][0]
        
        # Verify state contains redirect path
        assert "state" in params
        state = params["state"][0]
        assert "/dashboard" in state
    
    def test_orcid_authorize_with_custom_redirect(self):
        """Test ORCID authorize with custom redirect path"""
        response = requests.get(
            f"{BASE_URL}/api/auth/orcid/authorize",
            params={"redirect": "/analytics"},
            headers={"Origin": BASE_URL}
        )
        assert response.status_code == 200
        
        data = response.json()
        state = data["state"]
        # State should contain the custom redirect path
        assert "/analytics" in state
    
    def test_orcid_callback_requires_code(self):
        """Test that ORCID callback requires authorization code"""
        response = requests.post(
            f"{BASE_URL}/api/auth/orcid/callback",
            json={"state": "test_state"},
            headers={"Content-Type": "application/json"}
        )
        # Should return 400 because code is missing
        assert response.status_code == 400
        
        data = response.json()
        assert "detail" in data
        assert "code" in data["detail"].lower()


class TestHealthAndBasicEndpoints:
    """Test basic API health and endpoints"""
    
    def test_health_endpoint(self):
        """Test API health endpoint"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_root_endpoint(self):
        """Test API root endpoint"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "running"


class TestAuthEndpoints:
    """Test authentication endpoints"""
    
    def test_auth_me_requires_authentication(self):
        """Test that /auth/me requires authentication"""
        response = requests.get(f"{BASE_URL}/api/auth/me")
        assert response.status_code == 401
    
    def test_logout_endpoint(self):
        """Test logout endpoint works without auth"""
        response = requests.post(f"{BASE_URL}/api/auth/logout")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data


class TestAnalyticsEndpoints:
    """Test analytics endpoints (public)"""
    
    def test_analytics_overview(self):
        """Test analytics overview endpoint"""
        response = requests.get(f"{BASE_URL}/api/analytics/overview")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_submissions" in data
    
    def test_analytics_publishers(self):
        """Test publisher analytics endpoint"""
        response = requests.get(f"{BASE_URL}/api/analytics/publishers")
        assert response.status_code == 200
        
        # Should return a list
        data = response.json()
        assert isinstance(data, list)
    
    def test_analytics_journals(self):
        """Test journal analytics endpoint"""
        response = requests.get(f"{BASE_URL}/api/analytics/journals")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
