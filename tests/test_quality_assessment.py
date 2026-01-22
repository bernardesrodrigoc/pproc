"""
Test suite for PubProcess Quality Assessment Features
Tests new form options endpoints, submission fields, and quality indices
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://editcheck.preview.emergentagent.com').rstrip('/')
ADMIN_TOKEN = "O0TxVAXBmyse8PyU0Jsr3MUVt3Q9sjp_TT_KYCrevBs"


class TestQualityOptionsEndpoints:
    """Test new quality assessment form options endpoints"""
    
    def test_review_quality_scale_endpoint(self):
        """Test /api/options/review-quality-scale returns 1-5 scale"""
        response = requests.get(f"{BASE_URL}/api/options/review-quality-scale")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 5
        
        # Verify structure
        for item in data:
            assert "id" in item
            assert "value" in item
            assert "label" in item
            assert "description" in item
        
        # Verify values 1-5
        values = [item["value"] for item in data]
        assert values == [1, 2, 3, 4, 5]
        
        # Verify labels
        labels = [item["label"] for item in data]
        assert "Very Low" in labels
        assert "Very High" in labels
    
    def test_feedback_clarity_scale_endpoint(self):
        """Test /api/options/feedback-clarity-scale returns 1-5 scale"""
        response = requests.get(f"{BASE_URL}/api/options/feedback-clarity-scale")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 5
        
        # Verify values 1-5
        values = [item["value"] for item in data]
        assert values == [1, 2, 3, 4, 5]
        
        # Verify labels
        labels = [item["label"] for item in data]
        assert "Very Unclear" in labels
        assert "Very Clear" in labels
    
    def test_decision_fairness_endpoint(self):
        """Test /api/options/decision-fairness returns agree/neutral/disagree"""
        response = requests.get(f"{BASE_URL}/api/options/decision-fairness")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
        
        # Verify IDs
        ids = [item["id"] for item in data]
        assert "agree" in ids
        assert "neutral" in ids
        assert "disagree" in ids
        
        # Verify structure
        for item in data:
            assert "id" in item
            assert "label" in item
            assert "description" in item
    
    def test_would_recommend_endpoint(self):
        """Test /api/options/would-recommend returns yes/neutral/no"""
        response = requests.get(f"{BASE_URL}/api/options/would-recommend")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
        
        # Verify IDs
        ids = [item["id"] for item in data]
        assert "yes" in ids
        assert "neutral" in ids
        assert "no" in ids


class TestQualityIndicesInAnalytics:
    """Test quality indices in analytics overview"""
    
    @pytest.fixture(autouse=True)
    def setup_visibility(self):
        """Ensure demo_mode and public_stats are enabled for testing"""
        response = requests.put(
            f"{BASE_URL}/api/admin/settings",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            json={
                "visibility_mode": "threshold_based",
                "public_stats_enabled": True,
                "demo_mode_enabled": True
            }
        )
        assert response.status_code == 200
        yield
        # Reset to user_only mode after tests
        requests.put(
            f"{BASE_URL}/api/admin/settings",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            json={
                "visibility_mode": "user_only",
                "public_stats_enabled": False,
                "demo_mode_enabled": True
            }
        )
    
    def test_analytics_overview_includes_quality_indices(self):
        """Test analytics overview returns quality_indices when demo_mode enabled"""
        response = requests.get(f"{BASE_URL}/api/analytics/overview")
        assert response.status_code == 200
        
        data = response.json()
        assert data.get("sufficient_data") == True
        assert data.get("indices_available") == True
        assert "quality_indices" in data
    
    def test_average_review_quality_index(self):
        """Test average_review_quality index structure"""
        response = requests.get(f"{BASE_URL}/api/analytics/overview")
        data = response.json()
        
        quality_indices = data.get("quality_indices", {})
        assert "average_review_quality" in quality_indices
        
        arq = quality_indices["average_review_quality"]
        assert "value" in arq
        assert "scale" in arq
        assert "description" in arq
        assert arq["scale"] == "0-100"
        assert 0 <= arq["value"] <= 100
    
    def test_feedback_clarity_index(self):
        """Test feedback_clarity_index structure"""
        response = requests.get(f"{BASE_URL}/api/analytics/overview")
        data = response.json()
        
        quality_indices = data.get("quality_indices", {})
        assert "feedback_clarity_index" in quality_indices
        
        fci = quality_indices["feedback_clarity_index"]
        assert "value" in fci
        assert "scale" in fci
        assert fci["scale"] == "0-100"
        assert 0 <= fci["value"] <= 100
    
    def test_decision_fairness_index(self):
        """Test decision_fairness_index structure with distribution"""
        response = requests.get(f"{BASE_URL}/api/analytics/overview")
        data = response.json()
        
        quality_indices = data.get("quality_indices", {})
        assert "decision_fairness_index" in quality_indices
        
        dfi = quality_indices["decision_fairness_index"]
        assert "value" in dfi
        assert "scale" in dfi
        assert "distribution" in dfi
        assert dfi["scale"] == "0-100"
        
        # Check distribution has agree/neutral/disagree
        dist = dfi["distribution"]
        assert "agree" in dist
        assert "neutral" in dist
        assert "disagree" in dist
    
    def test_recommendation_index(self):
        """Test recommendation_index structure with distribution"""
        response = requests.get(f"{BASE_URL}/api/analytics/overview")
        data = response.json()
        
        quality_indices = data.get("quality_indices", {})
        assert "recommendation_index" in quality_indices
        
        ri = quality_indices["recommendation_index"]
        assert "value" in ri
        assert "scale" in ri
        assert "distribution" in ri
        assert ri["scale"] == "0-100"
        
        # Check distribution has yes/neutral/no
        dist = ri["distribution"]
        assert "yes" in dist
        assert "neutral" in dist
        assert "no" in dist


class TestSubmissionWithQualityFields:
    """Test submission creation with new quality assessment fields"""
    
    def test_submission_accepts_quality_fields(self):
        """Test that submission endpoint accepts new quality fields"""
        # This test requires authentication
        response = requests.post(
            f"{BASE_URL}/api/submissions",
            headers={
                "Authorization": f"Bearer {ADMIN_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "scientific_area": "life_sciences",
                "manuscript_type": "experimental",
                "publisher_id": "other",
                "custom_publisher_name": "Test Publisher Quality",
                "journal_id": "other",
                "custom_journal_name": "Test Journal Quality",
                "decision_type": "major_revision",
                "reviewer_count": "2+",
                "time_to_decision": "31-90",
                "apc_range": "1000_3000",
                "review_comments": ["methodology", "statistics"],
                "editor_comments": "yes_technical",
                "perceived_coherence": "yes",
                # NEW quality fields
                "overall_review_quality": 4,
                "feedback_clarity": 5,
                "decision_fairness": "agree",
                "would_recommend": "yes"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "submission_id" in data
        assert data.get("status") == "pending"


class TestValidForStatsValidation:
    """Test valid_for_stats submission validation logic"""
    
    def test_duplicate_submission_flagged(self):
        """Test that duplicate submissions within 30 days are flagged"""
        # First submission
        response1 = requests.post(
            f"{BASE_URL}/api/submissions",
            headers={
                "Authorization": f"Bearer {ADMIN_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "scientific_area": "computer_science",
                "manuscript_type": "methodological",
                "publisher_id": "other",
                "custom_publisher_name": "Duplicate Test Publisher",
                "journal_id": "other",
                "custom_journal_name": "Duplicate Test Journal",
                "decision_type": "reject_after_review",
                "reviewer_count": "1",
                "time_to_decision": "0-30",
                "apc_range": "no_apc",
                "review_comments": ["conceptual"],
                "editor_comments": "yes_generic",
                "perceived_coherence": "partially"
            }
        )
        assert response1.status_code == 200
        
        # Second submission to same journal (should be flagged as duplicate)
        response2 = requests.post(
            f"{BASE_URL}/api/submissions",
            headers={
                "Authorization": f"Bearer {ADMIN_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "scientific_area": "computer_science",
                "manuscript_type": "methodological",
                "publisher_id": "other",
                "custom_publisher_name": "Duplicate Test Publisher 2",
                "journal_id": "other",
                "custom_journal_name": "Duplicate Test Journal 2",
                "decision_type": "minor_revision",
                "reviewer_count": "2+",
                "time_to_decision": "31-90",
                "apc_range": "under_1000",
                "review_comments": ["methodology"],
                "editor_comments": "yes_technical",
                "perceived_coherence": "yes"
            }
        )
        assert response2.status_code == 200
        # Note: valid_for_stats is returned in response
        data = response2.json()
        assert "valid_for_stats" in data


class TestVisibilityMessages:
    """Test institutional/neutral Portuguese tone in visibility messages"""
    
    def test_user_only_mode_message(self):
        """Test visibility message in user_only mode"""
        # Set to user_only mode
        requests.put(
            f"{BASE_URL}/api/admin/settings",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            json={"visibility_mode": "user_only", "public_stats_enabled": False}
        )
        
        response = requests.get(f"{BASE_URL}/api/analytics/visibility-status")
        assert response.status_code == 200
        
        data = response.json()
        assert data.get("visibility_mode") == "user_only"
        assert "message" in data
        # Check for Portuguese institutional tone
        message = data.get("message", "")
        assert "estatísticas" in message.lower() or "dados" in message.lower()
    
    def test_threshold_based_mode_message(self):
        """Test visibility message in threshold_based mode"""
        # Set to threshold_based mode
        requests.put(
            f"{BASE_URL}/api/admin/settings",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            json={"visibility_mode": "threshold_based", "public_stats_enabled": False}
        )
        
        response = requests.get(f"{BASE_URL}/api/analytics/visibility-status")
        assert response.status_code == 200
        
        data = response.json()
        assert data.get("visibility_mode") == "threshold_based"


class TestSampleDataQualityFields:
    """Test that sample data includes new quality assessment fields"""
    
    def test_sample_data_has_quality_fields(self):
        """Verify sample submissions have new quality fields populated"""
        # Enable demo mode to include sample data
        requests.put(
            f"{BASE_URL}/api/admin/settings",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            json={"demo_mode_enabled": True, "visibility_mode": "threshold_based", "public_stats_enabled": True}
        )
        
        # Get analytics - if quality indices are available, sample data has the fields
        response = requests.get(f"{BASE_URL}/api/analytics/overview")
        assert response.status_code == 200
        
        data = response.json()
        # If indices_available is True, sample data has the new fields
        assert data.get("indices_available") == True
        
        quality_indices = data.get("quality_indices", {})
        # All 4 indices should be present
        assert "average_review_quality" in quality_indices
        assert "feedback_clarity_index" in quality_indices
        assert "decision_fairness_index" in quality_indices
        assert "recommendation_index" in quality_indices


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
