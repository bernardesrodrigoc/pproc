import React, { useState, useEffect } from 'react';
import { useLanguage } from '../i18n/LanguageContext';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import VisibilityBanner, { VisibilityNotice } from '../components/VisibilityBanner';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Badge } from '../components/ui/badge';
import { Progress } from '../components/ui/progress';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend
} from 'recharts';
import { 
  BarChart3, 
  Building2, 
  BookOpen, 
  Microscope,
  Info,
  AlertCircle,
  Loader2,
  TrendingUp,
  TrendingDown,
  Minus
} from 'lucide-react';

const API = process.env.REACT_APP_BACKEND_URL + '/api';

const CHART_COLORS = ['#c2410c', '#ea580c', '#fb923c', '#fdba74', '#ffedd5'];

export default function AnalyticsPage() {
  const { t } = useLanguage();
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);
  const [selectedPublisher, setSelectedPublisher] = useState('all');
  const [visibilityStatus, setVisibilityStatus] = useState(null);
  
  const [overview, setOverview] = useState(null);
  const [publishers, setPublishers] = useState([]);
  const [publisherAnalytics, setPublisherAnalytics] = useState([]);
  const [journalAnalytics, setJournalAnalytics] = useState([]);
  const [areaAnalytics, setAreaAnalytics] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [overviewRes, publishersRes, pubAnalytics, journalAnalytics, areaAnalytics, visibilityRes] = await Promise.all([
          fetch(`${API}/analytics/overview`).then(r => r.json()),
          fetch(`${API}/publishers`).then(r => r.json()),
          fetch(`${API}/analytics/publishers`).then(r => r.json()),
          fetch(`${API}/analytics/journals`).then(r => r.json()),
          fetch(`${API}/analytics/areas`).then(r => r.json()),
          fetch(`${API}/analytics/visibility-status`).then(r => r.json())
        ]);
        
        setOverview(overviewRes);
        setPublishers(publishersRes);
        setPublisherAnalytics(pubAnalytics);
        setJournalAnalytics(journalAnalytics);
        setAreaAnalytics(areaAnalytics);
        setVisibilityStatus(visibilityRes);
      } catch (error) {
        console.error('Failed to fetch analytics:', error);
      }
      setLoading(false);
    };

    fetchData();
  }, []);

  // Filter journals by publisher
  const filteredJournals = selectedPublisher === 'all' 
    ? journalAnalytics 
    : journalAnalytics.filter(j => j.publisher_id === selectedPublisher);

  const getScoreClass = (score) => {
    if (score >= 70) return 'bg-emerald-100 text-emerald-800';
    if (score >= 40) return 'bg-amber-100 text-amber-800';
    return 'bg-red-100 text-red-800';
  };

  const getScoreIcon = (score) => {
    if (score >= 70) return <TrendingUp className="w-4 h-4" />;
    if (score >= 40) return <Minus className="w-4 h-4" />;
    return <TrendingDown className="w-4 h-4" />;
  };

  const ScoreCard = ({ label, description, score }) => (
    <div className="bg-white border border-stone-200 rounded-lg p-4">
      <div className="flex items-start justify-between mb-2">
        <div>
          <p className="text-sm font-medium text-stone-700">{label}</p>
          <p className="text-xs text-stone-500 mt-1">{description}</p>
        </div>
        <Badge className={getScoreClass(score)}>
          {getScoreIcon(score)}
          <span className="ml-1">{score.toFixed(0)}</span>
        </Badge>
      </div>
      <Progress value={score} className="h-2" />
    </div>
  );

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

  // Prepare chart data
  const decisionChartData = overview?.decision_distribution 
    ? Object.entries(overview.decision_distribution).map(([key, value]) => ({
        name: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
        value
      }))
    : [];

  const reviewerChartData = overview?.reviewer_distribution
    ? Object.entries(overview.reviewer_distribution).map(([key, value]) => ({
        name: key === '0' ? 'No Reviewers' : key === '1' ? '1 Reviewer' : '2+ Reviewers',
        value
      }))
    : [];

  return (
    <div className="min-h-screen bg-[#FAFAF9]">
      <Navbar />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12" data-testid="analytics-dashboard">
        {/* Header */}
        <div className="mb-8">
          <h1 className="font-serif text-3xl md:text-4xl text-stone-900 mb-2">
            {t('analytics.title')}
          </h1>
          <p className="text-stone-600">
            {t('analytics.subtitle')}
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="border-stone-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-stone-500 mb-1">{t('analytics.totalSubmissions')}</p>
                  <p className="font-serif text-4xl text-stone-900">
                    {overview?.total_submissions || 0}
                  </p>
                </div>
                <div className="w-12 h-12 bg-stone-100 rounded-xl flex items-center justify-center">
                  <BarChart3 className="w-6 h-6 text-stone-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-stone-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-stone-500 mb-1">{t('analytics.avgTransparency')}</p>
                  <p className="font-serif text-4xl text-stone-900">
                    {publisherAnalytics.length > 0 
                      ? (publisherAnalytics.reduce((acc, p) => acc + p.transparency_score, 0) / publisherAnalytics.length).toFixed(0)
                      : '--'}
                  </p>
                </div>
                <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-emerald-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-stone-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-stone-500 mb-1">{t('analytics.avgReviewDepth')}</p>
                  <p className="font-serif text-4xl text-stone-900">
                    {publisherAnalytics.length > 0 
                      ? (publisherAnalytics.reduce((acc, p) => acc + p.review_depth_score, 0) / publisherAnalytics.length).toFixed(0)
                      : '--'}
                  </p>
                </div>
                <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                  <BookOpen className="w-6 h-6 text-blue-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="bg-white border border-stone-200 p-1">
            <TabsTrigger value="overview" className="data-[state=active]:bg-stone-900 data-[state=active]:text-white">
              <BarChart3 className="w-4 h-4 mr-2" />
              {t('analytics.overview')}
            </TabsTrigger>
            <TabsTrigger value="publishers" className="data-[state=active]:bg-stone-900 data-[state=active]:text-white">
              <Building2 className="w-4 h-4 mr-2" />
              {t('analytics.publishers')}
            </TabsTrigger>
            <TabsTrigger value="journals" className="data-[state=active]:bg-stone-900 data-[state=active]:text-white">
              <BookOpen className="w-4 h-4 mr-2" />
              {t('analytics.journals')}
            </TabsTrigger>
            <TabsTrigger value="areas" className="data-[state=active]:bg-stone-900 data-[state=active]:text-white">
              <Microscope className="w-4 h-4 mr-2" />
              {t('analytics.areas')}
            </TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6" data-testid="overview-tab">
            {!overview?.sufficient_data ? (
              <Card className="border-stone-200">
                <CardContent className="p-12 text-center">
                  <AlertCircle className="w-12 h-12 text-amber-500 mx-auto mb-4" />
                  <p className="text-stone-600">{t('analytics.insufficientData')}</p>
                </CardContent>
              </Card>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Decision Distribution */}
                <Card className="border-stone-200">
                  <CardHeader>
                    <CardTitle className="font-serif text-lg">Decision Distribution</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={decisionChartData}
                            cx="50%"
                            cy="50%"
                            innerRadius={60}
                            outerRadius={80}
                            paddingAngle={5}
                            dataKey="value"
                            label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                          >
                            {decisionChartData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                            ))}
                          </Pie>
                          <Tooltip />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </CardContent>
                </Card>

                {/* Reviewer Distribution */}
                <Card className="border-stone-200">
                  <CardHeader>
                    <CardTitle className="font-serif text-lg">Reviewer Distribution</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={reviewerChartData}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#e7e5e4" />
                          <XAxis dataKey="name" tick={{ fill: '#57534e', fontSize: 12 }} />
                          <YAxis tick={{ fill: '#57534e', fontSize: 12 }} />
                          <Tooltip />
                          <Bar dataKey="value" fill="#c2410c" radius={[4, 4, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </CardContent>
                </Card>

                {/* Score Explanations */}
                <Card className="border-stone-200 lg:col-span-2">
                  <CardHeader>
                    <CardTitle className="font-serif text-lg flex items-center">
                      <Info className="w-5 h-5 mr-2 text-stone-500" />
                      Understanding the Scores
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="p-4 bg-stone-50 rounded-lg">
                        <h4 className="font-medium text-stone-900 mb-2">{t('analytics.scores.transparency')}</h4>
                        <p className="text-sm text-stone-600">{t('analytics.scores.transparencyDesc')}</p>
                      </div>
                      <div className="p-4 bg-stone-50 rounded-lg">
                        <h4 className="font-medium text-stone-900 mb-2">{t('analytics.scores.reviewDepth')}</h4>
                        <p className="text-sm text-stone-600">{t('analytics.scores.reviewDepthDesc')}</p>
                      </div>
                      <div className="p-4 bg-stone-50 rounded-lg">
                        <h4 className="font-medium text-stone-900 mb-2">{t('analytics.scores.editorialEffort')}</h4>
                        <p className="text-sm text-stone-600">{t('analytics.scores.editorialEffortDesc')}</p>
                      </div>
                      <div className="p-4 bg-stone-50 rounded-lg">
                        <h4 className="font-medium text-stone-900 mb-2">{t('analytics.scores.consistency')}</h4>
                        <p className="text-sm text-stone-600">{t('analytics.scores.consistencyDesc')}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
          </TabsContent>

          {/* Publishers Tab */}
          <TabsContent value="publishers" className="space-y-6" data-testid="publishers-tab">
            {publisherAnalytics.length === 0 ? (
              <Card className="border-stone-200">
                <CardContent className="p-12 text-center">
                  <AlertCircle className="w-12 h-12 text-amber-500 mx-auto mb-4" />
                  <p className="text-stone-600">{t('analytics.insufficientData')}</p>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-4">
                {publisherAnalytics.map((pub) => (
                  <Card key={pub.publisher_id} className="border-stone-200" data-testid={`publisher-${pub.publisher_id}`}>
                    <CardHeader className="pb-2">
                      <div className="flex items-center justify-between">
                        <div>
                          <CardTitle className="font-serif text-lg">{pub.publisher_name}</CardTitle>
                          <CardDescription>{pub.total_cases} {t('analytics.cases')}</CardDescription>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Badge variant="outline">{t('analytics.metrics.deskRejectRate')}: {pub.desk_reject_rate}%</Badge>
                          <Badge variant="outline">{t('analytics.metrics.noPeerReviewRate')}: {pub.no_peer_review_rate}%</Badge>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <ScoreCard 
                          label={t('analytics.scores.transparency')} 
                          description="Reviewer presence" 
                          score={pub.transparency_score} 
                        />
                        <ScoreCard 
                          label={t('analytics.scores.reviewDepth')} 
                          description="Comment quality" 
                          score={pub.review_depth_score} 
                        />
                        <ScoreCard 
                          label={t('analytics.scores.editorialEffort')} 
                          description="Editor engagement" 
                          score={pub.editorial_effort_score} 
                        />
                        <ScoreCard 
                          label={t('analytics.scores.consistency')} 
                          description="Review alignment" 
                          score={pub.consistency_score} 
                        />
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </TabsContent>

          {/* Journals Tab */}
          <TabsContent value="journals" className="space-y-6" data-testid="journals-tab">
            <div className="flex justify-between items-center">
              <p className="text-sm text-stone-600">
                {filteredJournals.length} journals with sufficient data
              </p>
              <Select value={selectedPublisher} onValueChange={setSelectedPublisher}>
                <SelectTrigger className="w-64" data-testid="publisher-filter">
                  <SelectValue placeholder={t('analytics.filterByPublisher')} />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">{t('analytics.allPublishers')}</SelectItem>
                  {publishers.map(pub => (
                    <SelectItem key={pub.publisher_id} value={pub.publisher_id}>
                      {pub.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {filteredJournals.length === 0 ? (
              <Card className="border-stone-200">
                <CardContent className="p-12 text-center">
                  <AlertCircle className="w-12 h-12 text-amber-500 mx-auto mb-4" />
                  <p className="text-stone-600">{t('analytics.insufficientData')}</p>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-4">
                {filteredJournals.slice(0, 20).map((journal) => (
                  <Card key={journal.journal_id} className="border-stone-200" data-testid={`journal-${journal.journal_id}`}>
                    <CardHeader className="pb-2">
                      <div className="flex items-center justify-between">
                        <div>
                          <CardTitle className="font-serif text-lg">{journal.journal_name}</CardTitle>
                          <CardDescription>{journal.publisher_name} • {journal.total_cases} {t('analytics.cases')}</CardDescription>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <ScoreCard 
                          label={t('analytics.scores.transparency')} 
                          description="" 
                          score={journal.transparency_score} 
                        />
                        <ScoreCard 
                          label={t('analytics.scores.reviewDepth')} 
                          description="" 
                          score={journal.review_depth_score} 
                        />
                        <ScoreCard 
                          label={t('analytics.scores.editorialEffort')} 
                          description="" 
                          score={journal.editorial_effort_score} 
                        />
                        <ScoreCard 
                          label={t('analytics.scores.consistency')} 
                          description="" 
                          score={journal.consistency_score} 
                        />
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </TabsContent>

          {/* Areas Tab */}
          <TabsContent value="areas" className="space-y-6" data-testid="areas-tab">
            {areaAnalytics.length === 0 ? (
              <Card className="border-stone-200">
                <CardContent className="p-12 text-center">
                  <AlertCircle className="w-12 h-12 text-amber-500 mx-auto mb-4" />
                  <p className="text-stone-600">{t('analytics.insufficientData')}</p>
                </CardContent>
              </Card>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {areaAnalytics.map((area) => (
                  <Card key={area.area} className="border-stone-200" data-testid={`area-${area.area}`}>
                    <CardHeader className="pb-2">
                      <CardTitle className="font-serif text-lg capitalize">
                        {area.area.replace(/_/g, ' ')}
                      </CardTitle>
                      <CardDescription>{area.total_cases} {t('analytics.cases')}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-stone-600">{t('analytics.metrics.deskRejectRate')}</span>
                          <Badge variant="outline">{area.desk_reject_rate}%</Badge>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-stone-600">{t('analytics.metrics.noPeerReviewRate')}</span>
                          <Badge variant="outline">{area.no_peer_review_rate}%</Badge>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-stone-600">{t('analytics.metrics.fastDecisionRate')}</span>
                          <Badge variant="outline">{area.fast_decision_rate}%</Badge>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-stone-600">{t('analytics.metrics.slowDecisionRate')}</span>
                          <Badge variant="outline">{area.slow_decision_rate}%</Badge>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </TabsContent>
        </Tabs>
      </main>

      <Footer />
    </div>
  );
}
