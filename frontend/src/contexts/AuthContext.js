import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

const AuthContext = createContext();

const API = process.env.REACT_APP_BACKEND_URL + '/api';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [orcidConfigured, setOrcidConfigured] = useState(false);
  const [authVersion, setAuthVersion] = useState(0); // Force re-render on auth changes

  // 1. Check Authentication Status (COM CREDENTIALS: INCLUDE)
  const checkAuth = useCallback(async () => {
    try {
      const response = await fetch(`${API}/auth/me`, {
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include' // <--- ESSENCIAL: Envia o Cookie da sessão para o backend
      });
      
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        setAuthVersion(v => v + 1);
      } else {
        setUser(null);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  // 2. Check ORCID Status
  const checkOrcidStatus = useCallback(async () => {
    try {
      const response = await fetch(`${API}/auth/orcid/status`);
      if (response.ok) {
        const data = await response.json();
        setOrcidConfigured(data.configured);
      }
    } catch (error) {
      console.error('ORCID status check failed:', error);
    }
  }, []);

  useEffect(() => {
    checkAuth();
    checkOrcidStatus();
  }, [checkAuth, checkOrcidStatus]);

  // 3. Login With Google (ATUALIZADO para Self-Hosted)
  // Agora essa função aponta para o SEU backend, não para a Emergent
  const loginWithGoogle = async () => {
    try {
      const response = await fetch(`${API}/auth/google/authorize`);
      if (response.ok) {
        const data = await response.json();
        window.location.href = data.url;
      } else {
        console.error("Failed to get Google auth URL");
      }
    } catch (error) {
      console.error("Google login error:", error);
    }
  };

  // 4. Login With ORCID
  const loginWithOrcid = async (redirectAfter = '/dashboard') => {
    try {
      const response = await fetch(`${API}/auth/orcid/authorize?redirect=${encodeURIComponent(redirectAfter)}`, {
        headers: {
          'Origin': window.location.origin
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to initiate ORCID authentication');
      }
      
      const data = await response.json();
      sessionStorage.setItem('orcid_state', data.state);
      window.location.href = data.authorization_url;
    } catch (error) {
      console.error('ORCID auth initiation error:', error);
      throw error;
    }
  };

  // 5. Process ORCID Callback
  const processOrcidCallback = async (code, state) => {
    try {
      const storedState = sessionStorage.getItem('orcid_state');
      if (storedState && state !== storedState) {
        throw new Error('State mismatch - possible CSRF attack');
      }
      
      sessionStorage.removeItem('orcid_state');
      
      const response = await fetch(`${API}/auth/orcid/callback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include', // Importante
        body: JSON.stringify({ code, state })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'ORCID authentication failed');
      }

      const userData = await response.json();
      setUser(userData);
      setAuthVersion(v => v + 1);
      return userData;
    } catch (error) {
      console.error('ORCID callback error:', error);
      throw error;
    }
  };

  // 6. Logout
  const logout = async () => {
    try {
      await fetch(`${API}/auth/logout`, {
        method: 'POST',
        credentials: 'include' // Importante para apagar o cookie
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
    setUser(null);
    setAuthVersion(v => v + 1);
    setTimeout(() => {
      window.location.href = '/login'; // Redireciona para login
    }, 100);
  };

  // 7. Process Session (Legacy/Emergent) - Mantido para compatibilidade
  const processSession = async (sessionId) => {
    try {
      const response = await fetch(`${API}/auth/session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Session-ID': sessionId
        },
        credentials: 'include',
        body: JSON.stringify({ session_id: sessionId })
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        setAuthVersion(v => v + 1);
        return userData;
      }
      throw new Error('Session processing failed');
    } catch (error) {
      console.error('Session processing error:', error);
      throw error;
    }
  };

  // 8. Update Profile
  const updateProfile = async (data) => {
    try {
      const response = await fetch(`${API}/users/profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(data)
      });

      if (response.ok) {
        const updatedUser = await response.json();
        setUser(prev => ({ ...prev, ...updatedUser }));
        return updatedUser;
      }
      throw new Error('Profile update failed');
    } catch (error) {
      console.error('Profile update error:', error);
      throw error;
    }
  };

  const isAuthenticated = !!user;
  const isAdmin = user?.is_admin === true;
  const trustScoreVisible = user?.trust_score_visible || false;

  return (
    <AuthContext.Provider value={{ 
      user, 
      loading, 
      loginWithGoogle, 
      loginWithOrcid, 
      processOrcidCallback, 
      logout, 
      processSession, 
      updateProfile, 
      checkAuth, 
      isAuthenticated, 
      isAdmin, 
      trustScoreVisible, 
      orcidConfigured, 
      authVersion
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
