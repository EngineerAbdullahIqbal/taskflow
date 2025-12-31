# Tasks: Phase 2 Full-Stack Web Application Foundation

**Input**: Design documents from `/specs/001-ps2-fullstack-web-foundation/`
**Prerequisites**: plan.md (complete), spec.md (complete), 4 ADRs (complete)

**Organization**: Tasks grouped by user story to enable independent implementation and testing. Each user story can be developed and deployed incrementally.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

This is a **monorepo** with independent workspaces:
- **Backend**: `backend/app/` (FastAPI + SQLModel + Python)
- **Frontend**: `frontend/src/` (Next.js 16 + TypeScript + React)
- **Shared**: `shared/types/` (TypeScript API contract types)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Monorepo initialization, tooling configuration, and basic project structure

- [X] T001 Create monorepo root structure with frontend/, backend/, shared/, .github/workflows/
- [X] T002 Initialize frontend workspace with Next.js 16 App Router via `pnpm create next-app@latest`
- [X] T003 Initialize backend workspace with FastAPI + UV package manager via `uv init`
- [X] T004 [P] Configure frontend linting (ESLint + Prettier) in frontend/.eslintrc.json
- [X] T005 [P] Configure backend linting (Ruff) in backend/pyproject.toml
- [X] T006 [P] Setup TypeScript strict mode in frontend/tsconfig.json
- [X] T007 [P] Setup Python mypy --strict in backend/pyproject.toml
- [X] T008 [P] Install frontend dependencies: Better Auth, shadcn/ui, Tailwind CSS, React Hook Form, react-hot-toast
- [X] T009 [P] Install backend dependencies: FastAPI, SQLModel, Pydantic, python-jose, bcrypt, Alembic, Uvicorn
- [X] T010 Create environment variable templates (.env.example) for both frontend and backend
- [X] T011 [P] Configure Tailwind CSS in frontend/tailwind.config.js with design tokens (colors for priority levels)
- [X] T012 [P] Initialize shadcn/ui components in frontend/src/components/ui/
- [X] T013 Create monorepo README.md with setup instructions and architecture overview
- [X] T014 [P] Setup GitHub Actions CI workflow for frontend (.github/workflows/frontend-ci.yml)
- [X] T015 [P] Setup GitHub Actions CI workflow for backend (.github/workflows/backend-ci.yml)

**Checkpoint**: Project structure created, dependencies installed, CI configured

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database & ORM Foundation

- [X] T016 Setup Alembic for database migrations in backend/alembic/
- [X] T017 Configure SQLModel engine and async session factory in backend/app/utils/database.py
- [X] T018 Create database connection string configuration with Neon PostgreSQL in backend/app/config.py
- [X] T019 Create initial Alembic migration (001_create_tables.py) with all 5 tables (users, tasks, categories, notifications, notification_preferences)
- [X] T020 Test database connection and migration with `alembic upgrade head`

### Authentication Foundation (Better Auth + FastAPI JWT)

- [X] T021 Configure Better Auth in frontend with JWT plugin in frontend/src/lib/auth-config.ts
- [X] T022 Implement JWT middleware for FastAPI in backend/app/middleware/auth.py (verifies tokens, extracts user_id)
- [X] T023 Create password hashing utilities (bcrypt cost 12) in backend/app/utils/security.py
- [X] T024 Implement JWT token generation and refresh in backend/app/utils/jwt.py
- [X] T025 Create Better Auth React context provider in frontend/src/lib/auth-context.tsx

### API & Error Handling Infrastructure

- [X] T026 Setup FastAPI app with CORS middleware in backend/app/main.py
- [X] T027 Create global error handler for FastAPI in backend/app/middleware/error_handler.py
- [X] T028 Define standard API error response schemas in backend/app/schemas/error.py
- [X] T029 Create base API client with JWT header injection in frontend/src/lib/api/client.ts
- [X] T030 Setup API health check endpoint GET /api/health in backend/app/routes/health.py

### Shared Type Definitions

- [X] T031 [P] Create shared API type definitions in shared/types/api.ts (TaskResponse, UserResponse, etc.)
- [X] T032 [P] Export shared types from shared/types/index.ts for frontend consumption

