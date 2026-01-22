import React, { useState, useEffect } from 'react';
import { useLanguage } from '../i18n/LanguageContext';
import { Info, X, Shield, BarChart3, Lock, CheckCircle } from 'lucide-react';
import { Card, CardContent } from './ui/card';

const API = process.env.REACT_APP_BACKEND_URL + '/api';

/**
 * Reusable banner component for data visibility status
 * Shows a subtle, professional message when public stats are not yet available
 * Automatically hides when public stats are enabled
 */
export default function VisibilityBanner({ className = '' }) {
  const [status, setStatus] = useState(null);
  const [dismissed, setDismissed] = useState(false);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch(`${API}/analytics/visibility-status`);
        if (response.ok) {
          const data = await response.json();
          setStatus(data);
        }
      } catch (error) {
        console.error('Failed to fetch visibility status:', error);
      }
    };

    fetchStatus();
  }, []);

  // Don't show banner if:
  // - Status not loaded yet
  // - Public stats are enabled
  // - User dismissed the banner
  // - No message to show
  if (!status || status.public_stats_enabled || dismissed || !status.message) {
    return null;
  }

  return (
    <div className={`bg-stone-100 border-b border-stone-200 ${className}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between py-3">
          <div className="flex items-center space-x-3">
            <Info className="h-4 w-4 text-stone-500 flex-shrink-0" />
            <p className="text-sm text-stone-600 font-sans">
              {status.message}
            </p>
          </div>
          <button
            onClick={() => setDismissed(true)}
            className="text-stone-400 hover:text-stone-600 transition-colors p-1"
            aria-label="Dismiss"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}

/**
 * Professional data collection panel for when stats are not publicly visible
 * Replaces generic "insufficient data" message with institutional messaging
 */
export function DataCollectionPanel({ className = '' }) {
  const { t } = useLanguage();
  
  // Get array of reasons or use defaults
  const whyList = t('analytics.dataCollectionWhyList') || [
    "Protects contributor identity through aggregation",
    "Ensures statistical robustness of published metrics",
    "Prevents identification of individual submissions"
  ];

  return (
    <Card className={`bg-gradient-to-br from-stone-50 to-stone-100 border-stone-200 ${className}`}>
      <CardContent className="p-6 sm:p-8">
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-stone-200/50 mb-4">
            <BarChart3 className="w-8 h-8 text-stone-600" />
          </div>
          <h3 className="text-xl font-serif text-stone-900 mb-2">
            {t('analytics.dataCollectionTitle') || 'Aggregated Statistics — Data Collection in Progress'}
          </h3>
          <p className="text-stone-600 max-w-2xl mx-auto">
            {t('analytics.dataCollectionMessage') || 
              'To ensure statistical reliability and protect contributor anonymity, public metrics are published only when sufficient independent observations are available.'}
          </p>
        </div>

        {/* Confirmation that submission was recorded */}
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
          <div className="flex items-start space-x-3">
            <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-green-800">
              {t('analytics.dataCollectionNote') || 
                'Your contribution has been recorded and will be included in aggregated analyses once publication thresholds are met.'}
            </p>
          </div>
        </div>

        {/* Why this approach */}
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg p-5 border border-stone-200">
            <div className="flex items-center space-x-2 mb-3">
              <Shield className="w-5 h-5 text-stone-600" />
              <h4 className="font-medium text-stone-900">
                {t('analytics.dataCollectionWhyTitle') || 'Why this approach?'}
              </h4>
            </div>
            <ul className="space-y-2">
              {(Array.isArray(whyList) ? whyList : []).map((reason, index) => (
                <li key={index} className="flex items-start space-x-2 text-sm text-stone-600">
                  <Lock className="w-4 h-4 text-stone-400 flex-shrink-0 mt-0.5" />
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-blue-50 rounded-lg p-5 border border-blue-200">
            <div className="flex items-center space-x-2 mb-3">
              <BarChart3 className="w-5 h-5 text-blue-600" />
              <h4 className="font-medium text-blue-900">Personal Insights</h4>
            </div>
            <p className="text-sm text-blue-800">
              {t('analytics.dataCollectionPersonalNote') || 
                'In the meantime, your Personal Insights dashboard displays analyses based exclusively on your own submissions.'}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

/**
 * Compact version for inline use in analytics pages
 */
export function VisibilityNotice({ message, className = '' }) {
  const { t } = useLanguage();
  
  if (!message) return null;

  return (
    <div className={`bg-amber-50 border border-amber-200 rounded-lg p-4 ${className}`}>
      <div className="flex items-start space-x-3">
        <Info className="h-5 w-5 text-amber-600 flex-shrink-0 mt-0.5" />
        <div>
          <p className="text-sm text-amber-800 font-medium">
            {t('analytics.insufficientData') || 'Data collection in progress'}
          </p>
          <p className="text-sm text-amber-700 mt-1">{message}</p>
        </div>
      </div>
    </div>
  );
}
