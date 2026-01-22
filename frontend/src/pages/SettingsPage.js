import React from 'react';
import { useLanguage, LANGUAGES } from '../i18n/LanguageContext';
import { useAuth } from '../contexts/AuthContext';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Badge } from '../components/ui/badge';
import { Globe, User, Check, ExternalLink, ShieldCheck } from 'lucide-react';

export default function SettingsPage() {
  const { t, language, setLanguage } = useLanguage();
  const { user, loginWithOrcid } = useAuth();

  // Função para iniciar o vínculo com ORCID
  // O parâmetro '/settings' garante que o usuário volte para cá após conectar
  const handleConnectOrcid = () => {
    loginWithOrcid('/settings');
  };

  // Verifica se o usuário tem ORCID vinculado (seja hash ou ID real)
  const hasOrcid = !!(user?.has_orcid || user?.orcid || user?.orcid_hash || user?.auth_provider === 'orcid');

  return (
    <div className="min-h-screen bg-[#FAFAF9]">
      <Navbar />
      
      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12" data-testid="settings-page">
        <div className="mb-8">
          <h1 className="font-serif text-3xl text-stone-900 mb-2">
            {t('settings.title') || 'Settings'}
          </h1>
        </div>

        <div className="space-y-6">
          {/* Language Settings */}
          <Card className="border-stone-200">
            <CardHeader>
              <CardTitle className="font-serif text-lg flex items-center">
                <Globe className="w-5 h-5 mr-2 text-stone-500" />
                {t('settings.language')}
              </CardTitle>
              <CardDescription>
                Choose your preferred language for the interface
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-3">
                {LANGUAGES.map((lang) => (
                  <button
                    key={lang.code}
                    onClick={() => setLanguage(lang.code)}
                    className={`p-4 rounded-lg border-2 transition-all text-center
                      ${language === lang.code 
                        ? 'border-stone-900 bg-stone-50' 
                        : 'border-stone-200 hover:border-stone-300'
                      }`}
                    data-testid={`settings-lang-${lang.code}`}
                  >
                    <span className="text-2xl mb-2 block">{lang.flag}</span>
                    <span className="text-sm font-medium text-stone-700">{lang.name}</span>
                    {language === lang.code && (
                      <Check className="w-4 h-4 text-stone-900 mx-auto mt-2" />
                    )}
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Profile Settings */}
          <Card className="border-stone-200">
            <CardHeader>
              <CardTitle className="font-serif text-lg flex items-center">
                <User className="w-5 h-5 mr-2 text-stone-500" />
                {t('settings.profile') || 'Profile & Identity'}
              </CardTitle>
              <CardDescription>
                Manage your connected accounts and identity
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              
              {/* Read-Only Fields */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="name" className="text-stone-700">Name</Label>
                  <Input 
                    id="name" 
                    value={user?.name || ''} 
                    disabled 
                    className="bg-stone-50 mt-1 cursor-not-allowed text-stone-500"
                  />
                </div>
                <div>
                  <Label htmlFor="email" className="text-stone-700">Email</Label>
                  <Input 
                    id="email" 
                    value={user?.email || ''} 
                    disabled 
                    className="bg-stone-50 mt-1 cursor-not-allowed text-stone-500"
                  />
                </div>
              </div>

              {/* ORCID Integration Section */}
              <div className="pt-4 border-t border-stone-100">
                <Label className="text-stone-900 font-medium mb-2 block">
                  ORCID iD
                </Label>
                
                {hasOrcid ? (
                  // Estado Conectado
                  <div className="flex items-center justify-between p-4 bg-green-50/50 border border-green-200 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="bg-white p-1 rounded-full border border-green-100">
                        <img 
                          src="https://orcid.org/sites/default/files/images/orcid_16x16.png" 
                          alt="ORCID" 
                          className="w-5 h-5" 
                        />
                      </div>
                      <div>
                        <div className="flex items-center space-x-2">
                          <span className="font-medium text-stone-900">Connected</span>
                          <Badge variant="secondary" className="bg-green-100 text-green-800 hover:bg-green-100 border-none">
                            <ShieldCheck className="w-3 h-3 mr-1" />
                            Verified
                          </Badge>
                        </div>
                        <p className="text-sm text-stone-500 mt-0.5">
                          Your research identity is linked to this account.
                        </p>
                      </div>
                    </div>
                  </div>
                ) : (
                  // Estado Desconectado
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between p-4 bg-stone-50 border border-stone-200 rounded-lg gap-4">
                    <div>
                      <div className="flex items-center space-x-2 text-stone-900 font-medium">
                        <img 
                          src="https://orcid.org/sites/default/files/images/orcid_16x16.png" 
                          alt="ORCID" 
                          className="w-4 h-4" 
                        />
                        <span>Not Connected</span>
                      </div>
                      <p className="text-sm text-stone-500 mt-1 max-w-sm">
                        Link your ORCID iD to verify your researcher status and unify your contributions.
                      </p>
                    </div>
                    <Button 
                      onClick={handleConnectOrcid}
                      variant="outline"
                      className="bg-white hover:bg-stone-50 text-stone-700 border-stone-300 shadow-sm shrink-0"
                    >
                      Connect ORCID
                      <ExternalLink className="w-4 h-4 ml-2 text-stone-400" />
                    </Button>
                  </div>
                )}
              </div>

            </CardContent>
          </Card>
        </div>
      </main>

      <Footer />
    </div>
  );
}
