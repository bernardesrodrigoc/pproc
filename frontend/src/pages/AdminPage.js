import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Navbar from '../components/Navbar';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '../components/ui/dialog';
import { Textarea } from '../components/ui/textarea';
import { Label } from '../components/ui/label';
import { toast } from 'sonner';
import { 
  Shield, 
  Users, 
  FileText, 
  CheckCircle2, 
  AlertTriangle, 
  Clock,
  Eye,
  ChevronLeft,
  ChevronRight,
  Loader2,
  Download,
  UserCog,
  BarChart3
} from 'lucide-react';

const API = process.env.REACT_APP_BACKEND_URL + '/api';

export default function AdminPage() {
  const { user, isAdmin, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [users, setUsers] = useState([]);
  const [totalSubmissions, setTotalSubmissions] = useState(0);
  const [totalUsers, setTotalUsers] = useState(0);
  const [statusFilter, setStatusFilter] = useState('all');
  const [currentPage, setCurrentPage] = useState(0);
  const [activeTab, setActiveTab] = useState('submissions');
  
  // Modal state
  const [selectedSubmission, setSelectedSubmission] = useState(null);
  const [moderationNotes, setModerationNotes] = useState('');
  const [moderating, setModerating] = useState(false);
  const [viewingEvidence, setViewingEvidence] = useState(false);

  const pageSize = 20;

  // Check admin access
  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    } else if (!isAdmin) {
      navigate('/dashboard');
      toast.error('Admin access required');
    }
  }, [isAuthenticated, isAdmin, navigate]);

  // Fetch admin stats
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch(`${API}/admin/stats`, {
          credentials: 'include'
        });
        if (response.ok) {
          const data = await response.json();
          setStats(data);
        }
      } catch (error) {
        console.error('Failed to fetch stats:', error);
      }
    };

    if (isAdmin) {
      fetchStats();
    }
  }, [isAdmin]);

  // Fetch submissions
  useEffect(() => {
    const fetchSubmissions = async () => {
      setLoading(true);
      try {
        const statusParam = statusFilter !== 'all' ? `&status=${statusFilter}` : '';
        const response = await fetch(
          `${API}/admin/submissions?skip=${currentPage * pageSize}&limit=${pageSize}${statusParam}`,
          { credentials: 'include' }
        );
        if (response.ok) {
          const data = await response.json();
          setSubmissions(data.submissions);
          setTotalSubmissions(data.total);
        }
      } catch (error) {
        console.error('Failed to fetch submissions:', error);
      }
      setLoading(false);
    };

    if (isAdmin && activeTab === 'submissions') {
      fetchSubmissions();
    }
  }, [isAdmin, statusFilter, currentPage, activeTab]);

  // Fetch users
  useEffect(() => {
    const fetchUsers = async () => {
      setLoading(true);
      try {
        const response = await fetch(
          `${API}/admin/users?skip=${currentPage * pageSize}&limit=${pageSize}`,
          { credentials: 'include' }
        );
        if (response.ok) {
          const data = await response.json();
          setUsers(data.users);
          setTotalUsers(data.total);
        }
      } catch (error) {
        console.error('Failed to fetch users:', error);
      }
      setLoading(false);
    };

    if (isAdmin && activeTab === 'users') {
      fetchUsers();
    }
  }, [isAdmin, currentPage, activeTab]);

  const handleModerate = async (status) => {
    if (!selectedSubmission) return;
    
    setModerating(true);
    try {
      const response = await fetch(
        `${API}/admin/submissions/${selectedSubmission.submission_id}/moderate`,
        {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({
            status,
            admin_notes: moderationNotes || null
          })
        }
      );
      
      if (response.ok) {
        toast.success(`Submission ${status}`);
        setSelectedSubmission(null);
        setModerationNotes('');
        // Refresh submissions
        const statusParam = statusFilter !== 'all' ? `&status=${statusFilter}` : '';
        const refreshResponse = await fetch(
          `${API}/admin/submissions?skip=${currentPage * pageSize}&limit=${pageSize}${statusParam}`,
          { credentials: 'include' }
        );
        if (refreshResponse.ok) {
          const data = await refreshResponse.json();
          setSubmissions(data.submissions);
          setTotalSubmissions(data.total);
        }
        // Refresh stats
        const statsResponse = await fetch(`${API}/admin/stats`, { credentials: 'include' });
        if (statsResponse.ok) {
          setStats(await statsResponse.json());
        }
      } else {
        toast.error('Failed to moderate submission');
      }
    } catch (error) {
      console.error('Moderation error:', error);
      toast.error('An error occurred');
    }
    setModerating(false);
  };

  const handleToggleAdmin = async (userId) => {
    try {
      const response = await fetch(
        `${API}/admin/users/${userId}/toggle-admin`,
        {
          method: 'PUT',
          credentials: 'include'
        }
      );
      
      if (response.ok) {
        const data = await response.json();
        toast.success(`Admin status updated`);
        setUsers(users.map(u => 
          u.user_id === userId ? { ...u, is_admin: data.is_admin } : u
        ));
      } else {
        const error = await response.json();
        toast.error(error.detail || 'Failed to update admin status');
      }
    } catch (error) {
      console.error('Toggle admin error:', error);
      toast.error('An error occurred');
    }
  };

  const viewEvidence = (fileId) => {
    window.open(`${API}/admin/evidence/${fileId}`, '_blank');
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'validated':
        return (
          <Badge className="bg-emerald-100 text-emerald-800 hover:bg-emerald-100">
            <CheckCircle2 className="w-3 h-3 mr-1" />
            Validated
          </Badge>
        );
      case 'flagged':
        return (
          <Badge className="bg-red-100 text-red-800 hover:bg-red-100">
            <AlertTriangle className="w-3 h-3 mr-1" />
            Flagged
          </Badge>
        );
      default:
        return (
          <Badge className="bg-amber-100 text-amber-800 hover:bg-amber-100">
            <Clock className="w-3 h-3 mr-1" />
            Pending
          </Badge>
        );
    }
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString(undefined, { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
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

  const totalPages = Math.ceil(
    (activeTab === 'submissions' ? totalSubmissions : totalUsers) / pageSize
  );

  if (!isAdmin) {
    return null;
  }

  return (
    <div className="min-h-screen bg-[#FAFAF9]">
      <Navbar />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12" data-testid="admin-dashboard">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <Shield className="w-6 h-6 text-orange-700" />
              <h1 className="font-serif text-3xl text-stone-900">Admin Dashboard</h1>
            </div>
            <p className="text-stone-600">Moderate submissions and manage users</p>
          </div>
        </div>

        {/* Stats Grid */}
        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
            <Card className="border-stone-200">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs text-stone-500">Total Users</p>
                    <p className="text-2xl font-serif text-stone-900">{stats.total_users}</p>
                  </div>
                  <Users className="w-8 h-8 text-stone-300" />
                </div>
              </CardContent>
            </Card>
            <Card className="border-stone-200">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs text-stone-500">Total Submissions</p>
                    <p className="text-2xl font-serif text-stone-900">{stats.total_submissions}</p>
                  </div>
                  <FileText className="w-8 h-8 text-stone-300" />
                </div>
              </CardContent>
            </Card>
            <Card className="border-amber-200 bg-amber-50">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs text-amber-700">Pending</p>
                    <p className="text-2xl font-serif text-amber-900">{stats.pending_submissions}</p>
                  </div>
                  <Clock className="w-8 h-8 text-amber-300" />
                </div>
              </CardContent>
            </Card>
            <Card className="border-emerald-200 bg-emerald-50">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs text-emerald-700">Validated</p>
                    <p className="text-2xl font-serif text-emerald-900">{stats.validated_submissions}</p>
                  </div>
                  <CheckCircle2 className="w-8 h-8 text-emerald-300" />
                </div>
              </CardContent>
            </Card>
            <Card className="border-red-200 bg-red-50">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs text-red-700">Flagged</p>
                    <p className="text-2xl font-serif text-red-900">{stats.flagged_submissions}</p>
                  </div>
                  <AlertTriangle className="w-8 h-8 text-red-300" />
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={(v) => { setActiveTab(v); setCurrentPage(0); }}>
          <TabsList className="bg-white border border-stone-200 p-1 mb-6">
            <TabsTrigger value="submissions" className="data-[state=active]:bg-stone-900 data-[state=active]:text-white">
              <FileText className="w-4 h-4 mr-2" />
              Submissions
            </TabsTrigger>
            <TabsTrigger value="users" className="data-[state=active]:bg-stone-900 data-[state=active]:text-white">
              <Users className="w-4 h-4 mr-2" />
              Users
            </TabsTrigger>
          </TabsList>

          {/* Submissions Tab */}
          <TabsContent value="submissions" data-testid="submissions-tab">
            {/* Filter */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <Label>Filter by status:</Label>
                <Select value={statusFilter} onValueChange={(v) => { setStatusFilter(v); setCurrentPage(0); }}>
                  <SelectTrigger className="w-40" data-testid="status-filter">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All</SelectItem>
                    <SelectItem value="pending">Pending</SelectItem>
                    <SelectItem value="validated">Validated</SelectItem>
                    <SelectItem value="flagged">Flagged</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <p className="text-sm text-stone-500">
                {totalSubmissions} submission{totalSubmissions !== 1 ? 's' : ''}
              </p>
            </div>

            {/* Submissions List */}
            <Card className="border-stone-200">
              <CardContent className="p-0">
                {loading ? (
                  <div className="flex items-center justify-center py-12">
                    <Loader2 className="w-8 h-8 animate-spin text-stone-400" />
                  </div>
                ) : submissions.length === 0 ? (
                  <div className="text-center py-12">
                    <FileText className="w-12 h-12 text-stone-300 mx-auto mb-4" />
                    <p className="text-stone-500">No submissions found</p>
                  </div>
                ) : (
                  <div className="divide-y divide-stone-100">
                    {submissions.map((sub) => (
                      <div 
                        key={sub.submission_id}
                        className="p-4 hover:bg-stone-50 transition-colors"
                        data-testid={`admin-submission-${sub.submission_id}`}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-3 mb-1">
                              <p className="font-medium text-stone-900">{sub.journal_name}</p>
                              {getStatusBadge(sub.status)}
                              {sub.has_evidence && (
                                <Badge variant="outline" className="text-xs">
                                  Has Evidence
                                </Badge>
                              )}
                            </div>
                            <p className="text-sm text-stone-500">
                              {sub.publisher_name} • {getDecisionLabel(sub.decision_type)} • {formatDate(sub.created_at)}
                            </p>
                          </div>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setSelectedSubmission(sub)}
                            data-testid={`review-btn-${sub.submission_id}`}
                          >
                            <Eye className="w-4 h-4 mr-1" />
                            Review
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-center space-x-2 mt-4">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(p => Math.max(0, p - 1))}
                  disabled={currentPage === 0}
                >
                  <ChevronLeft className="w-4 h-4" />
                </Button>
                <span className="text-sm text-stone-600">
                  Page {currentPage + 1} of {totalPages}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(p => Math.min(totalPages - 1, p + 1))}
                  disabled={currentPage >= totalPages - 1}
                >
                  <ChevronRight className="w-4 h-4" />
                </Button>
              </div>
            )}
          </TabsContent>

          {/* Users Tab */}
          <TabsContent value="users" data-testid="users-tab">
            <Card className="border-stone-200">
              <CardContent className="p-0">
                {loading ? (
                  <div className="flex items-center justify-center py-12">
                    <Loader2 className="w-8 h-8 animate-spin text-stone-400" />
                  </div>
                ) : users.length === 0 ? (
                  <div className="text-center py-12">
                    <Users className="w-12 h-12 text-stone-300 mx-auto mb-4" />
                    <p className="text-stone-500">No users found</p>
                  </div>
                ) : (
                  <div className="divide-y divide-stone-100">
                    {users.map((u) => (
                      <div 
                        key={u.user_id}
                        className="p-4 hover:bg-stone-50 transition-colors flex items-center justify-between"
                        data-testid={`admin-user-${u.user_id}`}
                      >
                        <div className="flex items-center space-x-4">
                          {u.picture ? (
                            <img src={u.picture} alt="" className="w-10 h-10 rounded-full" />
                          ) : (
                            <div className="w-10 h-10 rounded-full bg-stone-200 flex items-center justify-center">
                              <Users className="w-5 h-5 text-stone-500" />
                            </div>
                          )}
                          <div>
                            <div className="flex items-center space-x-2">
                              <p className="font-medium text-stone-900">{u.name}</p>
                              {u.is_admin && (
                                <Badge className="bg-orange-100 text-orange-800">Admin</Badge>
                              )}
                            </div>
                            <p className="text-sm text-stone-500">{u.email}</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-4">
                          <div className="text-right">
                            <p className="text-sm text-stone-600">
                              Trust: {u.trust_score?.toFixed(0) || 50}
                            </p>
                            <p className="text-xs text-stone-400">
                              {u.contribution_count || 0} contributions
                            </p>
                          </div>
                          {u.user_id !== user?.user_id && (
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleToggleAdmin(u.user_id)}
                              data-testid={`toggle-admin-${u.user_id}`}
                            >
                              <UserCog className="w-4 h-4 mr-1" />
                              {u.is_admin ? 'Remove Admin' : 'Make Admin'}
                            </Button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Pagination */}
            {Math.ceil(totalUsers / pageSize) > 1 && (
              <div className="flex items-center justify-center space-x-2 mt-4">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(p => Math.max(0, p - 1))}
                  disabled={currentPage === 0}
                >
                  <ChevronLeft className="w-4 h-4" />
                </Button>
                <span className="text-sm text-stone-600">
                  Page {currentPage + 1} of {Math.ceil(totalUsers / pageSize)}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(p => Math.min(Math.ceil(totalUsers / pageSize) - 1, p + 1))}
                  disabled={currentPage >= Math.ceil(totalUsers / pageSize) - 1}
                >
                  <ChevronRight className="w-4 h-4" />
                </Button>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </main>

      {/* Submission Review Modal */}
      <Dialog open={!!selectedSubmission} onOpenChange={() => setSelectedSubmission(null)}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="font-serif">Review Submission</DialogTitle>
            <DialogDescription>
              Review the submission details and moderate accordingly
            </DialogDescription>
          </DialogHeader>
          
          {selectedSubmission && (
            <div className="space-y-6">
              {/* Status */}
              <div className="flex items-center space-x-2">
                <span className="text-sm text-stone-500">Current Status:</span>
                {getStatusBadge(selectedSubmission.status)}
              </div>

              {/* Submission Details */}
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-stone-50 rounded-lg p-4">
                  <p className="text-xs text-stone-500 mb-1">Journal</p>
                  <p className="font-medium text-stone-900">{selectedSubmission.journal_name}</p>
                  <p className="text-sm text-stone-600">{selectedSubmission.publisher_name}</p>
                </div>
                <div className="bg-stone-50 rounded-lg p-4">
                  <p className="text-xs text-stone-500 mb-1">Decision</p>
                  <p className="font-medium text-stone-900">{getDecisionLabel(selectedSubmission.decision_type)}</p>
                  <p className="text-sm text-stone-600">{selectedSubmission.time_to_decision} days</p>
                </div>
                <div className="bg-stone-50 rounded-lg p-4">
                  <p className="text-xs text-stone-500 mb-1">Reviewers</p>
                  <p className="font-medium text-stone-900">{selectedSubmission.reviewer_count}</p>
                </div>
                <div className="bg-stone-50 rounded-lg p-4">
                  <p className="text-xs text-stone-500 mb-1">APC</p>
                  <p className="font-medium text-stone-900">{selectedSubmission.apc_range}</p>
                </div>
                <div className="bg-stone-50 rounded-lg p-4">
                  <p className="text-xs text-stone-500 mb-1">Scientific Area</p>
                  <p className="font-medium text-stone-900 capitalize">{selectedSubmission.scientific_area?.replace(/_/g, ' ')}</p>
                </div>
                <div className="bg-stone-50 rounded-lg p-4">
                  <p className="text-xs text-stone-500 mb-1">Manuscript Type</p>
                  <p className="font-medium text-stone-900 capitalize">{selectedSubmission.manuscript_type}</p>
                </div>
              </div>

              {/* Review Comments */}
              <div className="bg-stone-50 rounded-lg p-4">
                <p className="text-xs text-stone-500 mb-2">Review Comment Types</p>
                <div className="flex flex-wrap gap-2">
                  {selectedSubmission.review_comments?.map((comment, i) => (
                    <Badge key={i} variant="outline" className="capitalize">
                      {comment.replace(/_/g, ' ')}
                    </Badge>
                  ))}
                  {(!selectedSubmission.review_comments || selectedSubmission.review_comments.length === 0) && (
                    <span className="text-sm text-stone-500">None specified</span>
                  )}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-stone-50 rounded-lg p-4">
                  <p className="text-xs text-stone-500 mb-1">Editor Comments</p>
                  <p className="font-medium text-stone-900 capitalize">{selectedSubmission.editor_comments?.replace(/_/g, ' ')}</p>
                </div>
                <div className="bg-stone-50 rounded-lg p-4">
                  <p className="text-xs text-stone-500 mb-1">Perceived Coherence</p>
                  <p className="font-medium text-stone-900 capitalize">{selectedSubmission.perceived_coherence}</p>
                </div>
              </div>

              {/* Evidence */}
              {selectedSubmission.has_evidence && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <FileText className="w-5 h-5 text-blue-600" />
                      <span className="font-medium text-blue-900">Evidence Attached</span>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => viewEvidence(selectedSubmission.evidence_file_id)}
                      data-testid="view-evidence-btn"
                    >
                      <Download className="w-4 h-4 mr-1" />
                      View Evidence
                    </Button>
                  </div>
                </div>
              )}

              {/* Admin Notes */}
              <div>
                <Label htmlFor="notes">Admin Notes (optional)</Label>
                <Textarea
                  id="notes"
                  value={moderationNotes}
                  onChange={(e) => setModerationNotes(e.target.value)}
                  placeholder="Add notes about this moderation decision..."
                  className="mt-1"
                  data-testid="moderation-notes"
                />
              </div>
            </div>
          )}

          <DialogFooter className="flex space-x-2">
            <Button
              variant="outline"
              onClick={() => setSelectedSubmission(null)}
            >
              Cancel
            </Button>
            <Button
              variant="outline"
              onClick={() => handleModerate('pending')}
              disabled={moderating || selectedSubmission?.status === 'pending'}
              data-testid="set-pending-btn"
            >
              <Clock className="w-4 h-4 mr-1" />
              Set Pending
            </Button>
            <Button
              variant="destructive"
              onClick={() => handleModerate('flagged')}
              disabled={moderating}
              data-testid="flag-btn"
            >
              {moderating ? <Loader2 className="w-4 h-4 mr-1 animate-spin" /> : <AlertTriangle className="w-4 h-4 mr-1" />}
              Flag
            </Button>
            <Button
              onClick={() => handleModerate('validated')}
              disabled={moderating}
              className="bg-emerald-600 hover:bg-emerald-700"
              data-testid="validate-btn"
            >
              {moderating ? <Loader2 className="w-4 h-4 mr-1 animate-spin" /> : <CheckCircle2 className="w-4 h-4 mr-1" />}
              Validate
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
