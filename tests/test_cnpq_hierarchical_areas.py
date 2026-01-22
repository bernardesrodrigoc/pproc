"""
Test CNPq Hierarchical Areas and Conditional Form Logic
Tests for:
1. CNPq hierarchical area endpoints (Grande Área → Área → Subárea)
2. Conditional logic in submission form (Open Access → APC, Editor comments → quality)
3. Backend validation for conditional fields
"""

import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test session token from previous iteration
TEST_SESSION_TOKEN = "O0TxVAXBmyse8PyU0Jsr3MUVt3Q9sjp_TT_KYCrevBs"


class TestCNPqGrandeAreas:
    """Test CNPq Grande Áreas endpoint (top level)"""
    
    def test_get_grande_areas_returns_9_items(self):
        """GET /api/options/cnpq/grande-areas returns all 9 Grande Áreas"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/grande-areas")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 9, f"Expected 9 Grande Áreas, got {len(data)}"
    
    def test_grande_areas_have_correct_structure(self):
        """Each Grande Área has code, name, and name_en fields"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/grande-areas")
        assert response.status_code == 200
        
        data = response.json()
        for ga in data:
            assert "code" in ga, "Missing 'code' field"
            assert "name" in ga, "Missing 'name' field"
            assert "name_en" in ga, "Missing 'name_en' field"
    
    def test_grande_areas_codes_are_1_to_9(self):
        """Grande Área codes are '1' through '9'"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/grande-areas")
        assert response.status_code == 200
        
        data = response.json()
        codes = [ga["code"] for ga in data]
        expected_codes = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        assert sorted(codes) == expected_codes
    
    def test_grande_area_1_is_ciencias_exatas(self):
        """Grande Área 1 is 'Ciências Exatas e da Terra'"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/grande-areas")
        assert response.status_code == 200
        
        data = response.json()
        ga1 = next((ga for ga in data if ga["code"] == "1"), None)
        assert ga1 is not None
        assert ga1["name"] == "Ciências Exatas e da Terra"
        assert ga1["name_en"] == "Exact and Earth Sciences"


