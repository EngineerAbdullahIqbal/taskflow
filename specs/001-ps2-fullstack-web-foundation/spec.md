# Feature Specification: Phase 2 Full-Stack Web Application Foundation

**Feature Branch**: `001-ps2-fullstack-web-foundation`
**Created**: 2025-12-28
**Status**: Draft
**Input**: User description: "write a stong foundational specs using @phase2-spec-generator skill that meet al our @phase2.md requiremnts and create a Strong Foundation for making a Complete Full stack Todo Evaluaion TaskFlow as an Product."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration and Secure Login (Priority: P1)

As a new user, I want to create a personal account and securely sign in so that I can manage my tasks privately and access them from any device.

**Why this priority**: Authentication is the foundation for multi-user functionality and data isolation. Without it, no other features can function properly in a multi-user environment.

**Independent Test**: Can be fully tested by creating a new account with email/password, logging out, and logging back in. Delivers immediate value by allowing users to create their identity in the system.

**Acceptance Scenarios**:

1. **Given** I am a new user on the signup page, **When** I enter valid email, password, and name, **Then** my account is created and I am redirected to the dashboard
2. **Given** I have an existing account, **When** I enter correct email and password on login page, **Then** I am authenticated and redirected to my dashboard
3. **Given** I am logged in, **When** I click logout, **Then** I am signed out and redirected to login page
4. **Given** I try to signup with an existing email, **When** I submit the form, **Then** I see an error message indicating email already exists
5. **Given** I enter an invalid password on login, **When** I submit the form, **Then** I see an error message and remain on login page
6. **Given** I try to access protected pages without logging in, **When** I navigate to dashboard or tasks page, **Then** I am redirected to login page

---

### User Story 2 - Create and View Rich Tasks/Habits (Priority: P1)

As a logged-in user, I want to create detailed tasks or habits with titles, stories, priorities, scheduled days, and categories so that I can comprehensively track and organize my to-do items and recurring habits.

**Why this priority**: Rich task creation with priority, scheduling, and categorization is essential for a professional task management and habit tracking application. Users need these fields to properly organize and prioritize their work from day one.

**Independent Test**: Can be tested by logging in, creating a task with title "Morning Workout", story/description "30-min cardio session", priority "High", scheduled for "Monday, Wednesday, Friday", category "Health & Fitness", and seeing it appear in the task list with all attributes. Delivers standalone value as a comprehensive task/habit tracker.

**Acceptance Scenarios**:

1. **Given** I am on the dashboard, **When** I click "New Task/Habit" and enter a title, **Then** the task is created and appears in my task list
2. **Given** I am creating a task, **When** I add a story/description (optional narrative about the task), **Then** the story is saved with the task
3. **Given** I am creating a task, **When** I select a priority level (Low, Medium, High, Urgent), **Then** the priority is saved and displayed with visual indicators (colors/icons)
4. **Given** I am creating a task, **When** I schedule it for specific days of the week (for habits) or set a due date (for one-time tasks), **Then** the schedule is saved and task appears on those days
5. **Given** I am creating a task, **When** I assign it to a category (or create a new category on-the-fly), **Then** the task is associated with that category and displays with category badge/color
6. **Given** I have created multiple tasks with different priorities and categories, **When** I view my dashboard, **Then** I see all tasks with title, priority indicator, category badge, schedule, completion status, and creation date
7. **Given** I am creating a task, **When** I try to submit without a title, **Then** I see a validation error (title is the only required field)
8. **Given** I have tasks, **When** another user logs in, **Then** they only see their own tasks and categories (data isolation)

---

### User Story 3 - Mark Tasks Complete and Delete Tasks (Priority: P2)

As a user managing my task list, I want to mark tasks as complete when I finish them and delete tasks I no longer need so that I can maintain an organized task list.

**Why this priority**: Completion and deletion are essential for task lifecycle management but can wait until basic create/view works. Still critical for user experience.

**Independent Test**: Can be tested by creating a task, marking it complete (strikethrough or visual indicator), and then deleting it. Delivers value as task cleanup functionality.

**Acceptance Scenarios**:

1. **Given** I have an incomplete task, **When** I click the complete toggle, **Then** the task is marked as complete with visual indication (strikethrough/check)
2. **Given** I have a completed task, **When** I click the complete toggle again, **Then** the task is marked as incomplete
3. **Given** I have a task, **When** I click the delete button and confirm, **Then** the task is permanently removed from my list
4. **Given** I have tasks, **When** I mark some complete and some incomplete, **Then** I can see both states clearly distinguished