**Checkpoint**: Foundation ready - authentication works, database connected, API routes functional. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - User Registration and Secure Login (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts and securely sign in with JWT authentication

**Independent Test**: Create account with email/password, logout, log back in. Verify JWT tokens issued and protected routes redirect unauthenticated users to login.

### Backend Implementation for User Story 1

- [X] T033 [P] [US1] Create User SQLModel in backend/app/models/user.py (id, email, name, password_hash, timestamps)
- [X] T034 [P] [US1] Create Pydantic schemas for auth in backend/app/schemas/auth.py (SignupRequest, LoginRequest, TokenResponse)
- [X] T035 [US1] Implement AuthService in backend/app/services/auth_service.py (signup, login, password verification)
- [X] T036 [US1] Implement POST /auth/signup endpoint in backend/app/routes/auth.py (create user, return JWT)
- [X] T037 [US1] Implement POST /auth/login endpoint in backend/app/routes/auth.py (verify credentials, return JWT)
- [X] T038 [US1] Implement POST /auth/logout endpoint in backend/app/routes/auth.py (token invalidation placeholder)
- [X] T039 [US1] Add email uniqueness validation and rate limiting (5 attempts/15min) to auth routes
- [X] T040 [US1] Add password strength validation (8+ chars, upper, lower, number, special) to signup

### Frontend Implementation for User Story 1

- [X] T041 [P] [US1] Create Signup page UI in frontend/src/app/(public)/signup/page.tsx
- [X] T042 [P] [US1] Create Login page UI in frontend/src/app/(public)/login/page.tsx
- [X] T043 [P] [US1] Create SignupForm component with React Hook Form in frontend/src/components/features/auth/SignupForm.tsx
- [X] T044 [P] [US1] Create LoginForm component with React Hook Form in frontend/src/components/features/auth/LoginForm.tsx
- [X] T045 [US1] Implement auth API client methods in frontend/src/lib/api/auth.ts (signUp, signIn, signOut)
- [X] T046 [US1] Create ProtectedRoute wrapper component in frontend/src/components/features/auth/ProtectedRoute.tsx
- [X] T047 [US1] Implement auth state management hook useAuth in frontend/src/hooks/useAuth.ts
- [X] T048 [US1] Create root layout with auth provider in frontend/src/app/layout.tsx
- [X] T049 [US1] Add form validation, error display, and loading states to signup/login forms
- [X] T050 [US1] Implement redirect logic (authenticated → dashboard, unauthenticated → login)

**Checkpoint**: Users can register, login, logout. JWT tokens issued and verified. Protected routes enforce authentication.

---

## Phase 4: User Story 2 - Create and View Rich Tasks/Habits (Priority: P1) 🎯 MVP

**Goal**: Enable users to create detailed tasks with title, story, priority, schedule, category and view them in a list

**Independent Test**: Login, create task "Morning Workout" with story, priority "High", schedule "Mon/Wed/Fri", category "Fitness", see it in task list with all attributes.

### Backend Implementation for User Story 2

- [ ] T051 [P] [US2] Create Task SQLModel in backend/app/models/task.py (id, user_id, title, story, priority, schedule, due_date, category_id, reminder fields, completed, timestamps)
- [ ] T052 [P] [US2] Create Category SQLModel in backend/app/models/category.py (id, user_id, name, color, timestamps)
- [ ] T053 [P] [US2] Create Pydantic schemas for tasks in backend/app/schemas/task.py (TaskCreate, TaskUpdate, TaskResponse)
- [ ] T054 [P] [US2] Create Pydantic schemas for categories in backend/app/schemas/category.py (CategoryCreate, CategoryUpdate, CategoryResponse)
- [ ] T055 [US2] Implement TaskService in backend/app/services/task_service.py (create, get_all, get_by_id with ownership verification)
- [ ] T056 [US2] Implement CategoryService in backend/app/services/category_service.py (create, get_all, update, delete with 20-category limit)
- [ ] T057 [US2] Implement POST /api/tasks endpoint in backend/app/routes/tasks.py (create task with validation)
- [ ] T058 [US2] Implement GET /api/tasks endpoint with pagination (20 per page) in backend/app/routes/tasks.py
- [ ] T059 [US2] Implement GET /api/tasks/{id} endpoint in backend/app/routes/tasks.py (ownership verification)
- [ ] T060 [US2] Implement POST /api/categories endpoint in backend/app/routes/categories.py
- [ ] T061 [US2] Implement GET /api/categories endpoint in backend/app/routes/categories.py
- [ ] T062 [US2] Add validation: title 1-200 chars, story max 2000 chars, schedule XOR due_date, category name unique per user

### Frontend Implementation for User Story 2

- [X] T063 [P] [US2] Create task API client methods in frontend/src/lib/api/tasks.ts (createTask, getTasks, getTaskById)
- [X] T064 [P] [US2] Create category API client methods in frontend/src/lib/api/categories.ts (createCategory, getCategories)
- [X] T065 [P] [US2] Create Task TypeScript interface in frontend/src/types/task.ts
- [X] T066 [P] [US2] Create Category TypeScript interface in frontend/src/types/category.ts
- [X] T067 [P] [US2] Create Dashboard page in frontend/src/app/(auth)/dashboard/page.tsx
- [X] T068 [P] [US2] Create TaskList component in frontend/src/components/features/tasks/TaskList.tsx
- [X] T069 [P] [US2] Create TaskItem card component in frontend/src/components/features/tasks/TaskItem.tsx (displays title, story, priority badge, category badge, schedule)
- [X] T070 [P] [US2] Create PriorityIndicator badge component in frontend/src/components/features/tasks/PriorityIndicator.tsx (color-coded: Low=blue, Med=yellow, High=orange, Urgent=red)
- [X] T071 [P] [US2] Create CategoryBadge component in frontend/src/components/features/tasks/CategoryBadge.tsx (name + color)
- [X] T072 [US2] Create CreateTaskModal component in frontend/src/components/features/tasks/CreateTaskModal.tsx (form with all fields)
- [X] T073 [US2] Create CategorySelector dropdown in frontend/src/components/features/categories/CategorySelector.tsx (with on-the-fly creation)
- [X] T074 [US2] Create ScheduleSelector component for day checkboxes in frontend/src/components/features/tasks/ScheduleSelector.tsx
- [X] T075 [US2] Implement useTasks hook for data fetching/mutations in frontend/src/hooks/useTasks.ts
- [X] T076 [US2] Implement useCategories hook in frontend/src/hooks/useCategories.ts
- [X] T077 [US2] Add loading states, error handling, and success toasts to task creation flow

**Checkpoint**: Users can create rich tasks with all fields, view them in paginated list. Categories work with on-the-fly creation. Data isolation verified (users only see own tasks).

---

## Phase 5: User Story 7 - Task Reminders with Email and Browser Notifications (Priority: P2)

**Goal**: Enable users to set reminders for tasks and receive notifications via email and browser

**Independent Test**: Create task with due date, set reminder "5 min before", enable email notification with custom email, verify browser notification and email sent at reminder time. Bell icon shows notification in center.

### Backend Implementation for User Story 7

- [ ] T078 [P] [US7] Create Notification SQLModel in backend/app/models/notification.py (id, user_id, task_id, type, title, message, read, clicked, created_at)
- [ ] T079 [P] [US7] Create NotificationPreference SQLModel in backend/app/models/notification_preference.py (id, user_id, reminder_email, email/browser enabled, timestamps)
- [ ] T080 [P] [US7] Create Pydantic schemas for notifications in backend/app/schemas/notification.py (NotificationResponse, MarkReadRequest)
- [ ] T081 [P] [US7] Create Pydantic schemas for preferences in backend/app/schemas/preference.py (NotificationPreferenceUpdate, NotificationPreferenceResponse)
- [ ] T082 [US7] Implement NotificationService in backend/app/services/notification_service.py (create, get_user_notifications, mark_read)
- [ ] T083 [US7] Implement EmailService in backend/app/services/email_service.py (send_reminder_email via Resend/SendGrid)
- [ ] T084 [US7] Create email HTML template in backend/app/templates/reminder_email.html
- [ ] T085 [US7] Create email plain text template in backend/app/templates/reminder_email.txt
- [ ] T086 [US7] Implement ReminderScheduler background job in backend/app/jobs/reminder_scheduler.py (60-second polling)
- [ ] T087 [US7] Implement ReminderProcessor in backend/app/jobs/reminder_processor.py (send browser + email notifications)
- [ ] T088 [US7] Setup Celery or APScheduler worker configuration in backend/app/jobs/__init__.py
- [ ] T089 [US7] Setup Redis connection for Celery job queue in backend/app/config.py
- [ ] T090 [US7] Implement GET /api/notifications endpoint in backend/app/routes/notifications.py (list user notifications)
- [ ] T091 [US7] Implement PATCH /api/notifications/{id}/read endpoint in backend/app/routes/notifications.py
- [ ] T092 [US7] Implement GET /api/user/notification-preferences endpoint in backend/app/routes/preferences.py
- [ ] T093 [US7] Implement PUT /api/user/notification-preferences endpoint in backend/app/routes/preferences.py
- [ ] T094 [US7] Add auto-cancel reminders logic when task completed or deleted (cascade)
- [ ] T095 [US7] Add 30-day notification retention cleanup job

### Frontend Implementation for User Story 7

- [ ] T096 [P] [US7] Create notification API client methods in frontend/src/lib/api/notifications.ts
- [ ] T097 [P] [US7] Create preferences API client methods in frontend/src/lib/api/preferences.ts
- [ ] T098 [P] [US7] Create notification-service.ts for Web Push API integration in frontend/src/lib/notification-service.ts
- [ ] T099 [P] [US7] Create Notification TypeScript interface in frontend/src/types/notification.ts
- [ ] T100 [P] [US7] Create NotificationBell component (bell icon + unread count) in frontend/src/components/features/notifications/NotificationBell.tsx
- [ ] T101 [P] [US7] Create NotificationCenter dropdown component in frontend/src/components/features/notifications/NotificationCenter.tsx
- [ ] T102 [P] [US7] Create NotificationItem card component in frontend/src/components/features/notifications/NotificationItem.tsx
- [ ] T103 [P] [US7] Create ReminderSettings component (timing + channels) in frontend/src/components/features/tasks/ReminderSettings.tsx
- [ ] T104 [US7] Implement useNotifications hook in frontend/src/hooks/useNotifications.ts
- [ ] T105 [US7] Add ReminderSettings to CreateTaskModal and EditTaskModal
- [ ] T106 [US7] Add NotificationBell to dashboard layout header
- [ ] T107 [US7] Implement browser notification permission request flow
- [ ] T108 [US7] Add Service Worker for Web Push API in frontend/public/sw.js
- [ ] T109 [US7] Implement notification click handler (navigate to task detail)

**Checkpoint**: Users can set reminders with custom timing and channels. Browser notifications work with permission flow. Email notifications sent via Resend/SendGrid. Bell icon shows notification center with 30-day history.

---

## Phase 6: User Story 3 - Mark Tasks Complete and Delete Tasks (Priority: P2)

**Goal**: Enable users to mark tasks as complete and delete tasks they no longer need

**Independent Test**: Create task, mark it complete (visual indicator), unmark, mark complete again, then delete it permanently.

### Backend Implementation for User Story 3

- [ ] T110 [US3] Implement PATCH /api/tasks/{id}/complete endpoint in backend/app/routes/tasks.py (toggle completion)
- [ ] T111 [US3] Implement DELETE /api/tasks/{id} endpoint in backend/app/routes/tasks.py (with ownership verification)
- [ ] T112 [US3] Add cascading delete logic for notifications when task deleted

### Frontend Implementation for User Story 3

- [ ] T113 [P] [US3] Add complete toggle button to TaskItem component
- [ ] T114 [P] [US3] Add delete button with confirmation to TaskItem component
- [ ] T115 [US3] Update task API client with updateTask, deleteTask methods in frontend/src/lib/api/tasks.ts
- [ ] T116 [US3] Add visual indicators for completed tasks (strikethrough, checkbox, opacity)
- [ ] T117 [US3] Add optimistic updates for completion toggle in useTasks hook
- [ ] T118 [US3] Add delete confirmation modal component

**Checkpoint**: Users can toggle task completion with visual feedback. Deletion works with confirmation and removes task + associated notifications.

---

## Phase 7: User Story 4 - Update Task Details (Priority: P2)

**Goal**: Enable users to edit existing task fields (title, story, priority, schedule, category)

**Independent Test**: Create task, click edit, update title/priority/category/schedule, save, verify all changes reflected.

### Backend Implementation for User Story 4

- [ ] T119 [US4] Implement PATCH /api/tasks/{id} endpoint in backend/app/routes/tasks.py (update task fields with validation)
- [ ] T120 [US4] Add validation for edit: title required, story max 2000 chars, schedule XOR due_date

### Frontend Implementation for User Story 4

- [ ] T121 [P] [US4] Create EditTaskModal component in frontend/src/components/features/tasks/EditTaskModal.tsx (pre-filled form)
- [ ] T122 [US4] Add edit button to TaskItem component that opens EditTaskModal
- [ ] T123 [US4] Implement edit flow with React Hook Form in EditTaskModal
- [ ] T124 [US4] Add cancel button that discards changes
- [ ] T125 [US4] Update useTasks hook to support edit mutations

**Checkpoint**: Users can edit all task fields. Validation enforced. Cancel button discards changes.

---

## Phase 8: User Story 5 - Filter and Sort Tasks (Priority: P3)

**Goal**: Enable users to filter tasks by status/priority/category and sort by various fields

**Independent Test**: Create 10 tasks with varying attributes, apply filter "High priority + Work category", sort by due date, verify correct results.

### Backend Implementation for User Story 5

- [ ] T126 [US5] Add query parameters to GET /api/tasks for filtering (status, priority, category_id) in backend/app/routes/tasks.py
- [ ] T127 [US5] Add query parameters for sorting (sort_by: created_at, due_date, priority, title; order: asc/desc)
- [ ] T128 [US5] Implement filtering logic in TaskService.get_all() method
- [ ] T129 [US5] Add database indexes for priority, category_id, due_date, created_at columns

### Frontend Implementation for User Story 5

- [ ] T130 [P] [US5] Create FilterPanel component in frontend/src/components/features/tasks/FilterPanel.tsx (status, priority, category dropdowns)
- [ ] T131 [P] [US5] Create SortControls component in frontend/src/components/features/tasks/SortControls.tsx
- [ ] T132 [US5] Add filter/sort state management to useTasks hook
- [ ] T133 [US5] Update task list to reflect filter/sort settings
- [ ] T134 [US5] Add URL query params for filter/sort persistence

**Checkpoint**: Users can filter by status/priority/category and sort by multiple fields. Results update in real-time.

---

## Phase 9: User Story 6 - Responsive Mobile Access (Priority: P3)

**Goal**: Ensure application works seamlessly on mobile, tablet, and desktop

**Independent Test**: Open app on mobile browser (375px), perform core actions (login, create task, mark complete), verify layout adapts without breaking.

### Frontend Implementation for User Story 6

- [ ] T135 [P] [US6] Add responsive breakpoints to Tailwind config (sm: 640px, md: 768px, lg: 1024px)
- [ ] T136 [P] [US6] Make TaskList responsive (stack on mobile, grid on tablet/desktop)
- [ ] T137 [P] [US6] Make TaskItem cards mobile-friendly (touch targets ≥44px, readable text)
- [ ] T138 [P] [US6] Make CreateTaskModal responsive (full screen on mobile, modal on desktop)
- [ ] T139 [P] [US6] Make FilterPanel responsive (collapsible on mobile)
- [ ] T140 [P] [US6] Add hamburger menu for mobile navigation
- [ ] T141 [US6] Test on real devices (iOS Safari, Android Chrome) and fix layout issues
- [ ] T142 [US6] Add viewport meta tag and prevent zoom on input focus

**Checkpoint**: Application fully functional on mobile (375px), tablet (768px), desktop (1024px+). Touch-friendly UI, no horizontal scroll.

---

## Phase 11: User Story 8 - High-Conversion Landing Page (Priority: P1)

**Story Goal**: Implement a modern, high-performance landing page with glassmorphism design and Framer Motion animations to serve as the primary entry point for Task-Flow, driving user engagement and sign-ups.

**Independent Test**: Navigate to root URL (`/`), verify hero section loads in < 2s with glassmorphism effects, scroll to view Bento grid feature showcase with staggered animations, click "Get Started" CTA to navigate to `/signup`, test responsive behavior on mobile (375px) and desktop (1024px+), verify WCAG 2.1 AA accessibility with keyboard navigation and screen reader.

**ADR Reference**: See `history/adr/0001-glassmorphism-styling-strategy-with-tailwind-backdrop-filters.md` for styling implementation approach.

### Dependencies & Setup

- [ ] T171 [P] [US8] Install Framer Motion in frontend workspace via `pnpm add framer-motion`
- [ ] T172 [P] [US8] Configure Tailwind CSS for glassmorphism utilities in frontend/tailwind.config.ts (extend backdrop-blur values if needed)
- [ ] T173 [P] [US8] Create brand constants file in frontend/src/lib/constants.ts (site name, colors, feature list)
- [ ] T174 [P] [US8] Add Open Graph image asset to frontend/public/og-image.png (1200x630px for social sharing)

### Root Layout & SEO Configuration

- [ ] T175 [US8] Update root layout metadata in frontend/src/app/layout.tsx with title, description, openGraph, twitter tags
- [ ] T176 [P] [US8] Configure robots.txt in frontend/public/robots.txt to allow crawling
- [ ] T177 [P] [US8] Add canonical URL configuration to layout for SEO

### Landing Page Components (Glassmorphism + Framer Motion)

- [ ] T178 [P] [US8] Create HeroSection component in frontend/src/app/(landing)/components/HeroSection.tsx with glassmorphism effects (backdrop-blur-lg, bg-white/10) and Framer Motion entrance animations (fade-in, slide-up)
- [ ] T179 [P] [US8] Create BentoGrid container component in frontend/src/app/(landing)/components/BentoGrid.tsx with staggerChildren animation variants
- [ ] T180 [P] [US8] Create FeatureCard component in frontend/src/app/(landing)/components/FeatureCard.tsx with whileInView scroll-triggered animations and glassmorphism styling
- [ ] T181 [P] [US8] Create Navbar component in frontend/src/app/(landing)/components/Navbar.tsx with translucent background (backdrop-blur-md, bg-white/20)
- [ ] T182 [P] [US8] Create Footer component in frontend/src/app/(landing)/components/Footer.tsx with links to privacy/terms and social media

### Root Page Assembly

- [ ] T183 [US8] Implement root page in frontend/src/app/page.tsx (Server Component) composing Navbar, HeroSection, BentoGrid (with 4-6 FeatureCards), Footer
- [ ] T184 [US8] Add "Get Started" CTA button in HeroSection linking to `/signup` route
- [ ] T185 [US8] Populate BentoGrid with feature cards showcasing: task creation, priority management, categories, reminders (content from constants.ts)

### Responsive & Performance Optimization

- [ ] T186 [P] [US8] Implement mobile-first responsive design using Tailwind breakpoints (sm:, md:, lg:) - BentoGrid adapts from grid-cols-1 to md:grid-cols-2 to lg:grid-cols-3
- [ ] T187 [P] [US8] Add conditional glassmorphism reduction on mobile screens (< 768px) for performance using responsive variants
- [ ] T188 [P] [US8] Optimize images with next/image component (priority prop for hero image, sizes prop for responsive images)
- [ ] T189 [P] [US8] Implement font optimization with next/font for local font loading to minimize layout shift

### Accessibility (WCAG 2.1 AA)

- [ ] T190 [P] [US8] Add semantic HTML5 tags (header, main, section, footer) for document structure
- [ ] T191 [P] [US8] Ensure color contrast ≥4.5:1 for all text on glassmorphism backgrounds (test with WebAIM contrast checker)
- [ ] T192 [P] [US8] Add keyboard navigation support (Tab, Enter) for all interactive elements (CTAs, navbar links)
- [ ] T193 [P] [US8] Add ARIA attributes (aria-label, aria-describedby) to sections and interactive elements for screen readers
- [ ] T194 [P] [US8] Verify touch targets ≥44x44px for mobile accessibility on CTA buttons and links

### Testing & Validation

- [ ] T195 [P] [US8] Write React Testing Library unit test for HeroSection component in frontend/tests/components/HeroSection.test.tsx
- [ ] T196 [P] [US8] Write React Testing Library unit test for BentoGrid and FeatureCard components in frontend/tests/components/BentoGrid.test.tsx
- [ ] T197 [P] [US8] Write Playwright E2E test verifying "Get Started" button navigates to /signup in frontend/tests/e2e/landing-page.spec.ts
- [ ] T198 [P] [US8] Write Playwright E2E test for responsive behavior (375px, 768px, 1024px viewports)
- [ ] T199 [US8] Run Lighthouse audit on landing page - verify Performance ≥90, Accessibility ≥90, SEO ≥90, load time < 2s
- [ ] T200 [P] [US8] Perform manual keyboard navigation test (Tab through all interactive elements, Enter to activate CTAs)
- [ ] T201 [P] [US8] Perform manual screen reader test (NVDA or VoiceOver) to verify all sections and CTAs are properly announced

### Integration with Existing Auth Routes

- [ ] T202 [US8] Verify root page (`/`) is publicly accessible (no auth guard) and navigation to `/signup` and `/login` works correctly
- [ ] T203 [US8] Test full user flow: Landing page → Click "Get Started" → Signup → Login → Dashboard

**Checkpoint**: Landing page live at root URL with glassmorphism design, Framer Motion animations, < 2s load time, responsive across mobile/tablet/desktop, WCAG 2.1 AA accessible, "Get Started" CTA navigates to signup.

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, quality gates, deployment

### Category Management Enhancements

- [ ] T143 [P] Implement PUT /api/categories/{id} endpoint in backend/app/routes/categories.py
- [ ] T144 [P] Implement DELETE /api/categories/{id} endpoint with null-cascade logic
- [ ] T145 [P] Create CategoryManager component in frontend/src/components/features/categories/CategoryManager.tsx (CRUD interface)

### Performance Optimization

- [ ] T146 [P] Add React.lazy() code splitting for modals and heavy components
- [ ] T147 [P] Implement pagination UI component for task list
- [ ] T148 [P] Add loading skeletons for better perceived performance
- [ ] T149 [P] Optimize database queries with proper indexes
- [ ] T150 [P] Add query result caching in useTasks hook

### Security Hardening

- [ ] T151 [P] Run npm audit and fix frontend vulnerabilities
- [ ] T152 [P] Run safety check and fix backend vulnerabilities
- [ ] T153 [P] Add CSRF protection to API endpoints
- [ ] T154 [P] Add input sanitization for XSS prevention
- [ ] T155 [P] Verify secrets not committed (.env files in .gitignore)

### Testing & Quality Gates

- [ ] T156 [P] Run ESLint + Prettier on frontend, fix all errors
- [ ] T157 [P] Run Ruff on backend, fix all errors
- [ ] T158 [P] Run TypeScript strict type checking, fix all errors
- [ ] T159 [P] Run mypy --strict on backend, fix all type errors
- [ ] T160 [P] Achieve Lighthouse score ≥90 (Performance, Accessibility, Best Practices, SEO)
- [ ] T161 [P] Verify WCAG 2.1 AA compliance (color contrast, keyboard navigation, screen reader)

### Documentation & Deployment

- [ ] T162 [P] Create quickstart.md with local dev setup instructions in specs/001-ps2-fullstack-web-foundation/
- [ ] T163 [P] Document API endpoints with OpenAPI/Swagger in backend
- [ ] T164 [P] Add deployment guide for Vercel (frontend) + Render/Railway (backend + worker)
- [ ] T165 [P] Setup Neon PostgreSQL database in cloud
- [ ] T166 [P] Configure environment variables for production (BETTER_AUTH_SECRET, DATABASE_URL, RESEND_API_KEY)
- [ ] T167 Deploy frontend to Vercel with automatic previews
- [ ] T168 Deploy backend + background worker to Render/Railway
- [ ] T169 Run smoke tests on production (signup → login → create task → set reminder → mark complete → delete)
- [ ] T170 Create demo video (<90s) showing all user stories

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-9)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 10)**: Depends on desired user stories being complete

