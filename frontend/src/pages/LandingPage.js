import React from 'react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../i18n/LanguageContext';
import { useAuth } from '../contexts/AuthContext';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
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
  Layers
} from 'lucide-react';

export default function LandingPage() {
  const { t } = useLanguage();
  const { isAuthenticated } = useAuth();

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
                <Link to={isAuthenticated ? "/submit" : "/login"}>
                  <Button 
                    size="lg" 
                    className="bg-stone-900 text-white hover:bg-stone-800 px-8 py-6 text-base active:scale-95 transition-transform"
                    data-testid="hero-get-started-btn"
                  >
                    {t('landing.getStarted')}
                    <ArrowRight className="ml-2 w-5 h-5" />
                  </Button>
                </Link>
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
            <Link to={isAuthenticated ? "/submit" : "/login"}>
              <Button 
                size="lg" 
                className="bg-white text-stone-900 hover:bg-stone-100 px-8 py-6 text-base"
                data-testid="cta-get-started-btn"
              >
                {t('landing.getStarted')}
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
