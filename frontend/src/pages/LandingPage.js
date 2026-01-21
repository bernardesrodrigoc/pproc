import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useLanguage } from '../i18n/LanguageContext';
import { useAuth } from '../contexts/AuthContext';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '../components/ui/dialog';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { toast } from 'sonner';
import { 
  Shield, 
  Lock, 
  BarChart3, 
  Users, 
  FileText,
  ArrowRight,
  CheckCircle2,
  Eye,
  Database,
  Layers,
  Loader2
} from 'lucide-react';

export default function LandingPage() {
  const { t } = useLanguage();
  const { isAuthenticated, loginWithGoogle, loginWithOrcid } = useAuth();
  const navigate = useNavigate();
  
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [showOrcidForm, setShowOrcidForm] = useState(false);
  const [orcidId, setOrcidId] = useState('');
  const [orcidName, setOrcidName] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGetStarted = () => {
    if (isAuthenticated) {
      navigate('/submit');
    } else {
      setShowAuthModal(true);
    }
  };

  const handleOrcidLogin = async (e) => {
    e.preventDefault();
    
    const orcidRegex = /^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$/;
    if (!orcidRegex.test(orcidId)) {
      toast.error('Please enter a valid ORCID ID (format: 0000-0000-0000-0000)');
      return;
    }
    
    setLoading(true);
    try {
      await loginWithOrcid(orcidId, orcidName);
      setShowAuthModal(false);
      navigate('/submit');
    } catch (error) {
      toast.error('Authentication failed. Please try again.');
    }
    setLoading(false);
  };

  const features = [
    { icon: Shield, label: t('landing.feature1'), color: 'text-emerald-600' },
    { icon: Lock, label: t('landing.feature2'), color: 'text-blue-600' },
    { icon: Users, label: t('landing.feature3'), color: 'text-purple-600' },
    { icon: Layers, label: t('landing.feature4'), color: 'text-orange-600' },
    { icon: BarChart3, label: t('landing.feature5'), color: 'text-rose-600' },
    { icon: Database, label: t('landing.feature6'), color: 'text-teal-600' },
  ];

  const steps = [
    { 
      number: '01', 
      title: t('landing.step1Title'), 
      desc: t('landing.step1Desc'),
      icon: FileText
    },
    { 
      number: '02', 
      title: t('landing.step2Title'), 
      desc: t('landing.step2Desc'),
      icon: Database
    },
    { 
      number: '03', 
      title: t('landing.step3Title'), 
      desc: t('landing.step3Desc'),
      icon: Eye
    },
  ];

  return (
    <div className="min-h-screen bg-[#FAFAF9]">
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-24 items-center">
            <div className="opacity-0 animate-fade-in-up">
              <p className="text-xs font-bold uppercase tracking-widest text-orange-700 mb-4">
                {t('landing.trustedBy')}
              </p>
              <h1 className="font-serif text-5xl md:text-6xl tracking-tight text-stone-900 leading-[1.1] mb-6">
                {t('landing.heroTitle')}
              </h1>
              <p className="text-lg text-stone-600 leading-relaxed mb-8 max-w-lg">
                {t('landing.heroSubtitle')}
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Button 
                  size="lg" 
                  className="bg-stone-900 text-white hover:bg-stone-800 px-8 py-6 text-base active:scale-95 transition-transform"
                  onClick={handleGetStarted}
                  data-testid="hero-get-started-btn"
                >
                  {t('landing.getStarted')}
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Button>
                <Link to="/analytics">
                  <Button 
                    variant="outline" 
                    size="lg"
                    className="border-stone-200 hover:bg-stone-50 px-8 py-6 text-base"
                    data-testid="hero-explore-btn"
                  >
                    {t('landing.exploreData')}
                  </Button>
                </Link>
              </div>
            </div>
            
            <div className="relative opacity-0 animate-fade-in-up animate-delay-200">
              <div className="aspect-[4/3] rounded-xl overflow-hidden shadow-2xl">
                <img 
                  src="https://images.pexels.com/photos/6333724/pexels-photo-6333724.jpeg"
                  alt="Research transparency"
                  className="w-full h-full object-cover"
                />
              </div>
              {/* Floating stats card */}
              <div className="absolute -bottom-6 -left-6 bg-white rounded-lg shadow-xl p-4 border border-stone-100">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-emerald-100 rounded-full flex items-center justify-center">
                    <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-serif text-stone-900">500+</p>
                    <p className="text-xs text-stone-500">Cases Analyzed</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-white border-y border-stone-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">
          <div className="text-center mb-16">
            <h2 className="font-serif text-3xl md:text-4xl tracking-tight text-stone-900 mb-4">
              {t('landing.howItWorks')}
            </h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12">
            {steps.map((step, index) => (
              <div 
                key={step.number} 
                className={`opacity-0 animate-fade-in-up animate-delay-${(index + 1) * 100}`}
              >
                <div className="relative">
                  <span className="text-7xl font-serif text-stone-100 absolute -top-4 -left-2">
                    {step.number}
                  </span>
                  <div className="relative z-10 pt-8">
                    <div className="w-12 h-12 bg-stone-900 rounded-lg flex items-center justify-center mb-4">
                      <step.icon className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="font-sans text-xl font-medium text-stone-800 mb-2">
                      {step.title}
                    </h3>
                    <p className="text-stone-600 leading-relaxed">
                      {step.desc}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Privacy Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <img 
            src="https://images.pexels.com/photos/33986857/pexels-photo-33986857.jpeg"
            alt=""
            className="w-full h-full object-cover"
          />
        </div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">
          <div className="max-w-3xl mx-auto text-center">
            <div className="w-16 h-16 bg-stone-900 rounded-2xl flex items-center justify-center mx-auto mb-8">
              <Shield className="w-8 h-8 text-white" />
            </div>
            <h2 className="font-serif text-3xl md:text-4xl tracking-tight text-stone-900 mb-6">
              {t('landing.privacyTitle')}
            </h2>
            <p className="text-lg text-stone-600 leading-relaxed">
              {t('landing.privacyDesc')}
            </p>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="bg-white border-t border-stone-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">
          <div className="text-center mb-16">
            <h2 className="font-serif text-3xl md:text-4xl tracking-tight text-stone-900">
              {t('landing.featuresTitle')}
            </h2>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <Card 
                key={index} 
                className="border-stone-200 hover:shadow-lg transition-shadow cursor-default"
              >
                <CardContent className="p-6 flex flex-col items-center text-center">
                  <div className={`w-12 h-12 rounded-xl bg-stone-50 flex items-center justify-center mb-4 ${feature.color}`}>
                    <feature.icon className="w-6 h-6" />
                  </div>
                  <p className="font-medium text-stone-800">{feature.label}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-stone-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h2 className="font-serif text-3xl md:text-4xl tracking-tight text-white mb-6">
              Ready to contribute?
            </h2>
            <p className="text-stone-400 text-lg mb-8 max-w-2xl mx-auto">
              Join researchers worldwide in building transparency in scientific publishing.
            </p>
            <Button 
              size="lg" 
              className="bg-white text-stone-900 hover:bg-stone-100 px-8 py-6 text-base"
              onClick={handleGetStarted}
              data-testid="cta-get-started-btn"
            >
              {t('landing.getStarted')}
              <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
          </div>
        </div>
      </section>

      <Footer />

      {/* Auth Modal */}
      <Dialog open={showAuthModal} onOpenChange={setShowAuthModal}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="font-serif text-xl">Sign in to continue</DialogTitle>
            <DialogDescription>
              Choose your preferred authentication method
            </DialogDescription>
          </DialogHeader>
          
          {!showOrcidForm ? (
            <div className="space-y-4 pt-4">
              {/* Google OAuth Button */}
              <Button 
                onClick={() => {
                  setShowAuthModal(false);
                  loginWithGoogle();
                }}
                className="w-full bg-stone-900 text-white hover:bg-stone-800 py-6 text-base flex items-center justify-center space-x-3"
                data-testid="modal-google-btn"
              >
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
                <span>Continue with Google</span>
              </Button>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t border-stone-200" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-white px-2 text-stone-500">or</span>
                </div>
              </div>

              {/* ORCID Button */}
              <Button 
                onClick={() => setShowOrcidForm(true)}
                variant="outline"
                className="w-full py-6 text-base flex items-center justify-center space-x-3 border-[#A6CE39] text-[#A6CE39] hover:bg-[#A6CE39]/10"
                data-testid="modal-orcid-btn"
              >
                <svg className="w-5 h-5" viewBox="0 0 256 256" fill="currentColor">
                  <path d="M128 0C57.3 0 0 57.3 0 128s57.3 128 128 128 128-57.3 128-128S198.7 0 128 0zM82.8 200.8h-24V91.2h24v109.6zm-12-124.4c-7.7 0-14-6.3-14-14s6.3-14 14-14 14 6.3 14 14-6.3 14-14 14zm130.4 124.4h-24v-54.8c0-13.8-.3-31.6-19.2-31.6-19.3 0-22.2 15-22.2 30.6v55.8h-24V91.2h23v15h.3c3.2-6 11-12.3 22.6-12.3 24.2 0 28.7 16 28.7 36.6v70.3h-.2z"/>
                </svg>
                <span>Continue with ORCID</span>
              </Button>

              <p className="text-xs text-stone-500 text-center mt-4">
                <Lock className="w-3 h-3 inline mr-1" />
                Authentication is used only to prevent spam. All contributions remain anonymous.
              </p>
            </div>
          ) : (
            <form onSubmit={handleOrcidLogin} className="space-y-4 pt-4">
              <Button 
                type="button"
                variant="ghost" 
                size="sm" 
                onClick={() => setShowOrcidForm(false)}
                className="-ml-2"
              >
                ← Back to options
              </Button>
              
              <div>
                <Label htmlFor="modal-orcid" className="text-stone-700">ORCID ID *</Label>
                <Input 
                  id="modal-orcid"
                  value={orcidId}
                  onChange={(e) => setOrcidId(e.target.value)}
                  placeholder="0000-0000-0000-0000"
                  className="mt-1"
                  required
                />
                <p className="text-xs text-stone-500 mt-1">Format: 0000-0000-0000-0000</p>
              </div>
              
              <div>
                <Label htmlFor="modal-name" className="text-stone-700">Display Name (optional)</Label>
                <Input 
                  id="modal-name"
                  value={orcidName}
                  onChange={(e) => setOrcidName(e.target.value)}
                  placeholder="Your name"
                  className="mt-1"
                />
              </div>
              
              <Button 
                type="submit"
                disabled={loading}
                className="w-full bg-[#A6CE39] text-white hover:bg-[#8AB82E] py-6 text-base"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Signing in...
                  </>
                ) : (
                  'Continue with ORCID'
                )}
              </Button>
            </form>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
