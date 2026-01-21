import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../i18n/LanguageContext';
import { useAuth } from '../contexts/AuthContext';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Progress } from '../components/ui/progress';
import { 
  FileText, 
  Plus, 
  Clock, 
  CheckCircle2, 
  AlertCircle,
  TrendingUp,
  Award,
  Loader2
} from 'lucide-react';

const API = process.env.REACT_APP_BACKEND_URL + '/api';

export default function DashboardPage() {
  const { t } = useLanguage();
  const { user, trustScoreVisible } = useAuth();
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSubmissions = async () => {
      try {
        const response = await fetch(`${API}/submissions/my`, {
          credentials: 'include'
        });
        if (response.ok) {
          const data = await response.json();
          setSubmissions(data);
        }
      } catch (error) {
        console.error('Failed to fetch submissions:', error);
      }
      setLoading(false);
    };

    fetchSubmissions();
  }, []);

  const getStatusBadge = (status) => {
    switch (status) {
      case 'validated':
        return (
          <Badge className="bg-emerald-100 text-emerald-800 hover:bg-emerald-100">
            <CheckCircle2 className="w-3 h-3 mr-1" />
            {t('dashboard.status.validated')}
          </Badge>
        );
      case 'flagged':
        return (
          <Badge className="bg-amber-100 text-amber-800 hover:bg-amber-100">
            <AlertCircle className="w-3 h-3 mr-1" />
            {t('dashboard.status.flagged')}
          </Badge>
        );
      default:
        return (
          <Badge className="bg-stone-100 text-stone-800 hover:bg-stone-100">
            <Clock className="w-3 h-3 mr-1" />
            {t('dashboard.status.pending')}
          </Badge>
        );
    }
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString(undefined, { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const getDecisionLabel = (type) => {
    const labels = {
      desk_reject: 'Desk Reject',
      reject_after_review: 'Reject After Review',
      major_revision: 'Major Revision',
      minor_revision: 'Minor Revision'
    };
    return labels[type] || type;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#FAFAF9]">
        <Navbar />
        <div className="flex items-center justify-center h-[calc(100vh-64px)]">
          <Loader2 className="w-8 h-8 animate-spin text-stone-600" />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#FAFAF9]">
      <Navbar />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12" data-testid="user-dashboard">
        {/* Header */}
        <div className="mb-8">
          <h1 className="font-serif text-3xl md:text-4xl text-stone-900 mb-2">
            {t('dashboard.title')}
          </h1>
          <p className="text-stone-600">
            {t('dashboard.welcomeBack')}, {user?.name}
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Trust Score - Only show if visible */}
          {trustScoreVisible ? (
            <Card className="border-stone-200">
              <CardContent className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <p className="text-sm text-stone-500 mb-1">{t('dashboard.trustScore')}</p>
                    <p className="font-serif text-4xl text-stone-900">
                      {user?.trust_score?.toFixed(0) || 0}
                    </p>
                  </div>
                  <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                    <Award className="w-5 h-5 text-orange-700" />
                  </div>
                </div>
                <Progress value={user?.trust_score || 0} className="h-2 mb-2" />
                <p className="text-xs text-stone-500">Based on validated, consistent submissions. Higher scores increase the statistical weight of your contributions.</p>
              </CardContent>
            </Card>
          ) : (
            <Card className="border-stone-200 bg-stone-50">
              <CardContent className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <p className="text-sm text-stone-500 mb-1">{t('dashboard.trustScore')}</p>
                    <p className="font-serif text-2xl text-stone-400">
                      Not yet visible
                    </p>
                  </div>
                  <div className="w-10 h-10 bg-stone-100 rounded-lg flex items-center justify-center">
                    <Award className="w-5 h-5 text-stone-400" />
                  </div>
                </div>
                <p className="text-xs text-stone-500">Your trust score will be visible after 2 validated submissions, or 1 validated submission with evidence.</p>
              </CardContent>
            </Card>
          )}

          {/* Contributions */}
          <Card className="border-stone-200">
            <CardContent className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <p className="text-sm text-stone-500 mb-1">{t('dashboard.contributions')}</p>
                  <p className="font-serif text-4xl text-stone-900">
                    {user?.contribution_count || 0}
                  </p>
                </div>
                <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-5 h-5 text-emerald-700" />
                </div>
              </div>
              <p className="text-sm text-stone-600">
                {user?.validated_count || 0} validated • {user?.flagged_count || 0} flagged
              </p>
            </CardContent>
          </Card>

          {/* Quick Action */}
          <Card className="border-stone-200 bg-stone-900 text-white">
            <CardContent className="p-6 flex flex-col justify-between h-full">
              <div>
                <p className="text-stone-300 text-sm mb-2">Ready to contribute?</p>
                <p className="text-xl font-medium mb-4">Submit a new case</p>
              </div>
              <Link to="/submit">
                <Button 
                  variant="secondary" 
                  className="w-full bg-white text-stone-900 hover:bg-stone-100"
                  data-testid="submit-case-btn"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  {t('nav.submit')}
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>

        {/* Submissions List */}
        <Card className="border-stone-200">
          <CardHeader>
            <CardTitle className="font-serif text-xl">{t('dashboard.mySubmissions')}</CardTitle>
            <CardDescription>{t('dashboard.recentActivity')}</CardDescription>
          </CardHeader>
          <CardContent>
            {submissions.length === 0 ? (
              <div className="text-center py-12">
                <FileText className="w-12 h-12 text-stone-300 mx-auto mb-4" />
                <p className="text-stone-600 mb-4">{t('dashboard.noSubmissions')}</p>
                <Link to="/submit">
                  <Button 
                    className="bg-stone-900 text-white hover:bg-stone-800"
                    data-testid="first-submission-btn"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    {t('dashboard.startSubmitting')}
                  </Button>
                </Link>
              </div>
            ) : (
              <div className="space-y-4">
                {submissions.map((submission) => (
                  <div 
                    key={submission.submission_id}
                    className="flex items-center justify-between p-4 bg-stone-50 rounded-lg hover:bg-stone-100 transition-colors"
                    data-testid={`submission-${submission.submission_id}`}
                  >
                    <div className="flex items-center space-x-4">
                      <div className="w-10 h-10 bg-white rounded-lg border border-stone-200 flex items-center justify-center">
                        <FileText className="w-5 h-5 text-stone-600" />
                      </div>
                      <div>
                        <p className="font-medium text-stone-900">{submission.journal_name}</p>
                        <p className="text-sm text-stone-500">{submission.publisher_name}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <p className="text-sm font-medium text-stone-700">
                          {getDecisionLabel(submission.decision_type)}
                        </p>
                        <p className="text-xs text-stone-500">
                          {formatDate(submission.created_at)}
                        </p>
                      </div>
                      {getStatusBadge(submission.status)}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </main>

      <Footer />
    </div>
  );
}
