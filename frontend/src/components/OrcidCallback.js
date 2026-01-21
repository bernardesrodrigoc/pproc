import React, { useEffect, useRef } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Loader2 } from 'lucide-react';
import { toast } from 'sonner';

export default function OrcidCallback() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { processOrcidCallback } = useAuth();
  const hasProcessed = useRef(false);

  useEffect(() => {
    // Prevent double processing in StrictMode
    if (hasProcessed.current) return;
    hasProcessed.current = true;

    const processAuth = async () => {
      try {
        // Extract code and state from URL params
        const code = searchParams.get('code');
        const state = searchParams.get('state');
        const error = searchParams.get('error');
        const errorDescription = searchParams.get('error_description');

        if (error) {
          console.error('ORCID OAuth error:', error, errorDescription);
          toast.error(errorDescription || 'Authentication was denied');
          navigate('/login', { replace: true });
          return;
        }

        if (!code) {
          console.error('No authorization code found');
          toast.error('Authentication failed - no authorization code');
          navigate('/login', { replace: true });
          return;
        }

        // Process the ORCID callback
        const userData = await processOrcidCallback(code, state);
        
        // Get redirect from response or default to dashboard
        const redirectTo = userData.redirect || '/dashboard';
        
        toast.success('Signed in successfully');
        navigate(redirectTo, { replace: true });
      } catch (error) {
        console.error('ORCID callback error:', error);
        toast.error(error.message || 'Authentication failed');
        navigate('/login', { replace: true });
      }
    };

    processAuth();
  }, [searchParams, navigate, processOrcidCallback]);

  return (
    <div className="min-h-screen bg-[#FAFAF9] flex items-center justify-center">
      <div className="text-center">
        <Loader2 className="w-8 h-8 animate-spin text-stone-600 mx-auto mb-4" />
        <p className="text-stone-600 font-sans">Completing ORCID authentication...</p>
      </div>
    </div>
  );
}