---

### User Story 4 - Update Task Details (Priority: P2)

As a user reviewing my tasks, I want to edit task titles, stories, priorities, schedules, and categories so that I can update information as my needs change.

**Why this priority**: Edit functionality enhances usability but is not required for minimum viability. Users can delete and recreate tasks if needed initially. However, with rich task fields, editing becomes more valuable.

**Independent Test**: Can be tested by creating a task with title "Morning Run", priority "Medium", category "Fitness", then editing it to "Morning Workout", priority "High", story "30-min cardio + stretching", and seeing all updates reflected. Delivers value as a comprehensive content update capability.

**Acceptance Scenarios**:

1. **Given** I have an existing task, **When** I click edit and change the title, **Then** the updated title is saved and displayed
2. **Given** I am editing a task, **When** I update the story/description, **Then** the new story is saved
3. **Given** I am editing a task, **When** I change the priority level from "Medium" to "High", **Then** the new priority is saved and visual indicator updates
4. **Given** I am editing a task, **When** I modify the schedule from "Monday, Wednesday" to "Monday, Wednesday, Friday", **Then** the new schedule is saved
5. **Given** I am editing a task, **When** I change the category assignment or create a new category during edit, **Then** the task is reassigned to the new category
6. **Given** I am editing a task, **When** I clear the title field, **Then** I see a validation error (title required)
7. **Given** I am editing a task, **When** I click cancel, **Then** my changes are discarded and original task data is preserved

---

### User Story 5 - Filter and Sort Tasks (Priority: P3)

As a user with many tasks, I want to filter tasks by status, priority, and category, and sort by creation date, due date, priority, or title so that I can quickly find and organize relevant tasks.

**Why this priority**: Advanced filtering and sorting improve usability for power users but are not essential for initial launch. Users can manually scan their lists initially. However, with rich task fields (priority, category, schedule), filtering becomes more valuable.

**Independent Test**: Can be tested by creating 10 tasks with varying completion states, priorities ("High", "Medium", "Low"), and categories ("Work", "Personal"), then filtering to show only "High" priority "Work" tasks and sorting by due date. Delivers value as a comprehensive productivity enhancement.

**Acceptance Scenarios**:

1. **Given** I have both pending and completed tasks, **When** I select "Pending" filter, **Then** I see only incomplete tasks
2. **Given** I have tasks, **When** I select "Completed" filter, **Then** I see only completed tasks
3. **Given** I have tasks with different priorities, **When** I select "High Priority" filter, **Then** I see only high-priority tasks
4. **Given** I have tasks with different priorities, **When** I select "Urgent Priority" filter, **Then** I see only urgent-priority tasks
5. **Given** I have tasks in multiple categories, **When** I select a specific category filter (e.g., "Work"), **Then** I see only tasks in that category
6. **Given** I have tasks, **When** I select "Uncategorized" filter, **Then** I see only tasks with no category assigned
7. **Given** I have multiple tasks, **When** I sort by "Newest First", **Then** tasks are ordered by creation date descending
8. **Given** I have multiple tasks, **When** I sort by "Due Date", **Then** tasks are ordered by due date ascending (soonest first)
9. **Given** I have multiple tasks, **When** I sort by "Priority", **Then** tasks are ordered by priority level (Urgent → High → Medium → Low)
10. **Given** I have multiple tasks, **When** I sort by "Title A-Z", **Then** tasks are ordered alphabetically by title
11. **Given** I apply multiple filters (status + priority + category) and sort, **When** I create a new task, **Then** the list updates to reflect new task with current filter/sort settings

---

### User Story 6 - Responsive Mobile Access (Priority: P3)

As a user accessing the application from various devices, I want the interface to work seamlessly on mobile phones, tablets, and desktops so that I can manage tasks wherever I am.

**Why this priority**: Responsive design enhances accessibility but desktop-first approach allows initial launch. Mobile optimization can be iterated post-launch.

**Independent Test**: Can be tested by accessing the application on a mobile browser (375px width) and performing all core actions (login, create task, mark complete, delete). Delivers value as mobile accessibility.

**Acceptance Scenarios**:

1. **Given** I access the app on a mobile device (< 640px width), **When** I view the task list, **Then** tasks stack vertically and are fully readable
2. **Given** I am on a tablet (640px - 1024px), **When** I navigate the interface, **Then** all buttons and forms are touch-friendly (minimum 44px tap targets)
3. **Given** I am on desktop (> 1024px), **When** I view the dashboard, **Then** I see an optimized layout with sidebar navigation
4. **Given** I resize my browser window, **When** I change from mobile to desktop width, **Then** the layout adapts without breaking