### User Story Dependencies

- **US1 (Auth)**: Can start after Foundational - No dependencies on other stories
- **US2 (Create/View Tasks)**: Can start after Foundational - No dependencies (but needs US1 for login in practice)
- **US7 (Reminders)**: Can start after Foundational - Extends US2 (adds reminder fields to tasks)
- **US3 (Complete/Delete)**: Can start after Foundational - Extends US2 (operates on existing tasks)
- **US4 (Edit)**: Can start after Foundational - Extends US2 (operates on existing tasks)
- **US5 (Filter/Sort)**: Can start after Foundational - Enhances US2 (filters/sorts task list)
- **US6 (Responsive)**: Can start after Foundational - Affects all UI components

**Recommended Sequence**: US1 → US2 → US7 → US3 → US4 → US5 → US6

### Within Each User Story

- Backend models before services
- Services before API endpoints
- API endpoints before frontend API clients
- Frontend API clients before UI components
- Core UI before enhancements

### Parallel Opportunities

**Phase 1 (Setup)**: Tasks T004-T015 can run in parallel (different config files)

**Phase 2 (Foundational)**:
- T016-T020 (Database) can run in parallel with T021-T025 (Auth)
- T031-T032 (Shared types) can run in parallel with backend/frontend setup

**User Story 2 (Create/View Tasks)**:
- T051-T054 (Models + Schemas) can run in parallel
- T063-T074 (Frontend components) can run in parallel after T051-T062 complete

