import React from "react";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { Toaster } from "./components/ui/sonner";
import { LanguageProvider } from "./i18n/LanguageContext";
import { AuthProvider } from "./contexts/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import RequireOrcid from "./components/RequireOrcid"; // <--- IMPORTANTE: Novo componente
import AuthCallback from "./components/AuthCallback";
import OrcidCallback from "./components/OrcidCallback";
import GoogleCallback from "./components/GoogleCallback";

// Pages
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import SubmissionPage from "./pages/SubmissionPage";
import AnalyticsPage from "./pages/AnalyticsPage";
import SettingsPage from "./pages/SettingsPage";
import TermsPage from "./pages/TermsPage";
import PrivacyPage from "./pages/PrivacyPage";
import AdminPage from "./pages/AdminPage";


import "./App.css";

// Router component that handles session_id detection
function AppRouter() {
  const location = useLocation();
  
  // MANTENHA: Isso intercepta o redirecionamento do Google via hash na URL
  // Evita condição de corrida antes de montar as rotas
  if (location.hash?.includes('session_id=')) {
    return <AuthCallback />;
  }

  return (
    <Routes>
      {/* Rotas Públicas */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/analytics" element={<AnalyticsPage />} />
      <Route path="/terms" element={<TermsPage />} />
      <Route path="/privacy" element={<PrivacyPage />} />
      
      {/* Rotas de Callback de Autenticação */}
      <Route path="/auth/callback" element={<AuthCallback />} />
      <Route path="/auth/orcid/callback" element={<OrcidCallback />} />

      {/* Rota especial para capturar o retorno do Google que o Backend perdeu */}
      <Route path="/api/auth/google/callback" element={<GoogleCallback />} />
      
      {/* Rotas Protegidas (Exigem Login) */}
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <DashboardPage />
        </ProtectedRoute>
      } />

      {/* Rota Protegida + Verificada (Exige Login + ORCID) */}
      <Route path="/submit" element={
        <ProtectedRoute>
          <RequireOrcid> {/* <--- AQUI: O Guarda-Costas do ORCID */}
            <SubmissionPage />
          </RequireOrcid>
        </ProtectedRoute>
      } />

      <Route path="/settings" element={
        <ProtectedRoute>
          <SettingsPage />
        </ProtectedRoute>
      } />

      <Route path="/admin" element={
        <ProtectedRoute>
          <AdminPage />
        </ProtectedRoute>
      } />
    </Routes>
  );
}

function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
        <BrowserRouter>
          <AppRouter />
          <Toaster position="top-right" richColors />
        </BrowserRouter>
      </AuthProvider>
    </LanguageProvider>
  );
}

export default App;