---

### User Story 7 - Task Reminders with Email and Browser Notifications (Priority: P2)

As a user managing tasks with schedules or due dates, I want to set reminders that notify me via email and browser notifications so that I never miss important tasks and can stay on top of my commitments.

**Why this priority**: Reminders are essential for task management effectiveness. Without reminders, users may forget scheduled tasks, reducing the app's value. This is a priority P2 feature because it enhances the core task management experience but the app is still functional without it (users can manually check their tasks).

**Independent Test**: Can be tested by creating a task with a due date, setting a reminder for 5 minutes before due time, selecting email notification option with a specific email address, and verifying that both a browser notification appears and an email is received at the exact reminder time. Delivers standalone value as a proactive task management feature.

**Acceptance Scenarios**:

1. **Given** I am creating or editing a task with a due date or schedule, **When** I enable reminders, **Then** I see options to set reminder timing (e.g., "5 minutes before", "1 hour before", "1 day before", "at exact time")
2. **Given** I enable reminders for a task, **When** I select "Browser Notification" option, **Then** the system requests browser notification permission (if not already granted)
3. **Given** I enable reminders for a task, **When** I select "Email Notification" option, **Then** I see a field to enter or select the email address where I want to receive reminders
4. **Given** I enter a new email address for reminders, **When** I save the task, **Then** the email address is saved to my notification preferences and can be reused for future reminders
5. **Given** I have a task with a reminder set, **When** the reminder time arrives, **Then** I receive a browser notification (if enabled) displaying the task title, description, and a link to view the task
6. **Given** I have a task with an email reminder set, **When** the reminder time arrives, **Then** I receive an email at the specified address with the task title, description, due date, and a link to the dashboard
7. **Given** I am logged into the dashboard, **When** I click the bell icon in the top bar, **Then** I see a notification center showing recent browser notifications and unread reminder notifications
8. **Given** I receive a browser notification, **When** I click on it, **Then** I am navigated to the task detail page for that task
9. **Given** I have multiple tasks with reminders, **When** reminder times arrive, **Then** notifications are sent independently for each task at their respective reminder times
10. **Given** I complete a task with pending reminders, **When** the task is marked complete, **Then** future reminders for that task are automatically canceled
11. **Given** I delete a task with pending reminders, **When** the task is deleted, **Then** all associated reminders are removed from the system
12. **Given** I have not granted browser notification permission, **When** a reminder time arrives, **Then** the notification appears only in the in-app notification center (bell icon) and is sent via email if configured

---

### User Story 8 - High-Conversion Landing Page (Priority: P1)

As a visitor to the Task-Flow website, I want to see a modern, attractive, and fast landing page that clearly explains the app's value so that I am motivated to sign up and start managing my tasks.

**Why this priority**: The landing page is the first point of contact for new users. A professional and engaging entry point is critical for user acquisition and building trust in the product.

**Independent Test**: Access the root URL (`/`), verify the hero section loads in < 2s, explore the bento grid feature showcase, and click the "Get Started" CTA to navigate to signup.

**Acceptance Scenarios**:

1. **Given** I am a visitor on the landing page, **When** the page loads, **Then** I see a high-conversion hero section with glassmorphism design and smooth motion animations (via `apply-motion-magic`)
2. **Given** I scroll down the landing page, **When** I reach the feature section, **Then** I see a Bento grid layout (via `scaffold-landing-page`) showcasing core features with staggered entry animations
3. **Given** I am on a mobile device, **When** I view the landing page, **Then** the layout adapts seamlessly (responsive design) and performance remains fast (< 2s load)
4. **Given** I am interested in the app, **When** I click the "Get Started" button, **Then** I am navigated directly to the signup page
5. **Given** I am using a screen reader, **When** I navigate the landing page, **Then** all sections and CTAs are properly labeled and accessible (WCAG 2.1 AA)

---

### Edge Cases

- What happens when a user tries to create a task with a title exceeding 200 characters? (System truncates or shows validation error)
- How does the system handle simultaneous edits from multiple browser tabs? (Last write wins with timestamp conflict detection)
- What happens when a user's session expires while they're creating a task? (Draft is lost unless auto-save implemented; user redirected to login)
- How does the system behave when the database connection is lost? (Show user-friendly error message, retry logic, cache operations locally)
- What happens when a user tries to delete a task that was already deleted by another session? (404 Not Found, gracefully remove from UI)
- How are tasks displayed when a user has hundreds or thousands of tasks? (Pagination with 20 tasks per page, or infinite scroll)

