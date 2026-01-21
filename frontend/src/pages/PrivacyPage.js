import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { useLanguage } from '../i18n/LanguageContext';

export default function PrivacyPage() {
  const { t } = useLanguage();

  return (
    <div className="min-h-screen bg-[#FAFAF9]">
      <Navbar />
      
      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="font-serif text-3xl text-stone-900 mb-8">{t('footer.privacy')}</h1>
        
        <div className="prose prose-stone max-w-none">
          <h2 className="font-serif text-xl text-stone-900 mt-8 mb-4">1. Privacy by Design</h2>
          <p className="text-stone-600 mb-4">
            PubProcess is built with privacy as a core principle. We collect only the minimum data necessary 
            to provide aggregated editorial decision statistics.
          </p>

          <h2 className="font-serif text-xl text-stone-900 mt-8 mb-4">2. Data Collection</h2>
          <p className="text-stone-600 mb-4">
            We collect:
          </p>
          <ul className="list-disc pl-6 text-stone-600 mb-4">
            <li><strong>Account Data:</strong> Email address (for authentication only) and optional ORCID</li>
            <li><strong>Submission Data:</strong> Structured categorical data about editorial decisions (no free text)</li>
            <li><strong>Evidence Files:</strong> Documentary proof of editorial decisions (encrypted, never public)</li>
          </ul>

          <h2 className="font-serif text-xl text-stone-900 mt-8 mb-4">3. Anonymization</h2>
          <p className="text-stone-600 mb-4">
            Your identity is protected through:
          </p>
          <ul className="list-disc pl-6 text-stone-600 mb-4">
            <li>Hashed user IDs that cannot be reverse-engineered</li>
            <li>No storage of IP addresses in plain text</li>
            <li>Minimal logging</li>
            <li>K-anonymity (statistics only displayed when ≥5 similar cases exist)</li>
          </ul>

          <h2 className="font-serif text-xl text-stone-900 mt-8 mb-4">4. Evidence Storage</h2>
          <p className="text-stone-600 mb-4">
            Uploaded evidence files are:
          </p>
          <ul className="list-disc pl-6 text-stone-600 mb-4">
            <li>Encrypted using industry-standard encryption</li>
            <li>Stripped of metadata automatically</li>
            <li>Never made public or shared with third parties</li>
            <li>Used only for internal validation</li>
            <li>Automatically deleted after 12 months (configurable)</li>
          </ul>

          <h2 className="font-serif text-xl text-stone-900 mt-8 mb-4">5. Data Sharing</h2>
          <p className="text-stone-600 mb-4">
            We do NOT share:
          </p>
          <ul className="list-disc pl-6 text-stone-600 mb-4">
            <li>Individual user data with any third party</li>
            <li>Personal information with journals or publishers</li>
            <li>Detailed submission records</li>
          </ul>
          <p className="text-stone-600 mb-4">
            We DO share:
          </p>
          <ul className="list-disc pl-6 text-stone-600 mb-4">
            <li>Aggregated, anonymized statistics via public dashboards</li>
          </ul>

          <h2 className="font-serif text-xl text-stone-900 mt-8 mb-4">6. User Rights</h2>
          <p className="text-stone-600 mb-4">
            You have the right to:
          </p>
          <ul className="list-disc pl-6 text-stone-600 mb-4">
            <li>Request deletion of your account and all associated data</li>
            <li>Export your submission history</li>
            <li>Update your profile information</li>
          </ul>

          <h2 className="font-serif text-xl text-stone-900 mt-8 mb-4">7. Security</h2>
          <p className="text-stone-600 mb-4">
            We implement industry-standard security measures including encrypted data storage, 
            secure authentication, and regular security audits.
          </p>

          <h2 className="font-serif text-xl text-stone-900 mt-8 mb-4">8. Contact</h2>
          <p className="text-stone-600 mb-4">
            For privacy-related inquiries, please contact us through the platform.
          </p>
        </div>
      </main>

      <Footer />
    </div>
  );
}
