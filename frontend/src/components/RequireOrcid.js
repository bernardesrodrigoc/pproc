import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Button } from './ui/button';
import { ShieldAlert, ExternalLink } from 'lucide-react';

export default function RequireOrcid({ children }) {
  const { user, loginWithOrcid } = useAuth();

  // Se o usuário não tem ORCID (nem hash, nem provider), bloqueia
  const hasOrcid = !!(user?.has_orcid || user?.orcid_hash || user?.auth_provider === 'orcid');

  if (!hasOrcid) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center p-4">
        <Card className="max-w-md w-full border-orange-200 bg-orange-50/50">
          <CardHeader className="text-center">
            <div className="mx-auto w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mb-4">
              <ShieldAlert className="w-6 h-6 text-orange-600" />
            </div>
            <CardTitle className="text-stone-900">Researcher Verification Required</CardTitle>
            <CardDescription className="text-stone-600">
              To ensure scientific integrity, this action requires a verified researcher identity.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-stone-600 text-center">
              Please link your ORCID iD to unlock submissions, analytics, and peer review features.
            </p>
            <Button 
              onClick={() => loginWithOrcid(window.location.pathname)} 
              className="w-full bg-stone-900 hover:bg-stone-800 text-white"
            >
              Connect ORCID Now
              <ExternalLink className="w-4 h-4 ml-2" />
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Se tiver ORCID, libera o acesso ao conteúdo
  return children;
}