## Requirements *(mandatory)*

### Functional Requirements

#### Authentication & Authorization
- **FR-001**: System MUST allow users to create accounts with email and password
- **FR-002**: System MUST validate email format (standard email regex) and enforce unique email addresses
- **FR-003**: System MUST enforce password strength requirements (minimum 8 characters, uppercase, lowercase, number, special character)
- **FR-004**: System MUST securely hash passwords using bcrypt with cost factor 12 before storage
- **FR-005**: System MUST issue JWT tokens upon successful login with 15-minute expiration for access tokens
- **FR-006**: System MUST provide refresh tokens with 7-day expiration for "remember me" functionality
- **FR-007**: System MUST verify JWT tokens on every API request and reject requests with invalid/expired tokens (401 Unauthorized)
- **FR-008**: System MUST ensure users can only access their own tasks (ownership verification on all operations)
- **FR-009**: System MUST rate-limit login attempts (maximum 5 failed attempts per 15 minutes per email)
- **FR-010**: System MUST destroy sessions on logout (invalidate tokens)

#### Task CRUD Operations
- **FR-011**: System MUST allow authenticated users to create tasks with a required title (1-200 characters)
- **FR-012**: System MUST allow users to add optional story/description to tasks (maximum 2000 characters, markdown formatting supported)
- **FR-013**: System MUST allow users to assign priority level to tasks (Low, Medium, High, Urgent) with default "Medium" if not specified
- **FR-014**: System MUST allow users to schedule tasks for specific days of week (recurring habits) or set a single due date (one-time tasks)
- **FR-015**: System MUST allow users to assign tasks to categories with on-the-fly category creation during task creation
- **FR-016**: System MUST associate each task with the creating user's ID (foreign key relationship)
- **FR-017**: System MUST allow users to retrieve all their tasks (paginated, 20 per page)
- **FR-018**: System MUST allow users to retrieve a single task by ID (ownership verified)
- **FR-019**: System MUST allow users to update task title, story, priority, schedule, and category assignment
- **FR-020**: System MUST allow users to toggle task completion status (boolean)
- **FR-021**: System MUST allow users to permanently delete tasks
- **FR-022**: System MUST automatically timestamp tasks on creation and update (created_at, updated_at)
- **FR-023**: System MUST validate title is not empty and does not exceed 200 characters
- **FR-024**: System MUST display tasks with visual priority indicators (color coding or icons: Low=blue, Medium=yellow, High=orange, Urgent=red)

#### Category Management
- **FR-025**: System MUST allow users to create custom categories with name (1-50 characters) and color (hex code)
- **FR-026**: System MUST enforce unique category names per user (case-insensitive)
- **FR-027**: System MUST limit users to a maximum of 20 categories
- **FR-028**: System MUST allow users to edit category name and color
- **FR-029**: System MUST allow users to delete categories (tasks with deleted category have category reference set to null)
- **FR-030**: System MUST display category badges with name and color on task cards

#### Notification & Reminders
- **FR-031**: System MUST allow users to set reminders for tasks with due dates or schedules
- **FR-032**: System MUST support reminder timing options: "5 minutes before", "15 minutes before", "1 hour before", "1 day before", "at exact time"
- **FR-033**: System MUST support two notification channels: browser notifications and email notifications
- **FR-034**: System MUST request browser notification permission when user enables browser notifications for the first time
- **FR-035**: System MUST allow users to specify email addresses for reminder notifications (saved to user notification preferences)
- **FR-036**: System MUST send browser notifications at the exact reminder time displaying task title, story preview, and clickable link to task detail
- **FR-037**: System MUST send email notifications at the exact reminder time with task title, full story, due date, and link to dashboard
- **FR-038**: System MUST provide a notification center UI (bell icon in top bar) showing recent browser notifications and unread reminders
- **FR-039**: System MUST automatically cancel pending reminders when a task is marked as completed
- **FR-040**: System MUST automatically delete all reminders when a task is deleted
- **FR-041**: System MUST send reminders independently for each task at their respective scheduled times
- **FR-042**: System MUST fall back to in-app notification center if browser notification permission is denied
- **FR-043**: System MUST track notification read/unread status and display unread count on bell icon