**User Story 7 (Reminders)**:
- T078-T081 (Models + Schemas) can run in parallel
- T096-T103 (Frontend components) can run in parallel after T078-T095 complete

**Phase 10 (Polish)**: Most tasks (T143-T166) can run in parallel

---

## Parallel Example: User Story 2

```bash
# Launch all models + schemas together:
T051: "Create Task SQLModel in backend/app/models/task.py"
T052: "Create Category SQLModel in backend/app/models/category.py"
T053: "Create Pydantic schemas for tasks in backend/app/schemas/task.py"
T054: "Create Pydantic schemas for categories in backend/app/schemas/category.py"

# After backend API complete, launch all frontend components together:
T063: "Create task API client methods in frontend/src/lib/api/tasks.ts"
T064: "Create category API client methods in frontend/src/lib/api/categories.ts"
T065: "Create Task TypeScript interface in frontend/src/types/task.ts"
T066: "Create Category TypeScript interface in frontend/src/types/category.ts"
T067: "Create Dashboard page in frontend/src/app/(auth)/dashboard/page.tsx"
T068: "Create TaskList component in frontend/src/components/features/tasks/TaskList.tsx"
T069: "Create TaskItem card component in frontend/src/components/features/tasks/TaskItem.tsx"
T070: "Create PriorityIndicator badge component"
T071: "Create CategoryBadge component"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 + 8)

1. Complete Phase 1: Setup → **Project structure ready**
2. Complete Phase 2: Foundational → **Auth + DB + API foundation ready**
3. Complete Phase 11: User Story 8 (Landing Page) → **Professional entry point live**
4. Complete Phase 3: User Story 1 (Auth) → **Users can register/login from landing page**
5. Complete Phase 4: User Story 2 (Create/View Tasks) → **Users can create rich tasks**
6. **STOP and VALIDATE**: Test US8 → US1 → US2 flow independently
7. Deploy/demo MVP with landing page + auth + task creation

**Note**: Landing page (US8) is developed first to establish brand identity and provide entry point before implementing auth flows.

### Incremental Delivery

1. **MVP**: US8 (Landing Page) + US1 (Auth) + US2 (Create/View) → Deploy → Get feedback
2. **V1.1**: Add US7 (Reminders) → Deploy → Get feedback on notifications
3. **V1.2**: Add US3 (Complete/Delete) → Deploy → Core task management complete
4. **V1.3**: Add US4 (Edit) → Deploy → Full CRUD functional
5. **V1.4**: Add US5 (Filter/Sort) + US6 (Responsive) → Deploy → Production-ready

### Parallel Team Strategy

With 3 developers:

1. **Together**: Complete Setup + Foundational (critical blocking work)
2. **Once Foundational done**:
   - **Developer A**: User Story 1 (Auth)
   - **Developer B**: User Story 2 (Create/View Tasks) - starts after US1 login works
   - **Developer C**: User Story 7 (Reminders) - can work on backend scheduler independently
3. **Integration**: Merge and test all stories together
4. **Continue in parallel**: US3/US4/US5/US6 can be split across team

---

## Notes

- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] label**: Maps task to specific user story for traceability (US1 = User Story 1, etc.)
- **Each user story**: Should be independently completable and testable
- **Commit strategy**: Commit after each task or logical group (e.g., all models for a story)
- **Stop at checkpoints**: Validate each story independently before proceeding
- **ADR references**: See history/adr/ for architectural decisions (ADR-001: Glassmorphism Styling, ADR-003 through ADR-006: Auth, Monorepo, Task Features, Notification Delivery)
- **Context7 MCP**: Must Use for Better Auth, Celery, Resend documentation during implementation

---

**Total Tasks**: 203 atomic, executable tasks
**User Stories**: 8 (US1-US8)
**MVP Scope**: US1 (Auth) + US2 (Create/View Tasks) + US8 (Landing Page) = ~110 tasks
**Estimated Effort**: MVP 2.5-3.5 weeks, Full feature set 5-7 weeks (single developer)
