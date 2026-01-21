import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { useLanguage } from '../i18n/LanguageContext';

export default function TermsPage() {
  const { t } = useLanguage();

  return (
    <div className="min-h-screen bg-[#FAFAF9]">
      <Navbar />
      
      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="font-serif text-3xl text-stone-900 mb-8">{t('footer.terms')}</h1>
        
        <div className="prose prose-stone max-w-none">
          <h2 className="font-serif text-xl text-stone-900 mt-8 mb-4">1. Purpose</h2>
          <p className="text-stone-600 mb-4">
            PubProcess is a platform designed to aggregate editorial decision statistics from scientific journals. 
            Our focus is on process transparency, not individual complaints. We do not evaluate scientific merit.
          </p>

          <h2 className="font-serif text-xl text-stone-900 mt-8 mb-4">2. User Responsibilities</h2>
          <p className="text-stone-600 mb-4">
            By using this platform, you agree to:
          </p>
          <ul className="list-disc pl-6 text-stone-600 mb-4">
            <li>Submit only accurate and truthful information about editorial decisions you have personally received</li>
            <li>Provide authentic documentary evidence when requested</li>
            <li>Not submit false, misleading, or fabricated data</li>
            <li>Not attempt to manipulate statistics or game the system</li>
            <li>Respect the anonymity and privacy of all users</li>
          </ul>

          <h2 className="font-serif text-xl text-stone-900 mt-8 mb-4">3. Data Usage</h2>
          <p className="text-stone-600 mb-4">
            All submitted data is processed into aggregated statistics. Individual cases are never displayed publicly. 
            We implement k-anonymity (minimum 5 cases) to protect user privacy.
          </p>

          <h2 className="font-serif text-xl text-stone-900 mt-8 mb-4">4. Evidence Handling</h2>
          <p className="text-stone-600 mb-4">
            Documentary evidence uploaded to the platform:
          </p>
          <ul className="list-disc pl-6 text-stone-600 mb-4">
            <li>Is encrypted and stored securely</li>
            <li>Is never made public</li>
            <li>Is used only for internal validation purposes</li>
            <li>Is automatically deleted after the retention period (default: 12 months)</li>
          </ul>

          <h2 className="font-serif text-xl text-stone-900 mt-8 mb-4">5. Disclaimer</h2>
          <p className="text-stone-600 mb-4">
            PubProcess provides statistics for informational purposes only. We do not:
          </p>
          <ul className="list-disc pl-6 text-stone-600 mb-4">
            <li>Evaluate the scientific merit of manuscripts</li>
            <li>Make accusations against journals, editors, or publishers</li>
            <li>Host complaints or personal opinions</li>
            <li>Guarantee the accuracy of user-submitted data</li>
          </ul>

          <h2 className="font-serif text-xl text-stone-900 mt-8 mb-4">6. Modifications</h2>
          <p className="text-stone-600 mb-4">
            We reserve the right to modify these terms at any time. Continued use of the platform constitutes 
            acceptance of any modifications.
          </p>
        </div>
      </main>

      <Footer />
    </div>
  );
}