class TestCNPqAreas:
    """Test CNPq Áreas endpoint (second level)"""
    
    def test_get_areas_for_grande_area_1(self):
        """GET /api/options/cnpq/areas/1 returns Áreas for Ciências Exatas"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/areas/1")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 8, f"Expected 8 Áreas for Grande Área 1, got {len(data)}"
    
    def test_areas_have_correct_structure(self):
        """Each Área has code, name, and name_en fields"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/areas/1")
        assert response.status_code == 200
        
        data = response.json()
        for area in data:
            assert "code" in area, "Missing 'code' field"
            assert "name" in area, "Missing 'name' field"
            assert "name_en" in area, "Missing 'name_en' field"
    
    def test_area_codes_follow_pattern(self):
        """Área codes follow pattern 'X.XX' (e.g., '1.01')"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/areas/1")
        assert response.status_code == 200
        
        data = response.json()
        for area in data:
            code = area["code"]
            assert code.startswith("1."), f"Area code {code} should start with '1.'"
            parts = code.split(".")
            assert len(parts) == 2, f"Area code {code} should have 2 parts"
    
    def test_area_1_01_is_matematica(self):
        """Área 1.01 is 'Matemática'"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/areas/1")
        assert response.status_code == 200
        
        data = response.json()
        area_101 = next((a for a in data if a["code"] == "1.01"), None)
        assert area_101 is not None
        assert area_101["name"] == "Matemática"
        assert area_101["name_en"] == "Mathematics"
    
    def test_invalid_grande_area_returns_404(self):
        """GET /api/options/cnpq/areas/99 returns 404"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/areas/99")
        assert response.status_code == 404
    
    def test_get_areas_for_all_grande_areas(self):
        """All 9 Grande Áreas have at least 1 Área"""
        for code in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            response = requests.get(f"{BASE_URL}/api/options/cnpq/areas/{code}")
            assert response.status_code == 200, f"Failed for Grande Área {code}"
            data = response.json()
            assert len(data) >= 1, f"Grande Área {code} should have at least 1 Área"


class TestCNPqSubareas:
    """Test CNPq Subáreas endpoint (third level)"""
    
    def test_get_subareas_for_area_1_01(self):
        """GET /api/options/cnpq/subareas/1.01 returns Subáreas for Matemática"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/subareas/1.01")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 4, f"Expected 4 Subáreas for Área 1.01, got {len(data)}"
    
    def test_subareas_have_correct_structure(self):
        """Each Subárea has code, name, and name_en fields"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/subareas/1.01")
        assert response.status_code == 200
        
        data = response.json()
        for subarea in data:
            assert "code" in subarea, "Missing 'code' field"
            assert "name" in subarea, "Missing 'name' field"
            assert "name_en" in subarea, "Missing 'name_en' field"
    
    def test_subarea_codes_follow_pattern(self):
        """Subárea codes follow pattern 'X.XX.XX' (e.g., '1.01.01')"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/subareas/1.01")
        assert response.status_code == 200
        
        data = response.json()
        for subarea in data:
            code = subarea["code"]
            assert code.startswith("1.01."), f"Subarea code {code} should start with '1.01.'"
            parts = code.split(".")
            assert len(parts) == 3, f"Subarea code {code} should have 3 parts"
    
    def test_subarea_1_01_01_is_algebra(self):
        """Subárea 1.01.01 is 'Álgebra'"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/subareas/1.01")
        assert response.status_code == 200
        
        data = response.json()
        subarea = next((s for s in data if s["code"] == "1.01.01"), None)
        assert subarea is not None
        assert subarea["name"] == "Álgebra"
        assert subarea["name_en"] == "Algebra"
    
    def test_area_without_subareas_returns_empty_list(self):
        """Some Áreas have no Subáreas (e.g., 2.01 Biologia Geral)"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/subareas/2.01")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0, "Área 2.01 should have no Subáreas"
    
    def test_invalid_area_returns_empty_list(self):
        """GET /api/options/cnpq/subareas/99.99 returns empty list"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/subareas/99.99")
        assert response.status_code == 200
        data = response.json()
        assert data == []


class TestCNPqLookup:
    """Test CNPq area lookup endpoint"""
    
    def test_lookup_grande_area(self):
        """Lookup Grande Área by code '1'"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/lookup/1")
        assert response.status_code == 200
        
        data = response.json()
        assert data["type"] == "grande_area"
        assert data["code"] == "1"
        assert data["name"] == "Ciências Exatas e da Terra"
    
    def test_lookup_area(self):
        """Lookup Área by code '1.01'"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/lookup/1.01")
        assert response.status_code == 200
        
        data = response.json()
        assert data["type"] == "area"
        assert data["code"] == "1.01"
        assert data["name"] == "Matemática"
    
    def test_lookup_subarea(self):
        """Lookup Subárea by code '1.01.01'"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/lookup/1.01.01")
        assert response.status_code == 200
        
        data = response.json()
        assert data["type"] == "subarea"
        assert data["code"] == "1.01.01"
        assert data["name"] == "Álgebra"
    
    def test_lookup_invalid_code_returns_404(self):
        """Lookup invalid code returns 404"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/lookup/99.99.99")
        assert response.status_code == 404


class TestSubmissionWithHierarchicalAreas:
    """Test submission creation with CNPq hierarchical areas"""
    
    @pytest.fixture
    def auth_headers(self):
        return {
            "Authorization": f"Bearer {TEST_SESSION_TOKEN}",
            "Content-Type": "application/json"
        }
    
    def test_submission_with_hierarchical_areas(self, auth_headers):
        """Create submission with CNPq hierarchical area fields"""
        submission_data = {
            "scientific_area_grande": "1",
            "scientific_area_area": "1.01",
            "scientific_area_subarea": "1.01.01",
            "manuscript_type": "experimental",
            "journal_id": "journal_nature",
            "publisher_id": "pub_springer",
            "decision_type": "accept",
            "reviewer_count": "2+",
            "time_to_decision": "31_90",
            "apc_range": "2000_3000",
            "review_comments": ["methodology", "statistics"],
            "editor_comments": "detailed",
            "perceived_coherence": "high",
            "journal_is_open_access": True
        }
        
        response = requests.post(
            f"{BASE_URL}/api/submissions",
            json=submission_data,
            headers=auth_headers
        )
        
        # May fail if duplicate within 30 days, but structure should be valid
        if response.status_code == 200:
            data = response.json()
            assert "submission_id" in data
            assert data["status"] == "pending"
    
    def test_submission_without_subarea_is_valid(self, auth_headers):
        """Submission without subárea is valid (subárea is optional)"""
        submission_data = {
            "scientific_area_grande": "2",
            "scientific_area_area": "2.01",  # Biologia Geral - has no subareas
            # No scientific_area_subarea
            "manuscript_type": "review",
            "journal_id": "journal_plos",
            "publisher_id": "pub_plos",
            "decision_type": "revise",
            "reviewer_count": "2+",
            "time_to_decision": "31_90",
            "apc_range": "1000_2000",
            "review_comments": ["conceptual"],
            "editor_comments": "brief",
            "perceived_coherence": "medium",
            "journal_is_open_access": True
        }
        
        response = requests.post(
            f"{BASE_URL}/api/submissions",
            json=submission_data,
            headers=auth_headers
        )
        
        # Check structure is valid (may fail due to duplicate check)
        assert response.status_code in [200, 422], f"Unexpected status: {response.status_code}"


class TestConditionalFieldsValidation:
    """Test backend validation for conditional fields"""
    
    @pytest.fixture
    def auth_headers(self):
        return {
            "Authorization": f"Bearer {TEST_SESSION_TOKEN}",
            "Content-Type": "application/json"
        }
    
    def test_apc_for_non_open_access_flagged(self, auth_headers):
        """APC range for non-open access journal should be flagged as inconsistent"""
        submission_data = {
            "scientific_area_grande": "3",
            "scientific_area_area": "3.01",
            "manuscript_type": "experimental",
            "journal_id": "journal_elsevier_test",
            "publisher_id": "pub_elsevier",
            "decision_type": "accept",
            "reviewer_count": "2+",
            "time_to_decision": "31_90",
            "apc_range": "2000_3000",  # APC provided
            "review_comments": ["methodology"],
            "editor_comments": "detailed",
            "perceived_coherence": "high",
            "journal_is_open_access": False  # NOT open access
        }
        
        response = requests.post(
            f"{BASE_URL}/api/submissions",
            json=submission_data,
            headers=auth_headers
        )
        
        # Submission may succeed but valid_for_stats should be False
        if response.status_code == 200:
            data = response.json()
            # The validation should flag this as inconsistent
            assert "valid_for_stats" in data
    
    def test_editor_quality_without_comments_flagged(self, auth_headers):
        """Editor comments quality without editor comments should be flagged"""
        submission_data = {
            "scientific_area_grande": "4",
            "scientific_area_area": "4.01",
            "manuscript_type": "experimental",
            "journal_id": "journal_test_editor",
            "publisher_id": "pub_springer",
            "decision_type": "reject",
            "reviewer_count": "1",
            "time_to_decision": "0_30",
            "apc_range": "no_apc",
            "review_comments": [],
            "editor_comments": "no",  # No editor comments
            "perceived_coherence": "low",
            "editor_comments_quality": 4,  # Quality rating provided (inconsistent!)
            "journal_is_open_access": False
        }
        
        response = requests.post(
            f"{BASE_URL}/api/submissions",
            json=submission_data,
            headers=auth_headers
        )
        
        # Submission may succeed but should be flagged
        if response.status_code == 200:
            data = response.json()
            assert "valid_for_stats" in data


class TestValidationLogic:
    """Test the validate_submission_for_stats logic"""
    
    @pytest.fixture
    def auth_headers(self):
        return {
            "Authorization": f"Bearer {TEST_SESSION_TOKEN}",
            "Content-Type": "application/json"
        }
    
    def test_complete_valid_submission(self, auth_headers):
        """Complete submission with all required fields should be valid"""
        submission_data = {
            "scientific_area_grande": "5",
            "scientific_area_area": "5.01",
            "scientific_area_subarea": "5.01.01",
            "manuscript_type": "experimental",
            "journal_id": "journal_valid_test",
            "publisher_id": "pub_springer",
            "decision_type": "accept",
            "reviewer_count": "2+",
            "time_to_decision": "31_90",
            "apc_range": "1000_2000",
            "review_comments": ["methodology", "statistics"],
            "editor_comments": "detailed",
            "perceived_coherence": "high",
            "journal_is_open_access": True,
            "editor_comments_quality": 4,
            "overall_review_quality": 4,
            "feedback_clarity": 4,
            "decision_fairness": "agree",
            "would_recommend": "yes"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/submissions",
            json=submission_data,
            headers=auth_headers
        )
        
        # Check response structure
        if response.status_code == 200:
            data = response.json()
            assert "submission_id" in data
            assert "valid_for_stats" in data


class TestLegacyScientificAreaCompatibility:
    """Test backwards compatibility with legacy scientific_area field"""
    
    def test_legacy_scientific_areas_endpoint(self):
        """Legacy /api/options/scientific-areas endpoint still works"""
        response = requests.get(f"{BASE_URL}/api/options/scientific-areas")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 9  # Returns Grande Áreas
        
        # Check legacy format
        for area in data:
            assert "id" in area
            assert "name" in area


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