#### Filtering & Sorting
- **FR-044**: System MUST support filtering tasks by status: "all", "pending" (completed=false), "completed" (completed=true)
- **FR-045**: System MUST support filtering tasks by priority: "all", "low", "medium", "high", "urgent"
- **FR-046**: System MUST support filtering tasks by category (show tasks in selected category or "uncategorized")
- **FR-047**: System MUST support sorting tasks by: creation date (newest/oldest first), due date, priority level, title (A-Z/Z-A), category
- **FR-048**: System MUST apply filter and sort parameters via query string (e.g., ?status=pending&priority=high&category=work&sort=created_desc)
- **FR-049**: System MUST preserve filter/sort preferences during session (URL state management)

#### Data Persistence
- **FR-050**: System MUST store all user, task, category, and notification data in Neon Serverless PostgreSQL database
- **FR-051**: System MUST ensure data persistence across application restarts
- **FR-052**: System MUST maintain database indexes on frequently queried columns (user_id, completed, created_at, priority, category_id, due_date, reminder_time)
- **FR-053**: System MUST handle database migration scripts for schema changes

#### API Endpoints
- **FR-054**: System MUST provide RESTful API endpoint GET /api/tasks (list all user tasks with query params for filtering/sorting)
- **FR-055**: System MUST provide RESTful API endpoint POST /api/tasks (create new task with title, story, priority, schedule, category, reminders)
- **FR-056**: System MUST provide RESTful API endpoint GET /api/tasks/{id} (get task by ID)
- **FR-057**: System MUST provide RESTful API endpoint PUT /api/tasks/{id} (update task including reminder settings)
- **FR-058**: System MUST provide RESTful API endpoint DELETE /api/tasks/{id} (delete task)
- **FR-059**: System MUST provide RESTful API endpoint PATCH /api/tasks/{id}/complete (toggle completion)
- **FR-060**: System MUST provide RESTful API endpoint GET /api/categories (list all user categories)
- **FR-061**: System MUST provide RESTful API endpoint POST /api/categories (create new category)
- **FR-062**: System MUST provide RESTful API endpoint PUT /api/categories/{id} (update category)
- **FR-063**: System MUST provide RESTful API endpoint DELETE /api/categories/{id} (delete category)
- **FR-064**: System MUST provide RESTful API endpoint GET /api/notifications (list user notifications for notification center)
- **FR-065**: System MUST provide RESTful API endpoint PATCH /api/notifications/{id}/read (mark notification as read)
- **FR-066**: System MUST provide RESTful API endpoint GET /api/user/notification-preferences (get user email notification settings)
- **FR-067**: System MUST provide RESTful API endpoint PUT /api/user/notification-preferences (update user email notification settings)
- **FR-068**: All API endpoints MUST require valid JWT token in Authorization header (Bearer scheme)
- **FR-069**: API MUST return proper HTTP status codes (200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 404 Not Found, 409 Conflict, 500 Internal Server Error)
- **FR-070**: API MUST return error responses in standardized JSON format: `{"detail": "Error message", "error_code": "ERROR_CODE"}`

#### User Interface
- **FR-071**: System MUST provide responsive web interface that adapts to mobile (< 640px), tablet (640px-1024px), and desktop (> 1024px)
- **FR-072**: UI MUST provide signup page with email, password, and name fields
- **FR-073**: UI MUST provide login page with email and password fields
- **FR-074**: UI MUST provide dashboard/task list page showing all user tasks with priority indicators and category badges
- **FR-075**: UI MUST provide task creation form with title (required), story, priority selector, schedule/due date picker, category selector, and reminder configuration
- **FR-076**: UI MUST provide task edit interface (inline or modal) allowing updates to all task fields including reminders
- **FR-077**: UI MUST provide category management interface (create, edit, delete categories)
- **FR-078**: UI MUST provide notification center (bell icon in top bar) showing recent notifications and unread count
- **FR-079**: UI MUST visually distinguish completed tasks from pending tasks (strikethrough, checkmark, or color)
- **FR-080**: UI MUST provide delete confirmation before permanently removing tasks or categories
- **FR-081**: UI MUST show loading states during async operations (spinners, skeletons)
- **FR-082**: UI MUST display user-friendly error messages for validation failures and server errors
- **FR-083**: UI MUST meet WCAG 2.1 AA accessibility standards (keyboard navigation, screen reader support, color contrast ≥4.5:1)

