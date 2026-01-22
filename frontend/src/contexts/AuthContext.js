import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

const AuthContext = createContext();

const API = process.env.REACT_APP_BACKEND_URL + '/api';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [orcidConfigured, setOrcidConfigured] = useState(false);
  const [authVersion, setAuthVersion] = useState(0); // Force re-render on auth changes

  const checkAuth = useCallback(async () => {
    try {
      const response = await fetch(`${API}/auth/me`, {
        credentials: 'include'
      });
      
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        setAuthVersion(v => v + 1); // Force components to re-check auth state
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

  // Check if ORCID OAuth is configured
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

  const loginWithGoogle = () => {
    // REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
    const redirectUrl = window.location.origin + '/auth/callback'; 
    window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
  };

  const loginWithOrcid = async (redirectAfter = '/dashboard') => {
    try {
      // Get the ORCID authorization URL from backend
      const response = await fetch(`${API}/auth/orcid/authorize?redirect=${encodeURIComponent(redirectAfter)}`, {
        headers: {
          'Origin': window.location.origin
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to initiate ORCID authentication');
      }
      
      const data = await response.json();
      
      // Store state for callback verification
      sessionStorage.setItem('orcid_state', data.state);
      
      // Redirect to ORCID authorization page
      window.location.href = data.authorization_url;
    } catch (error) {
      console.error('ORCID auth initiation error:', error);
      throw error;
    }
  };

  const processOrcidCallback = async (code, state) => {
    try {
      // Verify state matches
      const storedState = sessionStorage.getItem('orcid_state');
      if (storedState && state !== storedState) {
        throw new Error('State mismatch - possible CSRF attack');
      }
      
      // Clear stored state
      sessionStorage.removeItem('orcid_state');
      
      // Exchange code for session - redirect_uri is handled by backend env var
      const response = await fetch(`${API}/auth/orcid/callback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({
          code,
          state
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'ORCID authentication failed');
      }

      const userData = await response.json();
      setUser(userData);
      setAuthVersion(v => v + 1); // Force re-render
      return userData;
    } catch (error) {
      console.error('ORCID callback error:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await fetch(`${API}/auth/logout`, {
        method: 'POST',
        credentials: 'include'
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
    // Clear ALL auth state immediately and synchronously
    setUser(null);
    setAuthVersion(v => v + 1);
    // Don't redirect immediately - let state update propagate
    setTimeout(() => {
      window.location.href = '/';
    }, 100);
  };

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
        // Set user state BEFORE returning
        setUser(userData);
        setAuthVersion(v => v + 1); // Force components to update
        return userData;
      }
      throw new Error('Session processing failed');
    } catch (error) {
      console.error('Session processing error:', error);
      throw error;
    }
  };

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

  // Compute derived state values
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
      authVersion // Expose for components that need to force re-render
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
