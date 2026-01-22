# PubProcess - Editorial Decision Statistics Platform

## Original Problem Statement
Build a global, anonymous, data-driven platform that aggregates editorial decision statistics from scientific journals, focusing on process transparency, not individual complaints.

**Platform Positioning:** An infrastructure for data analysis of the scientific editorial process - capturing positive, neutral, and negative experiences equally.

## Architecture
- **Frontend**: React 19 + TailwindCSS + Shadcn UI + Recharts
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **Authentication**: Emergent Google OAuth + **ORCID OAuth 2.0** ✅
- **File Storage**: Local encrypted storage

## User Personas
1. **Researchers** - Submit editorial decisions anonymously to contribute to transparency
2. **PhD Students/Postdocs** - Explore journal statistics before submitting manuscripts
3. **Data Analysts** - Access aggregated statistics for meta-research

## Core Requirements
- [x] Anonymous user registration via Google OAuth
- [x] Hashed user IDs for anonymity
- [x] Structured submission form (no free text)
- [x] Evidence upload with encryption
- [x] K-anonymity (min 5 cases for public display)
- [x] Multi-dimensional scores (Transparency, Review Depth, Editorial Effort, Consistency)
- [x] i18n support (EN/PT/ES)
- [x] **Controlled Data Visibility System** ✅
- [x] **Quality Assessment System** ✅ (Jan 22, 2026)
- [x] **CNPq Hierarchical Scientific Areas** ✅ (Jan 22, 2026)
- [x] **Conditional Form Logic** ✅ (Jan 22, 2026)

## CNPq Hierarchical Scientific Areas (NEW Jan 22, 2026)

### Three-Level Hierarchy (Based on Official CNPq Table)
1. **Grande Área** (9 options): Top-level classification (e.g., "Ciências Exatas e da Terra")
2. **Área** (~80 options): Mid-level (e.g., "1.01 - Matemática")
3. **Subárea** (~400 options): Specific field (e.g., "1.01.01 - Álgebra")

### API Endpoints
- `GET /api/options/cnpq/grande-areas` - Returns all 9 Grande Áreas
- `GET /api/options/cnpq/areas/{code}` - Returns Áreas for given Grande Área
- `GET /api/options/cnpq/subareas/{code}` - Returns Subáreas for given Área
- `GET /api/options/cnpq/lookup/{code}` - Lookup any area by full code

