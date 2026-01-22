import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../i18n/LanguageContext';
import { useAuth } from '../contexts/AuthContext';
import Navbar from '../components/Navbar';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Label } from '../components/ui/label';
import { Input } from '../components/ui/input';
import { RadioGroup, RadioGroupItem } from '../components/ui/radio-group';
import { Checkbox } from '../components/ui/checkbox';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Progress } from '../components/ui/progress';
import { Slider } from '../components/ui/slider';
import { 
  ChevronRight, 
  ChevronLeft, 
  Upload, 
  CheckCircle2, 
  FileText,
  Shield,
  Loader2,
  AlertCircle,
  Star
} from 'lucide-react';

const API = process.env.REACT_APP_BACKEND_URL + '/api';

export default function SubmissionPage() {
  const { t } = useLanguage();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);
  
  // Form data
  const [formData, setFormData] = useState({
    scientific_area: '',
    manuscript_type: '',
    publisher_id: '',
    journal_id: '',
    decision_type: '',
    reviewer_count: '',
    time_to_decision: '',
    apc_range: '',
    review_comments: [],
    editor_comments: '',
    perceived_coherence: '',
    // NEW: Quality assessment fields
    overall_review_quality: null,
    feedback_clarity: null,
    decision_fairness: '',
    would_recommend: '',
    // Custom journal/publisher fields
    custom_publisher_name: '',
    custom_journal_name: '',
    custom_journal_open_access: null,
    custom_journal_apc_required: ''
  });
  
  const [evidenceFile, setEvidenceFile] = useState(null);
  const [submissionId, setSubmissionId] = useState(null);
  
  // Options from API
  const [options, setOptions] = useState({
    scientificAreas: [],
    manuscriptTypes: [],
    decisionTypes: [],
    reviewerCounts: [],
    timeRanges: [],
    apcRanges: [],
    reviewCommentTypes: [],
    editorCommentTypes: [],
    coherenceOptions: [],
    publishers: [],
    journals: [],
    // NEW: Quality assessment options
    reviewQualityScale: [],
    feedbackClarityScale: [],
    decisionFairnessOptions: [],
    wouldRecommendOptions: []
  });

  // Fetch options on mount
  useEffect(() => {
    const fetchOptions = async () => {
      setLoading(true);
      try {
        const [
          areas, types, decisions, reviewers, times, apcs, 
          reviewComments, editorComments, coherence, publishers
        ] = await Promise.all([
          fetch(`${API}/options/scientific-areas`).then(r => r.json()),
          fetch(`${API}/options/manuscript-types`).then(r => r.json()),
          fetch(`${API}/options/decision-types`).then(r => r.json()),
          fetch(`${API}/options/reviewer-counts`).then(r => r.json()),
          fetch(`${API}/options/time-ranges`).then(r => r.json()),
          fetch(`${API}/options/apc-ranges`).then(r => r.json()),
          fetch(`${API}/options/review-comment-types`).then(r => r.json()),
          fetch(`${API}/options/editor-comment-types`).then(r => r.json()),
          fetch(`${API}/options/coherence-options`).then(r => r.json()),
          fetch(`${API}/publishers`).then(r => r.json())
        ]);
        
        setOptions({
          scientificAreas: areas,
          manuscriptTypes: types,
          decisionTypes: decisions,
          reviewerCounts: reviewers,
          timeRanges: times,
          apcRanges: apcs,
          reviewCommentTypes: reviewComments,
          editorCommentTypes: editorComments,
          coherenceOptions: coherence,
          publishers: publishers,
          journals: []
        });
      } catch (err) {
        console.error('Failed to fetch options:', err);
        setError('Failed to load form options');
      }
      setLoading(false);
    };
    
    fetchOptions();
  }, []);

  // Fetch journals when publisher changes
  useEffect(() => {
    const fetchJournals = async () => {
      if (formData.publisher_id) {
        try {
          const journals = await fetch(`${API}/journals?publisher_id=${formData.publisher_id}`).then(r => r.json());
          setOptions(prev => ({ ...prev, journals }));
        } catch (err) {
          console.error('Failed to fetch journals:', err);
        }
      }
    };
    
    fetchJournals();
  }, [formData.publisher_id]);

  const totalSteps = 5;
  const progress = (step / totalSteps) * 100;

  const updateFormData = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const toggleReviewComment = (commentId) => {
    setFormData(prev => ({
      ...prev,
      review_comments: prev.review_comments.includes(commentId)
        ? prev.review_comments.filter(c => c !== commentId)
        : [...prev.review_comments, commentId]
    }));
  };

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file size (10MB max)
      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB');
        return;
      }
      setEvidenceFile(file);
      setError(null);
    }
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setError(null);
    
    try {
      // Submit form data
      const response = await fetch(`${API}/submissions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) throw new Error('Submission failed');
      
      const result = await response.json();
      setSubmissionId(result.submission_id);
      
      // Upload evidence if provided
      if (evidenceFile && result.submission_id) {
        const formDataFile = new FormData();
        formDataFile.append('file', evidenceFile);
        
        await fetch(`${API}/submissions/${result.submission_id}/evidence`, {
          method: 'POST',
          credentials: 'include',
          body: formDataFile
        });
      }
      
      setSuccess(true);
    } catch (err) {
      console.error('Submission error:', err);
      setError('Failed to submit. Please try again.');
    }
    
    setSubmitting(false);
  };

  const canProceed = () => {
    switch (step) {
      case 1:
        return formData.scientific_area && formData.manuscript_type;
      case 2:
        // Check publisher
        const publisherValid = formData.publisher_id && 
          (formData.publisher_id !== 'other' || formData.custom_publisher_name.trim());
        // Check journal
        const journalValid = formData.journal_id && 
          (formData.journal_id !== 'other' || formData.custom_journal_name.trim());
        return publisherValid && journalValid;
      case 3:
        return formData.decision_type && formData.reviewer_count && 
               formData.time_to_decision && formData.apc_range;
      case 4:
        return formData.editor_comments && formData.perceived_coherence;
      case 5:
        return true; // Evidence is optional
      default:
        return false;
    }
  };

  // Redirect if not authenticated
  if (!isAuthenticated) {
    navigate('/login');
    return null;
  }

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

  if (success) {
    return (
      <div className="min-h-screen bg-[#FAFAF9]">
        <Navbar />
        <div className="max-w-2xl mx-auto px-4 py-24">
          <Card className="border-stone-200 shadow-lg">
            <CardContent className="pt-12 pb-8 text-center">
              <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <CheckCircle2 className="w-8 h-8 text-emerald-600" />
              </div>
              <h2 className="font-serif text-2xl text-stone-900 mb-2">
                {t('submission.successTitle')}
              </h2>
              <p className="text-stone-600 mb-6">
                {t('submission.successDesc')}
              </p>
              <div className="bg-stone-50 rounded-lg p-4 mb-8 text-left">
                <div className="flex items-start space-x-3">
                  <Shield className="w-5 h-5 text-stone-500 mt-0.5" />
                  <p className="text-sm text-stone-600">
                    {t('submission.privacyReminder')}
                  </p>
                </div>
              </div>
              <div className="flex justify-center space-x-4">
                <Button 
                  variant="outline"
                  onClick={() => navigate('/dashboard')}
                  data-testid="view-submissions-btn"
                >
                  {t('dashboard.mySubmissions')}
                </Button>
                <Button 
                  onClick={() => {
                    setSuccess(false);
                    setStep(1);
                    setFormData({
                      scientific_area: '',
                      manuscript_type: '',
                      publisher_id: '',
                      journal_id: '',
                      decision_type: '',
                      reviewer_count: '',
                      time_to_decision: '',
                      apc_range: '',
                      review_comments: [],
                      editor_comments: '',
                      perceived_coherence: ''
                    });
                    setEvidenceFile(null);
                  }}
                  className="bg-stone-900 text-white hover:bg-stone-800"
                  data-testid="submit-another-btn"
                >
                  Submit Another
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#FAFAF9]">
      <Navbar />
      
      <div className="max-w-2xl mx-auto px-4 py-12">
        <div className="text-center mb-8">
          <h1 className="font-serif text-3xl text-stone-900 mb-2">
            {t('submission.title')}
          </h1>
          <p className="text-stone-600">
            {t('submission.subtitle')}
          </p>
        </div>

        {/* Progress */}
        <div className="mb-8">
          <div className="flex justify-between text-sm mb-2">
            <span className="text-stone-600">Step {step} of {totalSteps}</span>
            <span className="text-stone-500">{Math.round(progress)}%</span>
          </div>
          <Progress value={progress} className="h-2" />
          <div className="flex justify-between mt-2">
            {[
              t('submission.step1'),
              t('submission.step2'),
              t('submission.step3'),
              t('submission.step4'),
              t('submission.step5')
            ].map((label, i) => (
              <span 
                key={i} 
                className={`text-xs ${i + 1 <= step ? 'text-stone-900 font-medium' : 'text-stone-400'}`}
              >
                {label}
              </span>
            ))}
          </div>
        </div>

        <Card className="border-stone-200 shadow-lg">
          <CardContent className="p-8">
            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center space-x-3">
                <AlertCircle className="w-5 h-5 text-red-600" />
                <p className="text-red-700 text-sm">{error}</p>
              </div>
            )}

            {/* Step 1: Manuscript Context */}
            {step === 1 && (
              <div className="space-y-6" data-testid="step-1">
                <div>
                  <Label className="text-stone-700 font-medium mb-3 block">
                    {t('submission.scientificArea')}
                  </Label>
                  <Select 
                    value={formData.scientific_area} 
                    onValueChange={(v) => updateFormData('scientific_area', v)}
                  >
                    <SelectTrigger className="w-full" data-testid="scientific-area-select">
                      <SelectValue placeholder="Select area..." />
                    </SelectTrigger>
                    <SelectContent>
                      {options.scientificAreas.map(area => (
                        <SelectItem key={area.id} value={area.id}>
                          {area.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label className="text-stone-700 font-medium mb-3 block">
                    {t('submission.manuscriptType')}
                  </Label>
                  <RadioGroup 
                    value={formData.manuscript_type}
                    onValueChange={(v) => updateFormData('manuscript_type', v)}
                    className="grid grid-cols-2 gap-4"
                  >
                    {options.manuscriptTypes.map(type => (
                      <div key={type.id} className="flex items-center space-x-2">
                        <RadioGroupItem value={type.id} id={type.id} />
                        <Label htmlFor={type.id} className="cursor-pointer">{type.name}</Label>
                      </div>
                    ))}
                  </RadioGroup>
                </div>
              </div>
            )}

            {/* Step 2: Journal Context */}
            {step === 2 && (
              <div className="space-y-6" data-testid="step-2">
                <div>
                  <Label className="text-stone-700 font-medium mb-3 block">
                    {t('submission.selectPublisher')}
                  </Label>
                  <Select 
                    value={formData.publisher_id} 
                    onValueChange={(v) => {
                      updateFormData('publisher_id', v);
                      updateFormData('journal_id', ''); // Reset journal
                      if (v !== 'other') {
                        updateFormData('custom_publisher_name', '');
                      }
                    }}
                  >
                    <SelectTrigger className="w-full" data-testid="publisher-select">
                      <SelectValue placeholder="Select publisher..." />
                    </SelectTrigger>
                    <SelectContent>
                      {options.publishers.map(pub => (
                        <SelectItem key={pub.publisher_id} value={pub.publisher_id}>
                          {pub.name}
                        </SelectItem>
                      ))}
                      <SelectItem value="other" className="text-orange-700 font-medium">
                        Other / Not listed
                      </SelectItem>
                    </SelectContent>
                  </Select>
                  
                  {formData.publisher_id === 'other' && (
                    <div className="mt-3">
                      <Input
                        value={formData.custom_publisher_name}
                        onChange={(e) => updateFormData('custom_publisher_name', e.target.value)}
                        placeholder="Enter publisher name (will be reviewed)"
                        className="w-full"
                        data-testid="custom-publisher-input"
                      />
                    </div>
                  )}
                </div>

                <div>
                  <Label className="text-stone-700 font-medium mb-3 block">
                    {t('submission.selectJournal')}
                  </Label>
                  <Select 
                    value={formData.journal_id} 
                    onValueChange={(v) => {
                      updateFormData('journal_id', v);
                      if (v !== 'other') {
                        updateFormData('custom_journal_name', '');
                        updateFormData('custom_journal_open_access', null);
                        updateFormData('custom_journal_apc_required', '');
                      }
                    }}
                    disabled={!formData.publisher_id}
                  >
                    <SelectTrigger className="w-full" data-testid="journal-select">
                      <SelectValue placeholder={formData.publisher_id ? "Select journal..." : "Select publisher first"} />
                    </SelectTrigger>
                    <SelectContent>
                      {options.journals.map(journal => (
                        <SelectItem key={journal.journal_id} value={journal.journal_id}>
                          {journal.name}
                        </SelectItem>
                      ))}
                      <SelectItem value="other" className="text-orange-700 font-medium">
                        Journal not listed
                      </SelectItem>
                    </SelectContent>
                  </Select>
                  
                  {formData.journal_id === 'other' && (
                    <div className="mt-3 space-y-4 p-4 bg-stone-50 rounded-lg border border-stone-200">
                      <div>
                        <Label className="text-stone-600 text-sm mb-2 block">Journal Name *</Label>
                        <Input
                          value={formData.custom_journal_name}
                          onChange={(e) => updateFormData('custom_journal_name', e.target.value)}
                          placeholder="Enter journal name"
                          className="w-full"
                          data-testid="custom-journal-input"
                        />
                      </div>
                      
                      <div className="space-y-3">
                        <Label className="text-stone-600 text-sm block">Additional Info (optional)</Label>
                        
                        <div className="flex items-center space-x-2">
                          <Checkbox 
                            id="open-access"
                            checked={formData.custom_journal_open_access === true}
                            onCheckedChange={(checked) => updateFormData('custom_journal_open_access', checked ? true : null)}
                          />
                          <Label htmlFor="open-access" className="text-sm cursor-pointer">Open Access journal</Label>
                        </div>
                        
                        <div>
                          <Label className="text-stone-500 text-xs mb-1 block">APC Required?</Label>
                          <RadioGroup 
                            value={formData.custom_journal_apc_required}
                            onValueChange={(v) => updateFormData('custom_journal_apc_required', v)}
                            className="flex space-x-4"
                          >
                            <div className="flex items-center space-x-1">
                              <RadioGroupItem value="yes" id="apc-yes" />
                              <Label htmlFor="apc-yes" className="text-sm cursor-pointer">Yes</Label>
                            </div>
                            <div className="flex items-center space-x-1">
                              <RadioGroupItem value="no" id="apc-no" />
                              <Label htmlFor="apc-no" className="text-sm cursor-pointer">No</Label>
                            </div>
                            <div className="flex items-center space-x-1">
                              <RadioGroupItem value="unknown" id="apc-unknown" />
                              <Label htmlFor="apc-unknown" className="text-sm cursor-pointer">Unknown</Label>
                            </div>
                          </RadioGroup>
                        </div>
                      </div>
                      
                      <p className="text-xs text-stone-500">
                        User-added journals are stored as "Unverified" and won't appear in public rankings until validated.
                      </p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Step 3: Decision Process */}
            {step === 3 && (
              <div className="space-y-6" data-testid="step-3">
                <div>
                  <Label className="text-stone-700 font-medium mb-3 block">
                    {t('submission.decisionType')}
                  </Label>
                  <RadioGroup 
                    value={formData.decision_type}
                    onValueChange={(v) => updateFormData('decision_type', v)}
                    className="grid grid-cols-2 gap-4"
                  >
                    {options.decisionTypes.map(type => (
                      <div key={type.id} className="flex items-center space-x-2">
                        <RadioGroupItem value={type.id} id={`decision-${type.id}`} />
                        <Label htmlFor={`decision-${type.id}`} className="cursor-pointer">{type.name}</Label>
                      </div>
                    ))}
                  </RadioGroup>
                </div>

                <div>
                  <Label className="text-stone-700 font-medium mb-3 block">
                    {t('submission.reviewerCount')}
                  </Label>
                  <RadioGroup 
                    value={formData.reviewer_count}
                    onValueChange={(v) => updateFormData('reviewer_count', v)}
                    className="space-y-2"
                  >
                    {options.reviewerCounts.map(count => (
                      <div key={count.id} className="flex items-center space-x-2">
                        <RadioGroupItem value={count.id} id={`reviewer-${count.id}`} />
                        <Label htmlFor={`reviewer-${count.id}`} className="cursor-pointer">{count.name}</Label>
                      </div>
                    ))}
                  </RadioGroup>
                </div>

                <div>
                  <Label className="text-stone-700 font-medium mb-3 block">
                    {t('submission.timeToDecision')}
                  </Label>
                  <RadioGroup 
                    value={formData.time_to_decision}
                    onValueChange={(v) => updateFormData('time_to_decision', v)}
                    className="space-y-2"
                  >
                    {options.timeRanges.map(range => (
                      <div key={range.id} className="flex items-center space-x-2">
                        <RadioGroupItem value={range.id} id={`time-${range.id}`} />
                        <Label htmlFor={`time-${range.id}`} className="cursor-pointer">{range.name}</Label>
                      </div>
                    ))}
                  </RadioGroup>
                </div>

                <div>
                  <Label className="text-stone-700 font-medium mb-3 block">
                    {t('submission.apcRange')}
                  </Label>
                  <RadioGroup 
                    value={formData.apc_range}
                    onValueChange={(v) => updateFormData('apc_range', v)}
                    className="grid grid-cols-2 gap-4"
                  >
                    {options.apcRanges.map(range => (
                      <div key={range.id} className="flex items-center space-x-2">
                        <RadioGroupItem value={range.id} id={`apc-${range.id}`} />
                        <Label htmlFor={`apc-${range.id}`} className="cursor-pointer">{range.name}</Label>
                      </div>
                    ))}
                  </RadioGroup>
                </div>
              </div>
            )}

            {/* Step 4: Review Characteristics */}
            {step === 4 && (
              <div className="space-y-6" data-testid="step-4">
                <div>
                  <Label className="text-stone-700 font-medium mb-3 block">
                    {t('submission.reviewComments')}
                  </Label>
                  <div className="space-y-3">
                    {options.reviewCommentTypes.map(type => (
                      <div key={type.id} className="flex items-center space-x-2">
                        <Checkbox 
                          id={`comment-${type.id}`}
                          checked={formData.review_comments.includes(type.id)}
                          onCheckedChange={() => toggleReviewComment(type.id)}
                        />
                        <Label htmlFor={`comment-${type.id}`} className="cursor-pointer">{type.name}</Label>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <Label className="text-stone-700 font-medium mb-3 block">
                    {t('submission.editorComments')}
                  </Label>
                  <RadioGroup 
                    value={formData.editor_comments}
                    onValueChange={(v) => updateFormData('editor_comments', v)}
                    className="space-y-2"
                  >
                    {options.editorCommentTypes.map(type => (
                      <div key={type.id} className="flex items-center space-x-2">
                        <RadioGroupItem value={type.id} id={`editor-${type.id}`} />
                        <Label htmlFor={`editor-${type.id}`} className="cursor-pointer">{type.name}</Label>
                      </div>
                    ))}
                  </RadioGroup>
                </div>

                <div>
                  <Label className="text-stone-700 font-medium mb-3 block">
                    {t('submission.perceivedCoherence')}
                  </Label>
                  <RadioGroup 
                    value={formData.perceived_coherence}
                    onValueChange={(v) => updateFormData('perceived_coherence', v)}
                    className="space-y-2"
                  >
                    {options.coherenceOptions.map(option => (
                      <div key={option.id} className="flex items-center space-x-2">
                        <RadioGroupItem value={option.id} id={`coherence-${option.id}`} />
                        <Label htmlFor={`coherence-${option.id}`} className="cursor-pointer">{option.name}</Label>
                      </div>
                    ))}
                  </RadioGroup>
                </div>
              </div>
            )}

            {/* Step 5: Evidence Upload */}
            {step === 5 && (
              <div className="space-y-6" data-testid="step-5">
                <div>
                  <Label className="text-stone-700 font-medium mb-2 block">
                    {t('submission.uploadEvidence')}
                  </Label>
                  <p className="text-sm text-stone-500 mb-4">
                    {t('submission.uploadDesc')}
                  </p>
                  
                  <div className="border-2 border-dashed border-stone-200 rounded-lg p-8 text-center hover:border-stone-300 transition-colors">
                    <input
                      type="file"
                      id="evidence-file"
                      accept=".pdf,.png,.jpg,.jpeg"
                      onChange={handleFileChange}
                      className="hidden"
                    />
                    <label htmlFor="evidence-file" className="cursor-pointer">
                      {evidenceFile ? (
                        <div className="flex items-center justify-center space-x-3">
                          <FileText className="w-8 h-8 text-emerald-600" />
                          <div className="text-left">
                            <p className="font-medium text-stone-900">{evidenceFile.name}</p>
                            <p className="text-sm text-stone-500">
                              {(evidenceFile.size / 1024 / 1024).toFixed(2)} MB
                            </p>
                          </div>
                        </div>
                      ) : (
                        <>
                          <Upload className="w-12 h-12 text-stone-400 mx-auto mb-4" />
                          <p className="text-stone-600 font-medium mb-1">
                            {t('submission.dragDrop')}
                          </p>
                          <p className="text-sm text-stone-500">
                            {t('submission.supportedFormats')}
                          </p>
                        </>
                      )}
                    </label>
                  </div>
                </div>

                <div className="bg-stone-50 rounded-lg p-4">
                  <div className="flex items-start space-x-3">
                    <Shield className="w-5 h-5 text-stone-500 mt-0.5" />
                    <div className="text-sm text-stone-600">
                      <p className="font-medium mb-1">Privacy Guarantee</p>
                      <p>Your uploaded files are encrypted and stored securely. They are never made public and are used only for internal validation purposes.</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Navigation */}
            <div className="flex justify-between mt-8 pt-6 border-t border-stone-100">
              <Button
                variant="outline"
                onClick={() => setStep(prev => prev - 1)}
                disabled={step === 1}
                data-testid="back-btn"
              >
                <ChevronLeft className="w-4 h-4 mr-2" />
                {t('submission.back')}
              </Button>
              
              {step < totalSteps ? (
                <Button
                  onClick={() => setStep(prev => prev + 1)}
                  disabled={!canProceed()}
                  className="bg-stone-900 text-white hover:bg-stone-800"
                  data-testid="next-btn"
                >
                  {t('submission.next')}
                  <ChevronRight className="w-4 h-4 ml-2" />
                </Button>
              ) : (
                <Button
                  onClick={handleSubmit}
                  disabled={submitting}
                  className="bg-stone-900 text-white hover:bg-stone-800"
                  data-testid="submit-btn"
                >
                  {submitting ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      {t('submission.submitting')}
                    </>
                  ) : (
                    t('submission.submit')
                  )}
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