#### Landing Page & Brand Identity
- **FR-089**: System MUST provide a high-conversion landing page at the root URL (/) featuring Task-Flow value proposition
- **FR-090**: Landing page MUST utilize a Bento grid layout for showcasing features (tasks, habits, categories, reminders)
- **FR-091**: Landing page MUST implement glassmorphism design aesthetic (backdrop-blur, translucent borders, subtle gradients)
- **FR-092**: Landing page MUST feature staggered entry animations and scroll-triggered motion effects using Framer Motion
- **FR-093**: System MUST implement SEO metadata (title, description, Open Graph tags) for the landing page to improve search visibility
- **FR-094**: Landing page MUST include a clear "Get Started" call-to-action leading to user registration

#### Performance & Reliability
- **FR-084**: System MUST load initial page in under 2 seconds on standard broadband connection
- **FR-085**: System MUST complete API requests in under 300ms for CRUD operations (p95 latency)
- **FR-086**: System MUST achieve Lighthouse performance score ≥90
- **FR-087**: System MUST handle at least 100 concurrent users without degradation
- **FR-088**: System MUST process and send reminders within 30 seconds of scheduled reminder time (allowing for job scheduler delay)

### Key Entities

- **User**: Represents a registered user account with unique email, name, password hash, and creation timestamp. Each user owns zero or more tasks and zero or more categories. Managed partially by Better Auth (authentication session) and partially by application (user profile data).

- **Task**: Represents a to-do item or recurring habit belonging to a specific user. Contains:
  - title (required, 1-200 characters)
  - story/description (optional, max 2000 characters, markdown supported)
  - priority (enum: Low, Medium, High, Urgent; default: Medium)
  - schedule (array of day names for recurring habits, e.g., ["Monday", "Wednesday", "Friday"])
  - due_date (single date for one-time tasks, mutually exclusive with schedule)
  - category_id (foreign key to Category, nullable)
  - reminder_enabled (boolean, default: false)
  - reminder_timing (enum: 5min_before, 15min_before, 1hour_before, 1day_before, at_time; nullable)
  - reminder_channels (JSON array: ["browser", "email"])
  - completed (boolean, default: false)
  - timestamps (created_at, updated_at)
  - user_id (foreign key to User)
  Each task belongs to exactly one user and optionally one category.

- **Category**: Represents a user-created task category with name and color. Contains:
  - name (1-50 characters, unique per user, case-insensitive)
  - color (hex code, e.g., "#3B82F6")
  - user_id (foreign key to User)
  - timestamps (created_at, updated_at)
  Each category belongs to one user and can be assigned to zero or more tasks. Maximum 20 categories per user.

- **Notification**: Represents an in-app notification for the notification center. Contains:
  - user_id (foreign key to User)
  - task_id (foreign key to Task, nullable if task deleted)
  - type (enum: reminder, system)
  - title (notification title)
  - message (notification body)
  - read (boolean, default: false)
  - clicked (boolean, default: false)
  - timestamps (created_at)
  Each notification belongs to one user. Notifications are retained for 30 days, then auto-deleted.

- **NotificationPreference**: Represents user's email notification settings. Contains:
  - user_id (foreign key to User, unique)
  - reminder_email (email address for reminders, defaults to user's account email)
  - email_notifications_enabled (boolean, default: true)
  - browser_notifications_enabled (boolean, default: false)
  - timestamps (created_at, updated_at)
  One preference record per user.

- **Session**: Represents an authenticated user session managed via JWT tokens. Contains user ID, email, expiration time, and token type (access/refresh). Not explicitly stored in database (stateless JWT approach).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete account creation and first task creation in under 3 minutes
- **SC-002**: Users can successfully log in and access their tasks within 5 seconds of entering credentials
- **SC-003**: System supports 100 concurrent users performing CRUD operations without response time degradation (maintains <300ms p95 latency)
- **SC-004**: 95% of task creation requests complete successfully on first attempt
- **SC-005**: Users can access and perform all core functions (login, create, view, edit, delete, complete tasks) on mobile devices (375px width) without horizontal scrolling
- **SC-006**: Initial page load (dashboard) completes in under 2 seconds on 3G connection
- **SC-007**: Zero unauthorized access incidents (users can only see/modify their own tasks)
- **SC-008**: Application achieves 99% uptime during evaluation period
- **SC-009**: Lighthouse performance score ≥90, accessibility score ≥90
- **SC-010**: All core workflows (signup, login, create task, mark complete, delete) have ≥85% test coverage

### User Satisfaction Metrics

- **SC-011**: 90% of users successfully complete primary task (create and manage at least one task) on first session
- **SC-012**: Users report intuitive navigation (no more than 2 clicks to reach any core function)
- **SC-013**: Error messages are clear and actionable (users understand what went wrong and how to fix it)

## Assumptions

1. **Authentication Method**: Using Better Auth with JWT tokens (as specified in phase2.md). Shared secret between frontend and backend for token verification.

2. **Database Schema**:
   - **Tasks table**: user_id (foreign key), title (varchar 200), story (text), priority (enum: low/medium/high/urgent, default: medium), schedule (JSON array of day names or null), due_date (date or null), category_id (foreign key to categories, nullable), completed (boolean, default: false), created_at (timestamp), updated_at (timestamp)
   - **Categories table**: id (primary key), user_id (foreign key), name (varchar 50, unique per user), color (varchar 7 for hex code), created_at (timestamp), updated_at (timestamp)
   - **Users table**: Managed by Better Auth with id (primary key), email (unique), name, password_hash
   - **Note**: schedule and due_date are mutually exclusive (one task has either schedule array OR due_date, not both)

3. **Session Duration**: Access tokens expire in 15 minutes, refresh tokens in 7 days (standard JWT practice). Users remain logged in via refresh token unless they explicitly log out.

4. **Pagination**: Task list uses offset-based pagination with 20 tasks per page (standard for moderate data volumes). Infinite scroll or cursor-based pagination can be considered post-launch.

5. **Deployment**: Frontend deployed on Vercel (Next.js optimized), backend deployed on compatible Python hosting (Render/Railway), database on Neon Serverless PostgreSQL.

6. **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge - latest 2 versions). No IE11 support.

