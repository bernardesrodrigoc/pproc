import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../i18n/LanguageContext';
import { useAuth } from '../contexts/AuthContext';
import Navbar from '../components/Navbar';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Shield, Lock, Loader2 } from 'lucide-react';
import { toast } from 'sonner';

// Define a URL da API (garante que pega do .env)
const API_URL = process.env.REACT_APP_BACKEND_URL + '/api';

export default function LoginPage() {
  const { t } = useLanguage();
  // REMOVIDO: loginWithGoogle do useAuth (pois vamos usar a implementação própria)
  const { loginWithOrcid, isAuthenticated, orcidConfigured } = useAuth();
  const navigate = useNavigate();
  
  // States para loading
  const [orcidLoading, setOrcidLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false); // Novo state

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  // --- NOVA FUNÇÃO DE LOGIN COM GOOGLE (Self-Hosted) ---
  const handleGoogleLogin = async () => {
    setGoogleLoading(true);
    try {
      // 1. Pede ao backend a URL de autorização do Google
      const response = await fetch(`${API_URL}/auth/google/authorize`);
      
      if (!response.ok) {
        throw new Error('Failed to get authorization URL');
      }

      const data = await response.json();
      
      // 2. Redireciona o navegador para o Google
      window.location.href = data.url;
      
    } catch (error) {
      console.error("Google login error:", error);
      toast.error('Failed to initiate Google login. Please try again.');
      setGoogleLoading(false);
    }
  };
  // -----------------------------------------------------

  const handleOrcidLogin = async () => {
    if (!orcidConfigured) {
      toast.error('ORCID authentication is not yet configured. Please use Google sign-in.');
      return;
    }
    
    setOrcidLoading(true);
    try {
      await loginWithOrcid('/dashboard');
      // User will be redirected to ORCID
    } catch (error) {
      toast.error('Failed to initiate ORCID authentication');
      setOrcidLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FAFAF9]">
      <Navbar />
      
      <div className="flex min-h-[calc(100vh-64px)]">
        {/* Left side - Image */}
        <div className="hidden lg:block lg:w-1/2 relative">
          <img 
            src="https://images.pexels.com/photos/3992944/pexels-photo-3992944.jpeg"
            alt="Abstract background"
            className="absolute inset-0 w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-stone-900/60" />
          <div className="absolute inset-0 flex items-center justify-center p-12">
            <div className="text-center text-white">
              <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center mx-auto mb-6">
                <Shield className="w-8 h-8 text-white" />
              </div>
              <h2 className="font-serif text-3xl mb-4">Your Privacy Matters</h2>
              <p className="text-white/80 max-w-md">
                We never share individual submissions. All data is aggregated and anonymized to protect your identity.
              </p>
            </div>
          </div>
        </div>

        {/* Right side - Login form */}
        <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
          <Card className="w-full max-w-md border-stone-200 shadow-lg">
            <CardHeader className="text-center pb-2">
              <CardTitle className="font-serif text-2xl text-stone-900">
                {t('auth.signInTitle')}
              </CardTitle>
              <CardDescription className="text-stone-600">
                {t('auth.signInSubtitle')}
              </CardDescription>
            </CardHeader>
            <CardContent className="pt-6">
              <div className="space-y-4">
                
                {/* Google OAuth Button (ATUALIZADO) */}
                <Button 
                  onClick={handleGoogleLogin}
                  disabled={googleLoading || orcidLoading}
                  className="w-full bg-stone-900 text-white hover:bg-stone-800 py-6 text-base flex items-center justify-center space-x-3"
                  data-testid="google-login-btn"
                >
                  {googleLoading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <svg className="w-5 h-5" viewBox="0 0 24 24">
                      <path
                        fill="currentColor"
                        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                      />
                      <path
                        fill="currentColor"
                        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                      />
                      <path
                        fill="currentColor"
                        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                      />
                      <path
                        fill="currentColor"
                        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                      />
                    </svg>
                  )}
                  <span>{googleLoading ? "Connecting..." : "Continue with Google"}</span>
                </Button>

                <div className="relative">
                  <div className="absolute inset-0 flex items-center">
                    <span className="w-full border-t border-stone-200" />
                  </div>
                  <div className="relative flex justify-center text-xs uppercase">
                    <span className="bg-white px-2 text-stone-500">or</span>
                  </div>
                </div>

                {/* ORCID OAuth Button */}
                <Button 
                  onClick={handleOrcidLogin}
                  disabled={orcidLoading || googleLoading}
                  variant="outline"
                  className="w-full py-6 text-base flex items-center justify-center space-x-3 border-[#A6CE39] text-[#A6CE39] hover:bg-[#A6CE39]/10 disabled:opacity-50"
                  data-testid="orcid-login-btn"
                >
                  {orcidLoading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <svg className="w-5 h-5" viewBox="0 0 256 256" fill="currentColor">
                      <path d="M128 0C57.3 0 0 57.3 0 128s57.3 128 128 128 128-57.3 128-128S198.7 0 128 0zM82.8 200.8h-24V91.2h24v109.6zm-12-124.4c-7.7 0-14-6.3-14-14s6.3-14 14-14 14 6.3 14 14-6.3 14-14 14zm130.4 124.4h-24v-54.8c0-13.8-.3-31.6-19.2-31.6-19.3 0-22.2 15-22.2 30.6v55.8h-24V91.2h23v15h.3c3.2-6 11-12.3 22.6-12.3 24.2 0 28.7 16 28.7 36.6v70.3h-.2z"/>
                    </svg>
                  )}
                  <span>Continue with ORCID</span>
                </Button>

                {!orcidConfigured && (
                  <p className="text-xs text-amber-600 text-center">
                    ORCID authentication requires configuration. Contact administrator.
                  </p>
                )}
              </div>

              <div className="mt-6 p-4 bg-stone-50 rounded-lg border border-stone-100">
                <div className="flex items-start space-x-3">
                  <Lock className="w-5 h-5 text-stone-500 mt-0.5" />
                  <p className="text-sm text-stone-600">
                    Authentication is used only to prevent spam and duplicate submissions. All contributions remain anonymous.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
