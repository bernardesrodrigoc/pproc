import React, { useState, useEffect } from 'react';
import { Info, X } from 'lucide-react';

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
 * Compact version for inline use in analytics pages
 */
export function VisibilityNotice({ message, className = '' }) {
  if (!message) return null;

  return (
    <div className={`bg-amber-50 border border-amber-200 rounded-lg p-4 ${className}`}>
      <div className="flex items-start space-x-3">
        <Info className="h-5 w-5 text-amber-600 flex-shrink-0 mt-0.5" />
        <div>
          <p className="text-sm text-amber-800 font-medium">Data Collection in Progress</p>
          <p className="text-sm text-amber-700 mt-1">{message}</p>
        </div>
      </div>
    </div>
  );
}