7. **Offline Support**: Not required for Phase 2. Application requires active internet connection. Progressive Web App (PWA) features deferred to Phase 3.

8. **Email Verification**: Email verification not required for Phase 2. Users can log in immediately after signup. Verification can be added in Phase 3.

9. **Password Reset**: Password reset functionality not required for Phase 2 (out of scope per phase2.md). Users contact support if locked out.

10. **Data Retention**: User data retained indefinitely unless user deletes account. No automatic data purging. GDPR/privacy features deferred to production release.

11. **Priority Visual Indicators**: Low=blue (#3B82F6), Medium=yellow (#EAB308), High=orange (#F97316), Urgent=red (#EF4444) for consistent UI representation.

12. **Category Limits**: Maximum 20 categories per user to prevent database bloat and maintain performance. This is a reasonable limit for personal task management.

13. **Schedule Format**: For recurring habits, schedule stored as JSON array of day names (e.g., ["Monday", "Wednesday", "Friday"]). For one-time tasks, use due_date field instead. UI provides clear distinction between recurring and one-time tasks.

14. **Reminder Processing**: Background job scheduler (e.g., Celery, APScheduler, or serverless cron) checks for pending reminders every minute and sends notifications within 30 seconds of scheduled time.

15. **Email Service**: Using Resend or SendGrid for transactional email delivery. Email templates use HTML with plain text fallback.

16. **Browser Notifications**: Using Web Push API for browser notifications. Requires user permission grant. Notifications expire after 24 hours if not clicked.

17. **Notification Retention**: In-app notifications (notification center) retained for 30 days, then auto-deleted to prevent database bloat. Users can manually dismiss notifications.

18. **Default Notification Email**: If user does not specify a reminder email, system uses the user's account email address from the users table.

## Out of Scope

The following features are explicitly **not** included in Phase 2:

- Social login (Google, GitHub OAuth)
- Email verification workflow
- Password reset/forgot password
- Two-factor authentication (2FA)
- Collaborative tasks (shared with other users)
- Task comments or activity history
- File attachments to tasks
- Dark mode theme
- Push notifications (mobile app notifications)
- SMS/text message notifications
- Search functionality (full-text search)
- Bulk operations (multi-select, bulk delete)
- Task export (CSV, JSON)
- User profile editing (change email, password)
- Account deletion
- Admin dashboard or user management
- Analytics or usage tracking (beyond basic logging)
- Offline/PWA support
- Real-time collaboration (WebSockets)
- Recurring task instances (e.g., creating separate task per scheduled day)
- Task dependencies or subtasks
- Custom reminder frequencies (e.g., "every 2 hours")
- Notification digest emails (daily summary)
- AI chatbot integration (reserved for Phase 3)

## Dependencies

- **External Services**:
  - Neon Serverless PostgreSQL (database hosting)
  - Vercel (frontend deployment)
  - Python hosting service (Render, Railway, or similar for backend)

- **Authentication**:
  - Better Auth library (frontend session management)
  - JWT verification shared between Next.js and FastAPI

- **Third-Party Libraries** (to be verified via Context7 MCP during implementation):
  - Next.js 16+ (App Router)
  - FastAPI (Python backend framework)
  - SQLModel (Python ORM)
  - shadcn/ui (UI component library)
  - Tailwind CSS (styling)
  - bcrypt (password hashing)

## Security Considerations

- **Password Security**: Passwords hashed with bcrypt (cost factor 12), never stored in plaintext, never logged, never returned in API responses
- **JWT Tokens**: Signed with HS256 algorithm using shared secret from environment variable (BETTER_AUTH_SECRET), tokens expire automatically
- **Rate Limiting**: Login endpoint limited to 5 attempts per 15 minutes per email to prevent brute-force attacks
- **Data Isolation**: All database queries filtered by authenticated user_id to prevent unauthorized access
- **Input Validation**: All user inputs validated on both client and server (title length, email format, password strength)
- **HTTPS**: All production traffic served over HTTPS (enforced by Vercel and backend hosting)
- **CORS**: Backend configured to only accept requests from frontend origin
- **SQL Injection**: Prevented via SQLModel parameterized queries (ORM-based access)
- **XSS Prevention**: User-generated content (titles, descriptions) sanitized before rendering
- **CSRF Protection**: Not required for JWT-based stateless API (no cookies for auth)

## Deployment Requirements

- **Frontend**: Deployed on Vercel with production environment variables (API base URL, Better Auth secret)
- **Backend**: Deployed with public API URL, environment variables for database connection and JWT secret
- **Database**: Neon Serverless PostgreSQL instance with connection pooling enabled
- **Environment Variables**:
  - Frontend: `NEXT_PUBLIC_API_URL`, `BETTER_AUTH_SECRET`
  - Backend: `DATABASE_URL`, `BETTER_AUTH_SECRET`, `CORS_ORIGINS`
- **Health Checks**: API provides `/health` endpoint for uptime monitoring
- **Database Migrations**: Alembic migration scripts for schema changes, tested in staging before production
- **Rollback Plan**: Git-based rollback for frontend/backend, database migration rollback scripts

## Deliverables

1. **Public GitHub Repository** with:
   - Monorepo structure (frontend/, backend/ directories)
   - /specs folder with organized specifications
   - CLAUDE.md files at root and in each service
   - README.md with setup instructions
   - Database migration scripts
   - All source code and configuration

2. **Deployed Application**:
   - Frontend live on Vercel (public URL)
   - Backend API accessible via public URL
   - Working authentication system (signup, login, logout)
   - All CRUD operations functional
   - Responsive UI working on mobile, tablet, desktop

3. **Demo Video**: Under 90 seconds demonstrating:
   - User signup
   - Login
   - Create task
   - Mark task complete
   - Edit task
   - Delete task
   - Filter/sort tasks
   - Responsive design (mobile view)

4. **Submission Form**: Completed at https://forms.gle/KMKEKaFUD6ZX4UtY8 with:
   - GitHub repo link
   - Vercel app URL
   - Backend API URL
   - Demo video link
   - WhatsApp number (for live presentation invitation)

## Acceptance Criteria Summary

This feature is considered **complete** and **ready for production** when:

✅ All P1 user stories (Authentication, Create/View Rich Tasks/Habits) are fully functional
✅ All P2 user stories (Complete/Delete, Edit Task Details including priority/schedule/category, Task Reminders with Email/Browser Notifications) are fully functional
✅ All P3 user stories (Filter/Sort with priority and category, Responsive) are implemented
✅ All functional requirements (FR-001 through FR-088) are met
✅ All success criteria (SC-001 through SC-013) are achieved
✅ Category management (create, edit, delete, assign to tasks) is fully functional
✅ Reminder system (browser notifications, email notifications, notification center) is fully functional
✅ Application is deployed and accessible via public URLs
✅ Test coverage ≥85% for all core workflows including notification delivery
✅ Lighthouse scores ≥90 (performance and accessibility)
✅ Security audit shows no critical vulnerabilities
✅ Demo video successfully demonstrates all core features including rich task creation with priority, schedule, category, and reminders
✅ Submission form completed with all required information

---

**Next Steps**:
1. Run `/sp.clarify` if any requirements need clarification
2. Run `/sp.plan` to generate detailed implementation plan
3. Run `/sp.tasks` to break plan into actionable tasks
4. Begin implementation following Spec-Driven Development workflow
