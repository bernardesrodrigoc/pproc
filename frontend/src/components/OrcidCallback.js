import React, { useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'sonner';
import { Loader2 } from 'lucide-react';

export default function OrcidCallback() {
  const navigate = useNavigate();
  const location = useLocation();
  // IMPORTANTE: Trouxemos o 'logout' e 'loginWithOrcid' para usar na ação do botão
  const { processOrcidCallback, logout, loginWithOrcid } = useAuth();
  const hasProcessed = useRef(false);

  useEffect(() => {
    // Evita processamento duplo (React Strict Mode)
    if (hasProcessed.current) return;
    hasProcessed.current = true;

    const processAuth = async () => {
      const params = new URLSearchParams(location.search);
      const code = params.get('code');
      const state = params.get('state');
      const error = params.get('error');

      // 1. Usuário cancelou no site do ORCID
      if (error) {
        toast.error("Authentication cancelled by user");
        navigate('/settings'); // Volta para settings
        return;
      }

      if (!code) {
        toast.error("No authorization code received");
        navigate('/login');
        return;
      }

      try {
        // 2. Tenta processar o vínculo
        const result = await processOrcidCallback(code, state);
        
        // Sucesso
        const redirectUrl = result.redirect || '/dashboard';
        toast.success("Successfully connected to ORCID");
        navigate(redirectUrl, { replace: true });

      } catch (err) {
        console.error('ORCID Auth Error:', err);

        // --- LÓGICA DO BOTÃO INTELIGENTE (SMART SWITCH) ---
        
        // Verifica se é o erro de conflito (409)
        if (err.message && (err.message.includes("já está conectado") || err.message.includes("already connected") || err.message.includes("409"))) {
            
            // Mostra o "Popup" (Toast) com o botão de ação
            toast.error("Account Conflict Detected", {
                description: "This ORCID iD is already linked to another account on our platform.",
                duration: 10000, // 10 segundos para ele ler e decidir
                action: {
                    label: "Log in to that account", // O texto do botão
                    onClick: async () => {
                        // A MÁGICA ACONTECE AQUI:
                        // 1. Desloga da conta atual (Google/Email)
                        await logout(); 
                        // 2. Inicia o login direto pelo ORCID
                        await loginWithOrcid('/dashboard');
                    }
                }
            });

            // Devolve o usuário para a tela de configurações enquanto ele decide
            navigate('/settings', { replace: true });
        } 
        else {
            // Outros erros genéricos
            toast.error("Authentication failed", {
                description: "An unexpected error occurred. Please try again."
            });
            navigate('/settings', { replace: true });
        }
      }
    };

    processAuth();
  }, [location, navigate, processOrcidCallback, logout, loginWithOrcid]);

  return (
    <div className="min-h-screen bg-[#FAFAF9] flex flex-col items-center justify-center p-4">
      <div className="text-center space-y-4">
        <Loader2 className="w-10 h-10 animate-spin text-stone-600 mx-auto" />
        <div>
          <h2 className="text-xl font-serif text-stone-900">Verifying ORCID...</h2>
          <p className="text-stone-500 text-sm">Please wait while we confirm your identity</p>
        </div>
      </div>
    </div>
  );
}
