# PubProcess - Editorial Decision Statistics Platform

## Original Problem Statement
Build a global, anonymous, data-driven platform that aggregates editorial decision statistics from scientific journals, focusing on process transparency, not individual complaints.

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
- [x] **Controlled Data Visibility System** (NEW Jan 22, 2026)

## Data Visibility System (NEW)

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
- Users: `/api/users/profile`, `/api/users/my-insights` (NEW)
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
- Submission form (5-step wizard) with "Other" options
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
- 500 sample submissions with `is_sample: true` flag
- Platform settings in `platform_settings` collection

## Prioritized Backlog

### P0 (Critical) - DONE
- [x] Core submission flow
- [x] Anonymous data aggregation
- [x] Public analytics dashboards
- [x] Language toggle
- [x] Controlled Data Visibility System

### P1 (High Priority)
- [x] Admin dashboard for flagging/validating submissions
- [x] Admin Settings tab with visibility controls
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

## Completed This Session (Jan 22, 2026)
- ✅ ORCID OAuth 2.0 fix - now uses environment-driven redirect_uri
- ✅ Controlled Data Visibility System with 3 modes (user_only, threshold_based, admin_forced)
- ✅ Admin Settings tab with visibility mode, public stats toggle, demo mode toggle
- ✅ Sample data management (view stats, purge sample data)
- ✅ User Personal Insights on dashboard (editorial process, time distribution, top journals)
- ✅ Visibility banner on analytics page (professional messaging)
- ✅ Sample data flagged with is_sample=true for clean separation
- ✅ Trust score confirmed starting at 0 for new users
- ✅ All 28 backend tests passing (100%)
