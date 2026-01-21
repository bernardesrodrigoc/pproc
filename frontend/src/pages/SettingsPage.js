import React, { useState } from 'react';
import { useLanguage, LANGUAGES } from '../i18n/LanguageContext';
import { useAuth } from '../contexts/AuthContext';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { toast } from 'sonner';
import { Globe, User, Check, Loader2 } from 'lucide-react';

export default function SettingsPage() {
  const { t, language, setLanguage } = useLanguage();
  const { user, updateProfile } = useAuth();
  const [orcid, setOrcid] = useState(user?.orcid || '');
  const [saving, setSaving] = useState(false);

  const handleSaveProfile = async () => {
    setSaving(true);
    try {
      await updateProfile({ orcid });
      toast.success(t('settings.saved'));
    } catch (error) {
      toast.error(t('common.error'));
    }
    setSaving(false);
  };

  return (
    <div className="min-h-screen bg-[#FAFAF9]">
      <Navbar />
      
      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12" data-testid="settings-page">
        <div className="mb-8">
          <h1 className="font-serif text-3xl text-stone-900 mb-2">
            {t('settings.title')}
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
                {t('settings.profile')}
              </CardTitle>
              <CardDescription>
                Update your profile information
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="email" className="text-stone-700">Email</Label>
                <Input 
                  id="email" 
                  value={user?.email || ''} 
                  disabled 
                  className="bg-stone-50 mt-1"
                />
              </div>
              <div>
                <Label htmlFor="name" className="text-stone-700">Name</Label>
                <Input 
                  id="name" 
                  value={user?.name || ''} 
                  disabled 
                  className="bg-stone-50 mt-1"
                />
              </div>
              <div>
                <Label htmlFor="orcid" className="text-stone-700">{t('settings.orcid')}</Label>
                <Input 
                  id="orcid" 
                  value={orcid} 
                  onChange={(e) => setOrcid(e.target.value)}
                  placeholder="0000-0000-0000-0000"
                  className="mt-1"
                  data-testid="orcid-input"
                />
                <p className="text-xs text-stone-500 mt-1">
                  Your ORCID helps link your contributions to your research identity
                </p>
              </div>
              <Button 
                onClick={handleSaveProfile}
                disabled={saving}
                className="bg-stone-900 text-white hover:bg-stone-800"
                data-testid="save-profile-btn"
              >
                {saving ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Saving...
                  </>
                ) : (
                  t('settings.updateProfile')
                )}
              </Button>
            </CardContent>
          </Card>
        </div>
      </main>

      <Footer />
    </div>
  );
}
