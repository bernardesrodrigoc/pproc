import React from 'react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../i18n/LanguageContext';
import { BarChart3 } from 'lucide-react';

export default function Footer() {
  const { t } = useLanguage();

  return (
    <footer className="bg-stone-900 text-stone-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-white rounded-md flex items-center justify-center">
                <BarChart3 className="w-5 h-5 text-stone-900" />
              </div>
              <span className="font-serif text-xl text-white">PubProcess</span>
            </div>
            <p className="text-stone-400 text-sm max-w-md">
              {t('footer.tagline')}
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="text-white font-medium mb-4">Platform</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/analytics" className="text-stone-400 hover:text-white text-sm transition-colors">
                  {t('nav.analytics')}
                </Link>
              </li>
              <li>
                <Link to="/submit" className="text-stone-400 hover:text-white text-sm transition-colors">
                  {t('nav.submit')}
                </Link>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="text-white font-medium mb-4">Legal</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/terms" className="text-stone-400 hover:text-white text-sm transition-colors">
                  {t('footer.terms')}
                </Link>
              </li>
              <li>
                <Link to="/privacy" className="text-stone-400 hover:text-white text-sm transition-colors">
                  {t('footer.privacy')}
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-stone-800 mt-8 pt-8 text-center text-stone-500 text-sm">
          <p>© {new Date().getFullYear()} PubProcess. All rights reserved.</p>
          <p className="mt-2 text-xs">
            This platform does not evaluate scientific merit. It focuses on process statistics only.
          </p>
        </div>
      </div>
    </footer>
  );
}
