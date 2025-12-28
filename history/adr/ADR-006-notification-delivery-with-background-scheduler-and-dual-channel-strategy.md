# ADR-006: Notification Delivery with Background Scheduler and Dual-Channel Strategy

> **Scope**: Clustered decision covering reminder processing infrastructure, notification delivery channels, email service integration, background job scheduling, and notification center persistence for Phase 2 task reminder feature.

- **Status:** Accepted
- **Date:** 2025-12-28
- **Feature:** 001-ps2-fullstack-web-foundation
- **Context:** User requested task reminder functionality with both email and browser notifications, requiring reliable scheduled delivery at exact times (e.g., "5 minutes before task due"). Must balance delivery reliability, user reach, infrastructure cost, and deployment complexity.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Adds background worker process, Redis dependency, email service cost, deployment complexity
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Serverless cron, client-side scheduling, background scheduler
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Impacts backend architecture, deployment strategy, infrastructure cost, user engagement
-->

## Decision

**Background Job Scheduler with Dual-Channel Notification Delivery**

Integrated notification solution components:

- **Job Scheduler**: Celery (Redis queue) OR APScheduler (in-memory for MVP)
  - Runs every 60 seconds checking `tasks` table for pending reminders
  - Calculates reminder time: `due_date` or next `schedule` occurrence minus `reminder_timing` offset
  - Sub-minute precision (30-second SLA for reminder delivery)

- **Notification Channels** (dual delivery for maximum reach):
  - **Browser Notifications**: Web Push API with permission request flow
    - Native OS notifications even when tab inactive
    - Bell icon in top bar with unread count
    - In-app notification center (persistent 30 days)
  - **Email Notifications**: Resend OR SendGrid transactional email
    - HTML template with task details (title, story, due date, link to dashboard)
    - Plain text fallback
    - User-configurable email address (defaults to account email)

- **Notification Persistence**:
  - `notifications` table stores all sent reminders for notification center
  - Auto-delete after 30 days (database cleanup job)
  - Cascade delete when task deleted
  - Mark as read/clicked for UI state

- **Delivery Logic**:
  1. Scheduler identifies due reminder (every 60s poll)
  2. Create `Notification` record in database
  3. If browser channel enabled + permission granted → send Web Push notification
  4. If email channel enabled → send via Resend/SendGrid
  5. If browser permission denied → show in-app notification center only
  6. Auto-cancel reminders when task marked complete or deleted

- **Infrastructure**:
  - Redis: Job queue persistence + retry handling (Celery) OR in-memory (APScheduler for MVP)
  - Background worker: Separate process from API server (scalable, can run on same container for MVP)
  - Email service: Resend free tier (3,000 emails/month) or SendGrid

## Consequences

### Positive

- **Reliable Delivery**: Background scheduler with Redis queue ensures reminders sent even during API downtime (messages queued for retry)
- **Maximum User Reach**: Dual-channel strategy (browser + email) covers users whether browser is open or closed
- **Graceful Degradation**: Falls back to in-app notification center if browser permission denied or email fails
- **Persistent Notification History**: 30-day retention in notification center provides historical record for users
- **Sub-Minute Precision**: 60-second polling interval delivers reminders within 30 seconds of scheduled time (acceptable UX)
- **Scalable Architecture**: Background worker can scale independently from API server (horizontal scaling for high reminder volume)
- **Context7 Support**: Celery and APScheduler patterns well-documented for FastAPI integration

### Negative

- **Infrastructure Complexity**: Requires Redis deployment alongside PostgreSQL (cost: ~$5-10/month on Railway/Render, or free tier on Upstash)
- **Deployment Overhead**: Background worker process requires separate container/dyno (cost: ~$7/month on Render, or free tier with limitations)
- **Email Service Cost**: Resend free tier 3,000 emails/month, then $0.10/1,000 emails (breaks at ~100 daily active users with 1 reminder/day)
- **Browser Permission Friction**: Users must grant notification permission (some browsers block by default, privacy-conscious users decline)
- **Debugging Complexity**: Distributed system (API + worker + Redis) harder to debug than synchronous flow
- **Polling Overhead**: 60-second polling adds constant database load (mitigated by indexed queries, ~10ms per poll)

## Alternatives Considered

**Alternative 1: Serverless Cron Jobs (Vercel Cron or GitHub Actions)**
- Approach: Vercel Cron triggers API endpoint every 1 minute to check pending reminders
- Pros: No separate worker process, no Redis dependency, simple deployment (single Vercel project)
- Cons:
  - Vercel Cron free tier limited to 1 cron job (need multiple for different frequencies)
  - No retry mechanism if cron invocation fails (missed reminders)
  - Cold start latency (serverless functions may take 1-2s to wake up)
  - Vendor lock-in to Vercel
  - Not suitable for high-frequency polling (60s is aggressive for cron)
- **Why Rejected**: Reliability concerns (no retry), Vercel lock-in, cold start latency unacceptable for time-sensitive reminders

**Alternative 2: Client-Side Reminder Scheduling (Browser localStorage + Service Worker)**
- Approach: Frontend schedules reminders in browser, Service Worker triggers notification at due time
- Pros: No backend infrastructure, instant notification (no polling delay), works offline
- Cons:
  - Unreliable (only works if browser open, Service Worker can be killed by OS)
  - No email fallback (user misses reminder if browser closed)
  - No notification history across devices (tied to single browser)
  - Security risk (reminder data in localStorage, no server validation)
- **Why Rejected**: Fundamental unreliability (user won't trust app if reminders missed), no email fallback, no cross-device sync

**Alternative 3: Database Triggers with pg_cron (PostgreSQL extension)**
- Approach: PostgreSQL pg_cron extension triggers SQL function every minute to send notifications
- Pros: No separate worker process, no Redis, everything in database
- Cons:
  - Neon Serverless PostgreSQL doesn't support pg_cron extension (vendor limitation)
  - Mixing business logic (email sending) with database layer (violates separation of concerns)
  - Hard to test (database-level logic harder to mock)
  - Limited error handling (SQL not ideal for HTTP requests)
- **Why Rejected**: Neon compatibility issue, poor separation of concerns, limited observability

## References

- Feature Spec: `specs/001-ps2-fullstack-web-foundation/spec.md` (User Story 7, FR-031 to FR-043: Notification & Reminders)
- Implementation Plan: `specs/001-ps2-fullstack-web-foundation/plan.md` (Phase 0 Task #8: Email Service, Task #9: Background Scheduler)
- Context7 Documentation:
  - Celery: `/celery/celery` (Python task queue)
  - APScheduler: `/agronholm/apscheduler` (Python job scheduler)
  - Resend: `/resend/resend` (email service)
- Related ADRs: None (orthogonal to auth and data model decisions)
- Cost Analysis:
  - Redis: Upstash free tier (10K commands/day) or Railway ($5/month)
  - Background Worker: Render free tier (750 hours/month) or Railway ($7/month)
  - Email: Resend free tier (3,000 emails/month)
  - **Total MVP cost**: $0 (free tiers) to $22/month (paid tiers for production)