### Form Implementation
- Cascading dropdowns: Grande Área → Área → Subárea
- Grande Área and Área are required
- Subárea is optional (some Áreas don't have Subáreas)

## Conditional Form Logic (NEW Jan 22, 2026)

### Open Access → APC Questions
- Question "O periódico é Open Access?" in Step 3
- APC range questions only appear if answer is "Sim"
- Non-Open Access journals automatically set `apc_range: "no_apc"`

### Editor Comments → Quality Rating
- If `editor_comments = "no"`, the editor quality rating is hidden
- Backend validation rejects `editor_comments_quality` when no comments were provided

### Backend Validation (validate_submission_for_stats)
- Checks logical consistency of conditional fields
- Flags inconsistent submissions (e.g., APC for non-open access)
- Only consistent submissions are included in aggregated statistics

## Quality Assessment System (Jan 22, 2026)

### New Submission Fields (Neutral Language)
- **overall_review_quality**: 1-5 scale (Very Low → Very High)
- **feedback_clarity**: 1-5 scale (Very Unclear → Very Clear)
- **decision_fairness**: agree / neutral / disagree
- **would_recommend**: yes / neutral / no

### Quality Indices (Aggregated)
- **Average Review Quality Score**: Mean of overall_review_quality (0-100 scale)
- **Feedback Clarity Index**: Mean of feedback_clarity (0-100 scale)
- **Decision Fairness Index**: % reporting decision aligned with feedback
- **Recommendation Index**: % who would recommend based on editorial process

### Submission Validation (`valid_for_stats`)
- **Completeness check**: All required fields present
- **Consistency check**: No contradictory responses (e.g., detailed comments with 0 reviewers)
- **Duplicate check**: No submissions to same journal within 30 days
- Flagged submissions excluded from aggregated statistics

### Messaging Tone (Institutional/Neutral)
- Portuguese professional language
- No language suggesting platform is "empty" or "in testing"
- Example: "As estatísticas agregadas são exibidas automaticamente quando há volume mínimo de dados para garantir interpretação adequada."

## Data Visibility System

### Three Visibility Modes
1. **User-Only (Mode A)** - Default
   - Public dashboards hidden/locked
   - Users see only their own submission history and personal insights
   - No public scores or rankings shown

2. **Threshold-Based (Mode B)**
   - Public stats visible when thresholds met (≥3 submissions from ≥3 users per journal)
   - Journals below threshold show "Data collection in progress"

3. **Admin-Forced (Mode C)**
   - Admin can manually enable/disable public stats
   - Override automatic thresholds for specific journals/publishers

### Admin Control Panel
- Global Settings: visibility_mode, public_stats_enabled, demo_mode_enabled
- Thresholds: min_submissions_per_journal, min_unique_users_per_journal
- Data Management: View sample vs real data counts, purge sample data
- Visibility Overrides: Per-journal/publisher/area visibility controls

### Sample Data Handling
- All sample data flagged with `is_sample: true`
- Can be purged with one admin action
- When demo mode disabled, sample data excluded from analytics
- Real user data always preserved

## What's Been Implemented

### Backend APIs
- Auth: `/api/auth/session`, `/api/auth/me`, `/api/auth/logout`, `/api/auth/orcid/*`
- Users: `/api/users/profile`, `/api/users/my-insights`
- Submissions: `/api/submissions`, `/api/submissions/my`, `/api/submissions/{id}/evidence`
- Publishers/Journals: `/api/publishers`, `/api/journals`
- Analytics: `/api/analytics/overview`, `/api/analytics/publishers`, `/api/analytics/journals`, `/api/analytics/areas`, `/api/analytics/visibility-status` (NEW)
- Form options: `/api/options/*`
- **Admin**: 
  - `/api/admin/stats`, `/api/admin/submissions`, `/api/admin/submissions/{id}/moderate`
  - `/api/admin/settings` (GET/PUT) (NEW)
  - `/api/admin/data/stats` (NEW)
  - `/api/admin/data/purge-sample` (NEW)
  - `/api/admin/visibility/override` (NEW)

### Frontend Pages
- Landing page with hero, features, privacy section, Auth Modal (Google + ORCID)
- Login page with Google OAuth + ORCID authentication
- Dashboard (protected) - user submissions, trust score, **Personal Insights section** (NEW)
- Submission form (6-step wizard) with hierarchical CNPq areas and conditional fields
- Analytics dashboard with visibility controls and professional messaging (UPDATED)
- Settings page (language, ORCID)
- Terms of Use & Privacy Policy
- **Admin Dashboard** - Submissions, Users, **Settings tab** (NEW)

### Trust Score System
- New users start with trust_score = 0 ✅
- Trust score hidden until: 2+ validated submissions OR 1 validated with evidence
- Calculation: +20 per validated, +10 per validated with evidence, -15 per flagged
- Capped at 0-100

### Database Seed Data
- 10 major publishers (Elsevier, Springer Nature, Wiley, MDPI, Frontiers, etc.)
- 100 journals (10 per publisher)
- 500 sample submissions with `is_sample: true` flag and quality assessment fields
- Platform settings in `platform_settings` collection

## Prioritized Backlog

### P0 (Critical) - DONE
- [x] Core submission flow
- [x] Anonymous data aggregation
- [x] Public analytics dashboards
- [x] Language toggle
- [x] Controlled Data Visibility System
- [x] Quality Assessment System (new neutral fields + indices)
- [x] CNPq Hierarchical Scientific Areas
- [x] Conditional Form Logic (Open Access/APC, Editor Comments/Quality)

### P1 (High Priority)
- [x] Admin dashboard for flagging/validating submissions
- [x] Admin Settings tab with visibility controls
- [x] Submission validation (valid_for_stats)
- [ ] Admin: Manage CNPq hierarchical areas (edit, activate/deactivate)
- [ ] User-added journal normalization workflow
- [ ] Email notifications for submission status
- [ ] Export analytics data (CSV/JSON)

### P2 (Medium Priority)
- [x] ORCID OAuth 2.0 authentication
- [ ] Advanced filtering on analytics
- [ ] Time-series analytics (trends over time)
- [ ] API rate limiting
- [ ] Optional account linking (Google + ORCID)

### P3 (Nice to Have)
- [ ] Mobile app (React Native)
- [ ] Comparison tool (compare 2+ journals)
- [ ] Community features (anonymized discussions)
- [ ] Integration with journal databases

## Next Tasks
1. Implement journal normalization workflow for user-added entries
2. Add email notifications for submission validation
3. Export analytics data functionality (CSV/JSON)
4. Optional account linking for users with both Google and ORCID
5. Fix admin dashboard screenshot test (authentication issue)

## Completed This Session (Jan 22, 2026)
- ✅ ORCID OAuth 2.0 fix - now uses environment-driven redirect_uri
- ✅ Controlled Data Visibility System with 3 modes (user_only, threshold_based, admin_forced)
- ✅ Admin Settings tab with visibility mode, public stats toggle, demo mode toggle
- ✅ Sample data management (view stats, purge sample data)
- ✅ User Personal Insights on dashboard (editorial process, time distribution, top journals)
- ✅ Visibility banner on analytics page (professional messaging)
- ✅ Sample data flagged with is_sample=true for clean separation
- ✅ Trust score confirmed starting at 0 for new users
- ✅ **Quality Assessment System** - New neutral fields capturing positive/neutral/negative experiences:
  - Form now has 6 steps (Step 5: Quality Assessment)
  - New fields: overall_review_quality (1-5), feedback_clarity (1-5), decision_fairness, would_recommend
  - New Quality Indices: Average Review Quality, Feedback Clarity Index, Decision Fairness Index, Recommendation Index
  - Submission validation with `valid_for_stats` flag (completeness, consistency, duplicate detection)
  - Institutional/neutral Portuguese messaging throughout
- ✅ **Hierarchical Scientific Areas** (Updated):
  - 9 Major Areas (Grande Áreas), ~80 Areas, ~400 Subareas
  - Cascading dropdowns in Step 1: Major Area → Area → Subarea
  - New endpoints: /api/options/cnpq/grande-areas, /areas/{code}, /subareas/{code}, /lookup/{code}
  - Backwards compatible with legacy scientific_area field
- ✅ **Conditional Form Logic**:
  - Open Access question controls APC visibility (Step 3)
  - Editor comments quality only appears if editor provided comments (Step 4)
  - Backend validation rejects logically inconsistent submissions
- ✅ **i18n Complete Translations** (Updated):
  - All new form fields fully translated in EN/PT/ES
  - Hierarchical area labels, conditional field labels, quality assessment descriptions
  - Language switching works correctly across entire form
- ✅ **Admin Areas Management Tab** (NEW):
  - New "Areas" tab in Admin dashboard
  - Hierarchy viewer: Major Area → Area → Subarea
  - Statistics summary showing counts at each level
  - Read-only view with future edit capability noted
- ✅ All 22 e2e tests passing (100%) - iteration_8.json
