# ADR-005: Rich Task Features with Priority, Categories, and Scheduling as MVP Baseline

> **Scope**: Clustered decision covering task data model complexity, including priority system, category management, habit scheduling, and narrative story field for Phase 2 MVP.

- **Status:** Accepted
- **Date:** 2025-12-28
- **Feature:** 001-ps2-fullstack-web-foundation
- **Context:** User explicitly requested professional task management with priority levels, user-created categories, recurring habit tracking (schedule days), and rich task narratives (story field). Decision required: include in Phase 2 MVP or defer to Phase 3+ to reduce scope.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Affects database schema, API design, UI complexity, future migration cost
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Basic CRUD only vs Priority only vs Full rich features
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Impacts data model, backend services, frontend components, testing
-->

## Decision

**Include Rich Task Features in Phase 2 MVP**

Feature set included:

- **Story Field**:
  - Markdown-supported narrative (max 2000 characters)
  - Optional field for detailed task context beyond title
  - Use case: Meeting notes, project context, subtask lists

- **Priority System**:
  - 4 levels: Low, Medium (default), High, Urgent
  - Color-coded UI indicators (Blue, Yellow, Orange, Red)
  - Filterable and sortable in task list
  - Indexed database column for query performance

- **Category Management**:
  - User-created categories (max 20 per user)
  - Name (1-50 chars) + Color (hex code)
  - On-the-fly creation in task form ("Add category" button)
  - Nullable foreign key (tasks can exist without category)

- **Habit Scheduling**:
  - `schedule` field: JSON array of day names (e.g., `["Monday", "Wednesday", "Friday"]`)
  - Mutually exclusive with `due_date` (one-time tasks use due_date, recurring habits use schedule)
  - Supports recurring habit tracking (e.g., "Exercise 3x/week")

- **Database Impact**:
  - Task table: +6 fields (story, priority, schedule, due_date, category_id, reminder fields)
  - Categories table: 3 fields (name, color, user_id)
  - Total: 5 tables (users, tasks, categories, notifications, notification_preferences)

## Consequences

### Positive

- **Professional-Grade UX**: Matches feature parity with Todoist, TickTick, Any.do (baseline expectations for task apps)
- **Differentiation**: Story field + habit scheduling distinguishes TaskFlow from basic todo apps
- **User Retention**: Priority and categories are frequently cited as essential features in user research
- **No Future Migration**: Avoiding this decision now would require painful schema migration + UI refactoring in Phase 3
- **Competitive Positioning**: Hackathon demo showcases professional product vs prototype
- **Minimal Complexity Addition**: 4 priority levels and 1 category table add ~20% data model complexity for 80% user value

### Negative

- **Increased Initial Scope**: Adds ~30% more implementation work vs basic task CRUD (estimated 3-4 extra days)
- **Additional UI Components Required**:
  - PriorityIndicator.tsx (badge with color coding)
  - CategorySelector.tsx (dropdown with on-the-fly creation)
  - CategoryManager.tsx (CRUD interface for categories)
  - ReminderSettings.tsx (reminder configuration)
  - ScheduleSelector.tsx (day checkboxes for habits)
- **Testing Complexity**: More edge cases (e.g., category deletion cascades, schedule validation, priority filtering)
- **Database Query Complexity**: Filtering by priority + category + due date requires compound indexes
- **Learning Curve**: Users must understand priority levels, category limits (20 max), schedule vs due_date distinction

## Alternatives Considered

**Alternative 1: Basic Task CRUD Only (Defer All Rich Features to Phase 3)**
- Approach: Phase 2 implements only title, completed status, created_at
- Pros: Faster MVP delivery (2 weeks vs 3 weeks), simpler data model, minimal testing
- Cons:
  - Poor hackathon demo (looks like prototype, not product)
  - Schema migration headache in Phase 3 (ALTER TABLE on production)
  - User feedback delayed (won't know if features are valued until Phase 3)
  - Competitive disadvantage (judges compare to existing todo apps)
- **Why Rejected**: Hackathon context favors feature-rich demo, migration cost unacceptable

**Alternative 2: Priority Only (Defer Categories and Scheduling)**
- Approach: Include 4-level priority system, defer categories and habits to Phase 3
- Pros: Balanced scope (adds priority without category overhead), simpler schema (no categories table)
- Cons:
  - User explicitly requested categories and scheduling (requirement misalignment)
  - Still requires schema migration in Phase 3 for categories (partial solution)
  - Habit tracking is core differentiator (deferring loses competitive edge)
- **Why Rejected**: User requirements explicitly included categories + scheduling, partial deferral doesn't solve migration problem

**Alternative 3: Tags Instead of Categories**
- Approach: Multi-select tags vs single-select category
- Pros: More flexible (tasks can have multiple tags), common pattern (GitHub, Gmail)
- Cons:
  - Increased complexity (many-to-many relationship, tag management UI)
  - Query performance cost (JOIN on task_tags table)
  - User confusion (when to use tag vs priority vs story)
- **Why Rejected**: Single category simpler for MVP, tags can be added in Phase 4+ if needed

## References

- Feature Spec: `specs/001-ps2-fullstack-web-foundation/spec.md` (User Story 2, FR-011 to FR-020, Assumptions #11-12)
- Implementation Plan: `specs/001-ps2-fullstack-web-foundation/plan.md` (Data Model Design - Task entity with priority, schedule, category_id)
- User Feedback: User explicitly requested "rich task tracking with priority, schedule, and categories" in planning phase
- Competitive Analysis: Todoist (priority P1-P4), TickTick (priorities + habits), Any.do (categories) all include these features
- Related ADRs: None (orthogonal to auth and infrastructure decisions)
- Phase 2 Requirements: phase2.md specifies "basic CRUD + at least 2 value-added features" - this satisfies requirement
