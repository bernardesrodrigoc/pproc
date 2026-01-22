"""
Test suite for Admin Diagnostics, Areas CRUD, CNPq from DB, and Threshold Visibility
Tests the critical fixes implemented:
1. Admin Diagnostics endpoint
2. Admin Areas CRUD (POST, PUT, DELETE)
3. CNPq areas from database
4. Threshold-based visibility logic
5. Analytics overview with real data
"""

import pytest
import requests
import os
import time
from datetime import datetime, timedelta

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://editcheck.preview.emergentagent.com').rstrip('/')

# Admin credentials for testing
ADMIN_EMAIL = "bernardesrodrigoc@gmail.com"


class TestHealthAndBasicEndpoints:
    """Basic health and connectivity tests"""
    
    def test_health_endpoint(self):
        """Test API health endpoint"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"
        print(f"✓ Health check passed: {data}")
    
    def test_visibility_status_endpoint(self):
        """Test visibility status endpoint (public)"""
        response = requests.get(f"{BASE_URL}/api/analytics/visibility-status")
        assert response.status_code == 200
        data = response.json()
        assert "visibility_mode" in data
        assert "public_stats_enabled" in data
        assert "demo_mode_enabled" in data
        print(f"✓ Visibility status: mode={data['visibility_mode']}, public={data['public_stats_enabled']}, demo={data['demo_mode_enabled']}")


class TestCNPQAreasFromDatabase:
    """Test CNPq areas endpoints - now served from database"""
    
    def test_get_grande_areas(self):
        """Test GET /api/options/cnpq/grande-areas returns areas from DB"""
        response = requests.get(f"{BASE_URL}/api/options/cnpq/grande-areas")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0, "Should have at least one grande area"
        
        # Check structure of first area
        first_area = data[0]
        assert "code" in first_area
        assert "name" in first_area
        assert "name_en" in first_area
        print(f"✓ Grande areas: {len(data)} areas returned")
        print(f"  First area: {first_area['code']} - {first_area['name']}")
    
    def test_get_areas_by_grande_area(self):
        """Test GET /api/options/cnpq/areas/{code} returns areas for a grande area"""
        # First get grande areas
        ga_response = requests.get(f"{BASE_URL}/api/options/cnpq/grande-areas")
        assert ga_response.status_code == 200
        grande_areas = ga_response.json()
        
        if grande_areas:
            first_ga_code = grande_areas[0]["code"]
            response = requests.get(f"{BASE_URL}/api/options/cnpq/areas/{first_ga_code}")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            print(f"✓ Areas for grande area {first_ga_code}: {len(data)} areas")
    
    def test_get_subareas_by_area(self):
        """Test GET /api/options/cnpq/subareas/{code} returns subareas"""
        # Get grande areas first
        ga_response = requests.get(f"{BASE_URL}/api/options/cnpq/grande-areas")
        grande_areas = ga_response.json()
        
        if grande_areas:
            first_ga_code = grande_areas[0]["code"]
            areas_response = requests.get(f"{BASE_URL}/api/options/cnpq/areas/{first_ga_code}")
            areas = areas_response.json()
            
            if areas:
                first_area_code = areas[0]["code"]
                response = requests.get(f"{BASE_URL}/api/options/cnpq/subareas/{first_area_code}")
                assert response.status_code == 200
                data = response.json()
                assert isinstance(data, list)
                print(f"✓ Subareas for area {first_area_code}: {len(data)} subareas")


class TestAdminDiagnosticsEndpoint:
    """Test Admin Diagnostics endpoint - requires admin auth"""
    
    @pytest.fixture
    def admin_session(self):
        """Create admin session for testing"""
        # For testing, we'll use direct MongoDB to create a test admin session
        # In production, this would use proper OAuth flow
        import subprocess
        import json
        
        # Create test admin user and session
        timestamp = int(time.time())
        session_token = f"test_admin_session_{timestamp}"
        user_id = f"test_admin_{timestamp}"
        
        mongo_script = f'''
        use test_database;
        
        // Check if admin user exists
        var existingAdmin = db.users.findOne({{email: "{ADMIN_EMAIL}"}});
        var userId = existingAdmin ? existingAdmin.user_id : "{user_id}";
        
        if (!existingAdmin) {{
            db.users.insertOne({{
                user_id: userId,
                email: "{ADMIN_EMAIL}",
                name: "Test Admin",
                hashed_id: "test_hashed_{timestamp}",
                trust_score: 100.0,
                contribution_count: 0,
                is_admin: true,
                created_at: new Date().toISOString()
            }});
        }} else {{
            db.users.updateOne(
                {{email: "{ADMIN_EMAIL}"}},
                {{$set: {{is_admin: true}}}}
            );
        }}
        
        // Create session
        db.user_sessions.insertOne({{
            session_id: "sess_{timestamp}",
            user_id: userId,
            session_token: "{session_token}",
            expires_at: new Date(Date.now() + 24*60*60*1000).toISOString(),
            created_at: new Date().toISOString()
        }});
        
        print("{session_token}");
        '''
        
        result = subprocess.run(
            ["mongosh", "--quiet", "--eval", mongo_script],
            capture_output=True,
            text=True
        )
        
        yield session_token
        
        # Cleanup
        cleanup_script = f'''
        use test_database;
        db.user_sessions.deleteOne({{session_token: "{session_token}"}});
        '''
        subprocess.run(["mongosh", "--quiet", "--eval", cleanup_script], capture_output=True)
    
    def test_diagnostics_endpoint_requires_auth(self):
        """Test that diagnostics endpoint requires authentication"""
        response = requests.get(f"{BASE_URL}/api/admin/diagnostics")
        assert response.status_code == 401
        print("✓ Diagnostics endpoint correctly requires authentication")
    
    def test_diagnostics_endpoint_returns_data(self, admin_session):
        """Test diagnostics endpoint returns comprehensive data"""
        headers = {"Authorization": f"Bearer {admin_session}"}
        response = requests.get(f"{BASE_URL}/api/admin/diagnostics", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check structure
        assert "platform_settings" in data
        assert "data_summary" in data
        assert "visibility_summary" in data
        assert "journal_details" in data
        
        # Check platform_settings
        settings = data["platform_settings"]
        assert "visibility_mode" in settings
        assert "public_stats_enabled" in settings
        assert "demo_mode_enabled" in settings
        assert "min_submissions_per_journal" in settings
        assert "min_unique_users_per_journal" in settings
        
        # Check data_summary
        summary = data["data_summary"]
        assert "total_submissions" in summary
        assert "sample_submissions" in summary
        assert "real_submissions" in summary
        assert "valid_real_submissions" in summary
        assert "unique_real_users" in summary
        
        # Check visibility_summary
        vis_summary = data["visibility_summary"]
        assert "visible_journals" in vis_summary
        assert "hidden_journals" in vis_summary
        assert "visibility_mode_explanation" in vis_summary
        
        print(f"✓ Diagnostics data returned successfully:")
        print(f"  - Total submissions: {summary['total_submissions']}")
        print(f"  - Real submissions: {summary['real_submissions']}")
        print(f"  - Valid real submissions: {summary['valid_real_submissions']}")
        print(f"  - Unique real users: {summary['unique_real_users']}")
        print(f"  - Visibility mode: {settings['visibility_mode']}")
        print(f"  - Visible journals: {vis_summary['visible_journals']}")


class TestAdminAreasCRUD:
    """Test Admin Areas CRUD operations"""
    
    @pytest.fixture
    def admin_session(self):
        """Create admin session for testing"""
        import subprocess
        
        timestamp = int(time.time())
        session_token = f"test_admin_areas_{timestamp}"
        user_id = f"test_admin_areas_{timestamp}"
        
        mongo_script = f'''
        use test_database;
        
        var existingAdmin = db.users.findOne({{email: "{ADMIN_EMAIL}"}});
        var userId = existingAdmin ? existingAdmin.user_id : "{user_id}";
        
        if (!existingAdmin) {{
            db.users.insertOne({{
                user_id: userId,
                email: "{ADMIN_EMAIL}",
                name: "Test Admin",
                hashed_id: "test_hashed_{timestamp}",
                trust_score: 100.0,
                is_admin: true,
                created_at: new Date().toISOString()
            }});
        }} else {{
            db.users.updateOne(
                {{email: "{ADMIN_EMAIL}"}},
                {{$set: {{is_admin: true}}}}
            );
        }}
        
        db.user_sessions.insertOne({{
            session_id: "sess_areas_{timestamp}",
            user_id: userId,
            session_token: "{session_token}",
            expires_at: new Date(Date.now() + 24*60*60*1000).toISOString(),
            created_at: new Date().toISOString()
        }});
        
        print("{session_token}");
        '''
        
        subprocess.run(["mongosh", "--quiet", "--eval", mongo_script], capture_output=True)
        
        yield session_token
        
        # Cleanup
        cleanup_script = f'''
        use test_database;
        db.user_sessions.deleteOne({{session_token: "{session_token}"}});
        db.scientific_areas.deleteOne({{code: "TEST_99"}});
        '''
        subprocess.run(["mongosh", "--quiet", "--eval", cleanup_script], capture_output=True)
    
    def test_get_admin_areas(self, admin_session):
        """Test GET /api/admin/areas returns all areas"""
        headers = {"Authorization": f"Bearer {admin_session}"}
        response = requests.get(f"{BASE_URL}/api/admin/areas", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "summary" in data
        assert "grande_areas" in data
        assert "areas" in data
        assert "subareas" in data
        
        summary = data["summary"]
        assert "total" in summary
        assert "grande_areas" in summary
        assert "areas" in summary
        assert "subareas" in summary
        
        print(f"✓ Admin areas returned: {summary['total']} total")
        print(f"  - Grande areas: {summary['grande_areas']}")
        print(f"  - Areas: {summary['areas']}")
        print(f"  - Subareas: {summary['subareas']}")
    
    def test_create_area(self, admin_session):
        """Test POST /api/admin/areas creates new area"""
        headers = {
            "Authorization": f"Bearer {admin_session}",
            "Content-Type": "application/json"
        }
        
        new_area = {
            "code": "TEST_99",
            "name": "Área de Teste",
            "name_en": "Test Area",
            "level": "grande_area",
            "parent_code": None
        }
        
        response = requests.post(
            f"{BASE_URL}/api/admin/areas",
            headers=headers,
            json=new_area
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["code"] == "TEST_99"
        assert data["name"] == "Área de Teste"
        assert data["name_en"] == "Test Area"
        assert data["level"] == "grande_area"
        assert data["is_active"] == True
        
        print(f"✓ Area created: {data['code']} - {data['name']}")
    
    def test_update_area(self, admin_session):
        """Test PUT /api/admin/areas/{code} updates area"""
        headers = {
            "Authorization": f"Bearer {admin_session}",
            "Content-Type": "application/json"
        }
        
        # First create the area
        new_area = {
            "code": "TEST_99",
            "name": "Área de Teste",
            "name_en": "Test Area",
            "level": "grande_area",
            "parent_code": None
        }
        requests.post(f"{BASE_URL}/api/admin/areas", headers=headers, json=new_area)
        
        # Update the area
        update_data = {
            "name": "Área de Teste Atualizada",
            "name_en": "Updated Test Area"
        }
        
        response = requests.put(
            f"{BASE_URL}/api/admin/areas/TEST_99",
            headers=headers,
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["name"] == "Área de Teste Atualizada"
        assert data["name_en"] == "Updated Test Area"
        
        print(f"✓ Area updated: {data['code']} - {data['name']}")
    
    def test_delete_area_soft_delete(self, admin_session):
        """Test DELETE /api/admin/areas/{code} soft deletes area"""
        headers = {
            "Authorization": f"Bearer {admin_session}",
            "Content-Type": "application/json"
        }
        
        # First create the area
        new_area = {
            "code": "TEST_99",
            "name": "Área de Teste",
            "name_en": "Test Area",
            "level": "grande_area",
            "parent_code": None
        }
        requests.post(f"{BASE_URL}/api/admin/areas", headers=headers, json=new_area)
        
        # Delete the area
        response = requests.delete(
            f"{BASE_URL}/api/admin/areas/TEST_99",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should be hard delete since no submissions
        assert "deleted" in data.get("message", "").lower() or "disabled" in data.get("message", "").lower()
        
        print(f"✓ Area deleted/disabled: {data}")


class TestThresholdVisibility:
    """Test threshold-based visibility logic"""
    
    def test_analytics_overview_public(self):
        """Test analytics overview endpoint"""
        response = requests.get(f"{BASE_URL}/api/analytics/overview")
        assert response.status_code == 200
        data = response.json()
        
        # Check basic structure
        assert "sufficient_data" in data
        
        print(f"✓ Analytics overview returned:")
        print(f"  - Sufficient data: {data.get('sufficient_data')}")
        print(f"  - Visibility restricted: {data.get('visibility_restricted')}")
        
        if data.get("sufficient_data"):
            print(f"  - Decision distribution: {data.get('decision_distribution')}")
    
    def test_analytics_publishers(self):
        """Test analytics publishers endpoint"""
        response = requests.get(f"{BASE_URL}/api/analytics/publishers")
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        print(f"✓ Analytics publishers: {len(data)} publishers returned")
    
    def test_analytics_journals(self):
        """Test analytics journals endpoint"""
        response = requests.get(f"{BASE_URL}/api/analytics/journals")
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        print(f"✓ Analytics journals: {len(data)} journals returned")
    
    def test_analytics_areas(self):
        """Test analytics areas endpoint"""
        response = requests.get(f"{BASE_URL}/api/analytics/areas")
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        print(f"✓ Analytics areas: {len(data)} areas returned")


class TestAdminSettings:
    """Test admin settings endpoints"""
    
    @pytest.fixture
    def admin_session(self):
        """Create admin session for testing"""
        import subprocess
        
        timestamp = int(time.time())
        session_token = f"test_admin_settings_{timestamp}"
        user_id = f"test_admin_settings_{timestamp}"
        
        mongo_script = f'''
        use test_database;
        
        var existingAdmin = db.users.findOne({{email: "{ADMIN_EMAIL}"}});
        var userId = existingAdmin ? existingAdmin.user_id : "{user_id}";
        
        if (!existingAdmin) {{
            db.users.insertOne({{
                user_id: userId,
                email: "{ADMIN_EMAIL}",
                name: "Test Admin",
                hashed_id: "test_hashed_{timestamp}",
                trust_score: 100.0,
                is_admin: true,
                created_at: new Date().toISOString()
            }});
        }} else {{
            db.users.updateOne(
                {{email: "{ADMIN_EMAIL}"}},
                {{$set: {{is_admin: true}}}}
            );
        }}
        
        db.user_sessions.insertOne({{
            session_id: "sess_settings_{timestamp}",
            user_id: userId,
            session_token: "{session_token}",
            expires_at: new Date(Date.now() + 24*60*60*1000).toISOString(),
            created_at: new Date().toISOString()
        }});
        
        print("{session_token}");
        '''
        
        subprocess.run(["mongosh", "--quiet", "--eval", mongo_script], capture_output=True)
        
        yield session_token
        
        # Cleanup
        cleanup_script = f'''
        use test_database;
        db.user_sessions.deleteOne({{session_token: "{session_token}"}});
        '''
        subprocess.run(["mongosh", "--quiet", "--eval", cleanup_script], capture_output=True)
    
    def test_get_admin_settings(self, admin_session):
        """Test GET /api/admin/settings returns platform settings"""
        headers = {"Authorization": f"Bearer {admin_session}"}
        response = requests.get(f"{BASE_URL}/api/admin/settings", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "visibility_mode" in data
        assert "public_stats_enabled" in data
        assert "demo_mode_enabled" in data
        assert "min_submissions_per_journal" in data
        assert "min_unique_users_per_journal" in data
        
        print(f"✓ Admin settings returned:")
        print(f"  - Visibility mode: {data['visibility_mode']}")
        print(f"  - Public stats: {data['public_stats_enabled']}")
        print(f"  - Demo mode: {data['demo_mode_enabled']}")
        print(f"  - Min submissions: {data['min_submissions_per_journal']}")
        print(f"  - Min users: {data['min_unique_users_per_journal']}")
    
    def test_get_data_stats(self, admin_session):
        """Test GET /api/admin/data/stats returns data statistics"""
        headers = {"Authorization": f"Bearer {admin_session}"}
        response = requests.get(f"{BASE_URL}/api/admin/data/stats", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "submissions" in data
        assert "users" in data
        
        subs = data["submissions"]
        assert "total" in subs
        assert "real" in subs
        assert "sample" in subs
        
        print(f"✓ Data stats returned:")
        print(f"  - Total submissions: {subs['total']}")
        print(f"  - Real submissions: {subs['real']}")
        print(f"  - Sample submissions: {subs['sample']}")


class TestDataIntegrity:
    """Test data integrity and sample data exclusion"""
    
    @pytest.fixture
    def admin_session(self):
        """Create admin session for testing"""
        import subprocess
        
        timestamp = int(time.time())
        session_token = f"test_admin_integrity_{timestamp}"
        user_id = f"test_admin_integrity_{timestamp}"
        
        mongo_script = f'''
        use test_database;
        
        var existingAdmin = db.users.findOne({{email: "{ADMIN_EMAIL}"}});
        var userId = existingAdmin ? existingAdmin.user_id : "{user_id}";
        
        if (!existingAdmin) {{
            db.users.insertOne({{
                user_id: userId,
                email: "{ADMIN_EMAIL}",
                name: "Test Admin",
                hashed_id: "test_hashed_{timestamp}",
                trust_score: 100.0,
                is_admin: true,
                created_at: new Date().toISOString()
            }});
        }} else {{
            db.users.updateOne(
                {{email: "{ADMIN_EMAIL}"}},
                {{$set: {{is_admin: true}}}}
            );
        }}
        
        db.user_sessions.insertOne({{
            session_id: "sess_integrity_{timestamp}",
            user_id: userId,
            session_token: "{session_token}",
            expires_at: new Date(Date.now() + 24*60*60*1000).toISOString(),
            created_at: new Date().toISOString()
        }});
        
        print("{session_token}");
        '''
        
        subprocess.run(["mongosh", "--quiet", "--eval", mongo_script], capture_output=True)
        
        yield session_token
        
        # Cleanup
        cleanup_script = f'''
        use test_database;
        db.user_sessions.deleteOne({{session_token: "{session_token}"}});
        '''
        subprocess.run(["mongosh", "--quiet", "--eval", cleanup_script], capture_output=True)
    
    def test_diagnostics_shows_correct_counts(self, admin_session):
        """Test that diagnostics shows correct submission counts"""
        headers = {"Authorization": f"Bearer {admin_session}"}
        response = requests.get(f"{BASE_URL}/api/admin/diagnostics", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        summary = data["data_summary"]
        
        # Verify counts are consistent
        total = summary["total_submissions"]
        sample = summary["sample_submissions"]
        real = summary["real_submissions"]
        
        # Total should equal sample + real
        assert total == sample + real, f"Total ({total}) should equal sample ({sample}) + real ({real})"
        
        # Valid real should be <= real
        valid_real = summary["valid_real_submissions"]
        assert valid_real <= real, f"Valid real ({valid_real}) should be <= real ({real})"
        
        print(f"✓ Data integrity verified:")
        print(f"  - Total: {total} = Sample: {sample} + Real: {real}")
        print(f"  - Valid real: {valid_real} <= Real: {real}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
