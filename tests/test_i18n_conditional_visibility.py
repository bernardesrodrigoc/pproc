"""
Test suite for i18n, conditional form logic, and visibility mode features
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://editcheck.preview.emergentagent.com')

class TestCNPQHierarchicalAreas:
    """Test CNPq hierarchical scientific areas endpoints"""
    
    def test_get_grande_areas(self):
        """Test GET /api/options/cnpq/grande-areas returns all 9 Grande Áreas"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/grande-areas")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        # Check structure
        assert all('code' in ga and 'name' in ga and 'name_en' in ga for ga in data)
        # Check first item
        assert data[0]['code'] == '1'
        assert data[0]['name'] == 'Ciências Exatas e da Terra'
        print(f"SUCCESS: Found {len(data)} Grande Áreas")
    
    def test_get_areas_for_grande_area(self):
        """Test GET /api/options/cnpq/areas/{code} returns Áreas"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/areas/1")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        # Check structure
        assert all('code' in a and 'name' in a and 'name_en' in a for a in data)
        # Check code pattern
        assert all(a['code'].startswith('1.') for a in data)
        print(f"SUCCESS: Found {len(data)} Áreas for Grande Área 1")
    
    def test_get_subareas_for_area(self):
        """Test GET /api/options/cnpq/subareas/{code} returns Subáreas"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/subareas/1.01")
        assert response.status_code == 200
        data = response.json()
        # May have subareas or empty list
        if len(data) > 0:
            assert all('code' in s and 'name' in s and 'name_en' in s for s in data)
            assert all(s['code'].startswith('1.01.') for s in data)
        print(f"SUCCESS: Found {len(data)} Subáreas for Área 1.01")
    
    def test_invalid_grande_area_returns_404_or_empty(self):
        """Test invalid Grande Área code returns 404 or empty list"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/areas/99")
        # API may return 404 or empty list for invalid codes
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert data == []
        print(f"SUCCESS: Invalid Grande Área returns status {response.status_code}")


class TestFormOptions:
    """Test form options endpoints"""
    
    def test_manuscript_types(self):
        """Test GET /api/options/manuscript-types"""
        response = requests.get(f"{BASE_URL}/api/options/manuscript-types")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        print(f"SUCCESS: Found {len(data)} manuscript types")
    
    def test_decision_types(self):
        """Test GET /api/options/decision-types"""
        response = requests.get(f"{BASE_URL}/api/options/decision-types")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        print(f"SUCCESS: Found {len(data)} decision types")
    
    def test_reviewer_counts(self):
        """Test GET /api/options/reviewer-counts"""
        response = requests.get(f"{BASE_URL}/api/options/reviewer-counts")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        print(f"SUCCESS: Found {len(data)} reviewer count options")
    
    def test_time_ranges(self):
        """Test GET /api/options/time-ranges"""
        response = requests.get(f"{BASE_URL}/api/options/time-ranges")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        print(f"SUCCESS: Found {len(data)} time range options")
    
    def test_apc_ranges(self):
        """Test GET /api/options/apc-ranges"""
        response = requests.get(f"{BASE_URL}/api/options/apc-ranges")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        print(f"SUCCESS: Found {len(data)} APC range options")
    
    def test_editor_comment_types(self):
        """Test GET /api/options/editor-comment-types"""
        response = requests.get(f"{BASE_URL}/api/options/editor-comment-types")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        print(f"SUCCESS: Found {len(data)} editor comment types")
    
    def test_review_quality_scale(self):
        """Test GET /api/options/review-quality-scale"""
        response = requests.get(f"{BASE_URL}/api/options/review-quality-scale")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5  # 1-5 scale
        print(f"SUCCESS: Found {len(data)} review quality scale options")
    
    def test_feedback_clarity_scale(self):
        """Test GET /api/options/feedback-clarity-scale"""
        response = requests.get(f"{BASE_URL}/api/options/feedback-clarity-scale")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5  # 1-5 scale
        print(f"SUCCESS: Found {len(data)} feedback clarity scale options")
    
    def test_decision_fairness_options(self):
        """Test GET /api/options/decision-fairness"""
        response = requests.get(f"{BASE_URL}/api/options/decision-fairness")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        print(f"SUCCESS: Found {len(data)} decision fairness options")
    
    def test_would_recommend_options(self):
        """Test GET /api/options/would-recommend"""
        response = requests.get(f"{BASE_URL}/api/options/would-recommend")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        print(f"SUCCESS: Found {len(data)} would recommend options")


class TestVisibilityStatus:
    """Test visibility status endpoint"""
    
    def test_visibility_status(self):
        """Test GET /api/analytics/visibility-status"""
        response = requests.get(f"{BASE_URL}/api/analytics/visibility-status")
        assert response.status_code == 200
        data = response.json()
        # Check required fields
        assert 'visibility_mode' in data
        assert 'public_stats_enabled' in data
        assert 'demo_mode_enabled' in data
        # Check visibility mode is one of the valid options
        assert data['visibility_mode'] in ['user_only', 'threshold_based', 'admin_forced']
        print(f"SUCCESS: Visibility status - mode: {data['visibility_mode']}, public: {data['public_stats_enabled']}")


class TestAnalyticsEndpoints:
    """Test analytics endpoints"""
    
    def test_analytics_overview(self):
        """Test GET /api/analytics/overview"""
        response = requests.get(f"{BASE_URL}/api/analytics/overview")
        assert response.status_code == 200
        data = response.json()
        # Check for key fields
        assert 'total_submissions' in data or 'visibility_restricted' in data
        print(f"SUCCESS: Analytics overview returned")
    
    def test_analytics_publishers(self):
        """Test GET /api/analytics/publishers"""
        response = requests.get(f"{BASE_URL}/api/analytics/publishers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"SUCCESS: Found {len(data)} publishers in analytics")
    
    def test_analytics_journals(self):
        """Test GET /api/analytics/journals"""
        response = requests.get(f"{BASE_URL}/api/analytics/journals")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"SUCCESS: Found {len(data)} journals in analytics")
    
    def test_analytics_areas(self):
        """Test GET /api/analytics/areas"""
        response = requests.get(f"{BASE_URL}/api/analytics/areas")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"SUCCESS: Found {len(data)} areas in analytics")


class TestPublishersAndJournals:
    """Test publishers and journals endpoints"""
    
    def test_get_publishers(self):
        """Test GET /api/publishers"""
        response = requests.get(f"{BASE_URL}/api/publishers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # Check structure
        assert all('publisher_id' in p and 'name' in p for p in data)
        print(f"SUCCESS: Found {len(data)} publishers")
    
    def test_get_journals_for_publisher(self):
        """Test GET /api/journals?publisher_id=..."""
        # First get a publisher
        publishers_response = requests.get(f"{BASE_URL}/api/publishers")
        publishers = publishers_response.json()
        if len(publishers) > 0:
            publisher_id = publishers[0]['publisher_id']
            response = requests.get(f"{BASE_URL}/api/journals?publisher_id={publisher_id}")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            print(f"SUCCESS: Found {len(data)} journals for publisher {publisher_id}")


class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_health(self):
        """Test GET /api/health"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        print("SUCCESS: Health check passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
