import React, { useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext'; // Vamos usar o login manual do contexto ou fetch direto
import { toast } from 'sonner';
import { Loader2 } from 'lucide-react';

export default function GoogleCallback() {
  const navigate = useNavigate();
  const location = useLocation();
  const hasFetched = useRef(false);

  useEffect(() => {
    if (hasFetched.current) return;
    hasFetched.current = true;

    const processGoogleLogin = async () => {
      // 1. Pega o código da URL
      const params = new URLSearchParams(location.search);
      const code = params.get('code');
      const error = params.get('error');

      if (error) {
        toast.error("Google authentication failed");
        navigate('/login');
        return;
      }

      if (!code) {
        toast.error("No code received from Google");
        navigate('/login');
        return;
      }

      try {
        // 2. Envia o código para o Backend (troca manual)
        const API_URL = process.env.REACT_APP_BACKEND_URL + '/api';
        
        const response = await fetch(`${API_URL}/auth/google/exchange`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to exchange token");
        }

        // 3. Sucesso! Recarrega a página para pegar a sessão (cookie)
        // Usamos window.location.href para forçar o refresh do AuthContext
        window.location.href = '/dashboard';

      } catch (err) {
        console.error("Google Auth Error:", err);
        toast.error("Login failed. Please try again.");
        navigate('/login');
      }
    };

    processGoogleLogin();
  }, [location, navigate]);

  return (
    <div className="min-h-screen bg-[#FAFAF9] flex flex-col items-center justify-center">
      <div className="text-center space-y-4">
        <Loader2 className="w-10 h-10 animate-spin text-stone-600 mx-auto" />
        <h2 className="text-xl font-serif text-stone-900">Finalizing Google Login...</h2>
      </div>
    </div>
  );
}
