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

## What's Been Implemented (Jan 21, 2026)

### Backend APIs
- Auth: `/api/auth/session`, `/api/auth/me`, `/api/auth/logout`, `/api/auth/orcid` (NEW)
- Users: `/api/users/profile`
- Submissions: `/api/submissions`, `/api/submissions/my`, `/api/submissions/{id}/evidence`
- Publishers/Journals: `/api/publishers`, `/api/journals`
- Analytics: `/api/analytics/overview`, `/api/analytics/publishers`, `/api/analytics/journals`, `/api/analytics/areas`
- Form options: `/api/options/*`
- **Admin**: `/api/admin/stats`, `/api/admin/submissions`, `/api/admin/submissions/{id}/moderate`, `/api/admin/evidence/{id}`, `/api/admin/users`, `/api/admin/users/{id}/toggle-admin`

### Frontend Pages
- Landing page with hero, features, privacy section, **Auth Modal (Google + ORCID)**
- Login page with **Google OAuth + ORCID authentication**
- Dashboard (protected) - user submissions & **conditional trust score display**
- Submission form (5-step wizard) with **"Other" options for publisher/journal**
- Analytics dashboard with 4 tabs (Overview, Publishers, Journals, Areas)
- Settings page (language, ORCID)
- Terms of Use & Privacy Policy
- **Admin Dashboard** (protected, admin-only) - Submissions moderation, User management

### Trust Score System (UPDATED)
- New users start with trust_score = 0
- Trust score hidden until: 2+ validated submissions OR 1 validated with evidence
- Calculation: +20 per validated, +10 per validated with evidence, -15 per flagged
- Capped at 0-100

### User-Added Journals Governance (NEW)
- User-added journals/publishers stored as "Unverified" (is_verified=false)
- Unverified entries excluded from public analytics
- Auto-promotion to "Verified" after 3+ validated submissions

### Database Seed Data
- 10 major publishers (Elsevier, Springer Nature, Wiley, MDPI, Frontiers, etc.)
- 100 journals (10 per publisher)
- 500 sample submissions with realistic distributions

## Prioritized Backlog

### P0 (Critical) - DONE
- [x] Core submission flow
- [x] Anonymous data aggregation
- [x] Public analytics dashboards
- [x] Language toggle

### P1 (High Priority)
- [x] Admin dashboard for flagging/validating submissions
- [ ] User-added journal normalization workflow
- [ ] Email notifications for submission status
- [ ] Export analytics data (CSV/JSON)

### P2 (Medium Priority)
- [x] ORCID OAuth 2.0 authentication (COMPLETED Jan 21, 2026)
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
