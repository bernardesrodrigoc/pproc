import React, { useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Loader2 } from 'lucide-react';

export default function AuthCallback() {
  const navigate = useNavigate();
  const location = useLocation();
  const { processSession, checkAuth } = useAuth();
  const hasProcessed = useRef(false);

  useEffect(() => {
    // Prevent double processing in StrictMode
    if (hasProcessed.current) return;
    hasProcessed.current = true;

    const processAuth = async () => {
      try {
        // Extract session_id from URL hash
        const hash = location.hash;
        const params = new URLSearchParams(hash.replace('#', ''));
        const sessionId = params.get('session_id');

        if (!sessionId) {
          console.error('No session_id found');
          navigate('/login', { replace: true });
          return;
        }

        // Process the session and wait for it to complete
        await processSession(sessionId);
        
        // Small delay to ensure React state has propagated
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // Double-check auth state is updated
        await checkAuth();
        
        // Navigate to dashboard
        navigate('/dashboard', { replace: true });
      } catch (error) {
        console.error('Auth callback error:', error);
        navigate('/login', { replace: true });
      }
    };

    processAuth();
  }, [location, navigate, processSession, checkAuth]);

  return (
    <div className="min-h-screen bg-[#FAFAF9] flex items-center justify-center">
      <div className="text-center">
        <Loader2 className="w-8 h-8 animate-spin text-stone-600 mx-auto mb-4" />
        <p className="text-stone-600 font-sans">Signing you in...</p>
      </div>
    </div>
  );
}
