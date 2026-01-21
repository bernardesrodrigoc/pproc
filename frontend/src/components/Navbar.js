import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage, LANGUAGES } from '../i18n/LanguageContext';
import { Button } from './ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator
} from './ui/dropdown-menu';
import { 
  BarChart3, 
  Menu, 
  X, 
  User, 
  LogOut, 
  Settings, 
  Globe,
  FileText,
  LayoutDashboard,
  ChevronDown
} from 'lucide-react';

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const { t, language, setLanguage } = useLanguage();
  const location = useLocation();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const isActive = (path) => location.pathname === path;

  const navLinks = [
    { path: '/analytics', label: t('nav.analytics'), icon: BarChart3 },
  ];

  const authLinks = [
    { path: '/dashboard', label: t('nav.dashboard'), icon: LayoutDashboard },
    { path: '/submit', label: t('nav.submit'), icon: FileText },
  ];

  return (
    <nav className="sticky top-0 z-50 glass border-b border-stone-200/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <div className="w-8 h-8 bg-stone-900 rounded-md flex items-center justify-center group-hover:bg-stone-800 transition-colors">
              <BarChart3 className="w-5 h-5 text-white" />
            </div>
            <span className="font-serif text-xl text-stone-900 hidden sm:block">
              PubProcess
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navLinks.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors flex items-center space-x-2
                  ${isActive(path) 
                    ? 'bg-stone-100 text-stone-900' 
                    : 'text-stone-600 hover:text-stone-900 hover:bg-stone-50'
                  }`}
              >
                <Icon className="w-4 h-4" />
                <span>{label}</span>
              </Link>
            ))}

            {isAuthenticated && authLinks.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors flex items-center space-x-2
                  ${isActive(path) 
                    ? 'bg-stone-100 text-stone-900' 
                    : 'text-stone-600 hover:text-stone-900 hover:bg-stone-50'
                  }`}
              >
                <Icon className="w-4 h-4" />
                <span>{label}</span>
              </Link>
            ))}
          </div>

          {/* Right side */}
          <div className="hidden md:flex items-center space-x-3">
            {/* Language Selector */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="sm" className="flex items-center space-x-1" data-testid="language-selector">
                  <Globe className="w-4 h-4" />
                  <span className="text-sm">{LANGUAGES.find(l => l.code === language)?.flag}</span>
                  <ChevronDown className="w-3 h-3" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-40">
                {LANGUAGES.map((lang) => (
                  <DropdownMenuItem
                    key={lang.code}
                    onClick={() => setLanguage(lang.code)}
                    className={language === lang.code ? 'bg-stone-100' : ''}
                    data-testid={`lang-${lang.code}`}
                  >
                    <span className="mr-2">{lang.flag}</span>
                    {lang.name}
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>

            {isAuthenticated ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="flex items-center space-x-2" data-testid="user-menu">
                    {user?.picture ? (
                      <img src={user.picture} alt="" className="w-7 h-7 rounded-full" />
                    ) : (
                      <User className="w-5 h-5" />
                    )}
                    <span className="text-sm max-w-[100px] truncate">{user?.name}</span>
                    <ChevronDown className="w-3 h-3" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-48">
                  <DropdownMenuItem onClick={() => navigate('/dashboard')} data-testid="menu-dashboard">
                    <LayoutDashboard className="w-4 h-4 mr-2" />
                    {t('nav.dashboard')}
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => navigate('/settings')} data-testid="menu-settings">
                    <Settings className="w-4 h-4 mr-2" />
                    {t('nav.settings')}
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={logout} className="text-red-600" data-testid="menu-logout">
                    <LogOut className="w-4 h-4 mr-2" />
                    {t('nav.logout')}
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : (
              <Button 
                onClick={() => navigate('/login')} 
                className="bg-stone-900 text-white hover:bg-stone-800"
                data-testid="login-btn"
              >
                {t('nav.login')}
              </Button>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden p-2 rounded-md text-stone-600 hover:text-stone-900 hover:bg-stone-100"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            data-testid="mobile-menu-btn"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-stone-200">
            <div className="space-y-1">
              {navLinks.map(({ path, label, icon: Icon }) => (
                <Link
                  key={path}
                  to={path}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`block px-4 py-3 rounded-md text-sm font-medium transition-colors flex items-center space-x-2
                    ${isActive(path) 
                      ? 'bg-stone-100 text-stone-900' 
                      : 'text-stone-600 hover:text-stone-900 hover:bg-stone-50'
                    }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{label}</span>
                </Link>
              ))}

              {isAuthenticated && (
                <>
                  {authLinks.map(({ path, label, icon: Icon }) => (
                    <Link
                      key={path}
                      to={path}
                      onClick={() => setMobileMenuOpen(false)}
                      className={`block px-4 py-3 rounded-md text-sm font-medium transition-colors flex items-center space-x-2
                        ${isActive(path) 
                          ? 'bg-stone-100 text-stone-900' 
                          : 'text-stone-600 hover:text-stone-900 hover:bg-stone-50'
                        }`}
                    >
                      <Icon className="w-4 h-4" />
                      <span>{label}</span>
                    </Link>
                  ))}
                  <button
                    onClick={() => { logout(); setMobileMenuOpen(false); }}
                    className="w-full text-left px-4 py-3 rounded-md text-sm font-medium text-red-600 hover:bg-red-50 flex items-center space-x-2"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>{t('nav.logout')}</span>
                  </button>
                </>
              )}

              {!isAuthenticated && (
                <Button 
                  onClick={() => { navigate('/login'); setMobileMenuOpen(false); }}
                  className="w-full mt-4 bg-stone-900 text-white hover:bg-stone-800"
                >
                  {t('nav.login')}
                </Button>
              )}

              {/* Mobile Language Selector */}
              <div className="px-4 py-3 border-t border-stone-200 mt-4">
                <p className="text-xs text-stone-500 mb-2">{t('settings.language')}</p>
                <div className="flex space-x-2">
                  {LANGUAGES.map((lang) => (
                    <button
                      key={lang.code}
                      onClick={() => setLanguage(lang.code)}
                      className={`px-3 py-1.5 rounded-md text-sm ${
                        language === lang.code 
                          ? 'bg-stone-900 text-white' 
                          : 'bg-stone-100 text-stone-600'
                      }`}
                    >
                      {lang.flag} {lang.name}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
