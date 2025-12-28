# Feature Specification: TaskFlow Console Application

**Feature Branch**: `phase-1-console`
**Created**: 2025-12-27
**Status**: Draft
**Input**: Phase 1 requirements - In-memory console-based todo application with 5 core CRUD operations

## Overview

TaskFlow Phase 1 is a command-line todo application that enables users to manage tasks through an interactive menu-driven interface. The application stores all tasks in memory during the session, providing a simple yet complete task management experience.

**Target Users**: Developers and users comfortable with command-line interfaces who need a lightweight task management tool.

**Core Value Proposition**: Quick, distraction-free task management without the overhead of databases, accounts, or complex setup.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add New Task (Priority: P1)

As a user, I want to add a new task with a title and optional description, so I can capture what I need to do.

**Why this priority**: Adding tasks is the foundational capability - without it, no other features have meaning. This is the entry point for all task management.

**Independent Test**: Can be fully tested by launching the app, selecting "Add Task", entering task details, and verifying confirmation message. Delivers immediate value by allowing users to capture tasks.

**Acceptance Scenarios**:

1. **Given** the application is running and showing the main menu, **When** I select option 1 (Add Task), **Then** I am prompted to enter a task title.

2. **Given** I am in the Add Task flow, **When** I enter a title "Buy groceries", **Then** I am prompted to enter an optional description.

3. **Given** I have entered a title, **When** I enter a description "Milk, eggs, bread" and confirm, **Then** the system displays "Task added with ID: [number]" and returns to the main menu.

4. **Given** I have entered a title, **When** I press Enter without typing a description, **Then** the task is created with an empty description and confirmation is shown.

5. **Given** I am prompted for a title, **When** I enter an empty string or only whitespace, **Then** the system displays an error "Title cannot be empty" and prompts again.

---

### User Story 2 - View All Tasks (Priority: P1)

As a user, I want to see all my tasks with their status, so I can understand what needs to be done.

**Why this priority**: Viewing tasks is essential for understanding current workload. Without visibility, users cannot make decisions about what to work on.

**Independent Test**: Can be tested by adding 2-3 tasks via Add Task, then selecting View Tasks to verify all appear with correct formatting. Delivers value by providing overview of all captured work.

**Acceptance Scenarios**:

1. **Given** there are no tasks, **When** I select option 2 (View Tasks), **Then** the system displays "No tasks found." and returns to the main menu.

2. **Given** there are 3 tasks (2 pending, 1 completed), **When** I select View Tasks, **Then** all tasks are displayed with their ID, status indicator, and title.

3. **Given** tasks exist, **When** viewing the task list, **Then** pending tasks show "[ ]" and completed tasks show "[✓]" before the title.

4. **Given** tasks exist, **When** viewing the task list, **Then** tasks are displayed in the format: "[status] ID. Title" (e.g., "[ ] 1. Buy groceries").

---

### User Story 3 - Mark Task Complete/Incomplete (Priority: P2)

As a user, I want to mark tasks as complete or incomplete, so I can track my progress and see what's done.

**Why this priority**: Tracking completion is the primary way users measure progress. This transforms a simple list into a productivity tool.

**Independent Test**: Can be tested by adding a task, marking it complete, viewing tasks to verify status change, then toggling back to incomplete. Delivers value by enabling progress tracking.

**Acceptance Scenarios**:

1. **Given** a pending task with ID 1 exists, **When** I select option 5 (Mark Complete) and enter ID 1, **Then** the system displays "Task marked as completed" and the task status changes to completed.

2. **Given** a completed task with ID 1 exists, **When** I select Mark Complete and enter ID 1, **Then** the system displays "Task marked as pending" and the task status changes to pending.

3. **Given** no task with ID 99 exists, **When** I enter ID 99 in Mark Complete, **Then** the system displays "Task not found." and returns to the main menu.

4. **Given** I am prompted for a task ID, **When** I enter non-numeric input like "abc", **Then** the system displays "Invalid input. Please enter a number." and returns to the menu.

---

### User Story 4 - Update Task (Priority: P2)

As a user, I want to update a task's title or description, so I can correct mistakes or add more details.

**Why this priority**: Mistakes happen and requirements evolve. Without update capability, users must delete and recreate tasks, losing the task ID and history context.

**Independent Test**: Can be tested by adding a task, selecting Update, modifying the title/description, then viewing tasks to confirm changes. Delivers value by allowing task refinement.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists with title "Buy groceries", **When** I select option 3 (Update Task) and enter ID 1, **Then** I see the current title and am prompted for a new title.

2. **Given** I am updating task 1 with title "Buy groceries", **When** I enter a new title "Buy organic groceries", **Then** the title is updated and I am prompted for description.

3. **Given** I am prompted for a new title, **When** I press Enter without input, **Then** the original title is preserved and I proceed to description prompt.

4. **Given** I have updated title and/or description, **When** the update completes, **Then** the system displays "Task updated" and returns to the main menu.

5. **Given** no task with ID 99 exists, **When** I enter ID 99 in Update Task, **Then** the system displays "Task not found." and returns to the main menu.

---

### User Story 5 - Delete Task (Priority: P3)

As a user, I want to delete a task I no longer need, so I can keep my task list clean and focused.

**Why this priority**: While important for list hygiene, deletion is less critical than creation and viewing. Users can work around this by simply ignoring unwanted tasks.

**Independent Test**: Can be tested by adding a task, deleting it, then viewing tasks to verify removal. Delivers value by enabling list cleanup.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists, **When** I select option 4 (Delete Task) and enter ID 1, **Then** the system asks for confirmation "Are you sure you want to delete this task? (y/n)".

2. **Given** I am confirming deletion for task 1, **When** I enter "y" or "Y", **Then** the task is removed and system displays "Task deleted".

3. **Given** I am confirming deletion for task 1, **When** I enter "n" or "N", **Then** the task is NOT deleted and system displays "Deletion cancelled" and returns to menu.

4. **Given** I am confirming deletion, **When** I enter anything other than y/Y/n/N, **Then** the system treats it as "no" and cancels deletion.

5. **Given** no task with ID 99 exists, **When** I enter ID 99 in Delete Task, **Then** the system displays "Task not found." and returns to the main menu.

---

### User Story 6 - Exit Application (Priority: P3)

As a user, I want to exit the application gracefully, so I can end my session when done.

**Why this priority**: Basic usability requirement. Users need a clear way to exit rather than using Ctrl+C.

**Independent Test**: Can be tested by selecting Exit option and verifying the application terminates with a farewell message.

**Acceptance Scenarios**:

1. **Given** I am at the main menu, **When** I select option 6 (Exit), **Then** the system displays "Goodbye!" and the application terminates.

2. **Given** I have added tasks during the session, **When** I exit the application, **Then** all tasks are lost (expected behavior for in-memory storage).

---

### Edge Cases

- **Empty title handling**: System rejects empty or whitespace-only titles with clear error message
- **Invalid menu choice**: Entering a number outside 1-6 or non-numeric input displays "Invalid choice. Please try again."
- **Invalid task ID format**: Non-numeric input for task ID displays "Invalid input. Please enter a number."
- **Task ID not found**: Operations on non-existent IDs display "Task not found." without crashing
- **Very long input**: Titles up to 200 characters and descriptions up to 1000 characters are accepted
- **Special characters**: Titles and descriptions can contain any printable characters including unicode
- **Keyboard interrupt (Ctrl+C)**: Application handles interrupt gracefully, displaying "Goodbye!" and exiting cleanly

## Requirements *(mandatory)*

### Functional Requirements

#### Task Management

- **FR-001**: System MUST allow users to create a new task with a required title (1-200 characters) and optional description (0-1000 characters)
- **FR-002**: System MUST assign a unique sequential integer ID to each task, starting from 1
- **FR-003**: System MUST store a creation timestamp for each task
- **FR-004**: System MUST display all tasks with their ID, completion status indicator, and title
- **FR-005**: System MUST allow users to update the title and/or description of an existing task by ID
- **FR-006**: System MUST allow users to delete a task by ID with confirmation prompt
- **FR-007**: System MUST allow users to toggle the completion status of a task by ID

#### User Interface

- **FR-008**: System MUST display an interactive numbered menu with options 1-6
- **FR-009**: System MUST display the menu format exactly as:
  ```
  === TaskFlow ===
  1. Add Task
  2. View Tasks
  3. Update Task
  4. Delete Task
  5. Mark Complete
  6. Exit

  Enter choice (1-6): _
  ```
- **FR-010**: System MUST return to the main menu after completing any operation (except Exit)
- **FR-011**: System MUST display completion status as "[ ]" for pending and "[✓]" for completed tasks

#### Input Validation

- **FR-012**: System MUST reject empty or whitespace-only task titles with error message "Title cannot be empty"
- **FR-013**: System MUST handle non-numeric input for menu choices gracefully with error message "Invalid choice. Please try again."
- **FR-014**: System MUST handle non-numeric input for task IDs with error message "Invalid input. Please enter a number."
- **FR-015**: System MUST handle non-existent task IDs with error message "Task not found."

#### Data Storage

- **FR-016**: System MUST store all tasks in memory only (no file or database persistence)
- **FR-017**: System MUST NOT persist any data between application sessions

### Key Entities

- **Task**: Represents a todo item with the following attributes:
  - **id**: Unique integer identifier, auto-assigned sequentially starting from 1
  - **title**: Required text describing the task (1-200 characters)
  - **description**: Optional text with additional details (0-1000 characters)
  - **completed**: Boolean indicating whether task is done (default: false)
  - **created_at**: Timestamp when the task was created

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new task in under 15 seconds (from menu selection to confirmation)
- **SC-002**: Users can view their complete task list in under 2 seconds response time
- **SC-003**: 100% of invalid inputs are caught and display user-friendly error messages (no crashes or stack traces)
- **SC-004**: Users can complete all 5 core operations (add, view, update, delete, mark complete) in a single session without application restart
- **SC-005**: Application handles up to 1000 tasks in memory without noticeable performance degradation
- **SC-006**: All menu operations return to the main menu within 1 second of completion
- **SC-007**: First-time users can successfully add and view a task without documentation (intuitive interface)

## Assumptions

The following reasonable defaults have been assumed based on the requirements:

1. **Single user**: The application is designed for a single user per session; no multi-user or authentication features
2. **Terminal environment**: Users have access to a terminal/console that supports basic text input/output
3. **Sequential IDs**: Task IDs are never reused, even after deletion (simpler implementation, no ID conflicts)
4. **No persistence warning**: Users understand that closing the app loses all data (documented in README, mentioned at exit)
5. **Case-insensitive confirmation**: Delete confirmation accepts uppercase or lowercase y/n
6. **UTF-8 support**: Terminal supports UTF-8 for the checkmark character (✓)

## Out of Scope

The following features are explicitly excluded from Phase 1:

- Command-line arguments (all interaction via interactive menu)
- File persistence or database storage
- Task priorities or due dates
- Categories, tags, or labels
- Search or filtering capabilities
- Task sorting options
- Undo/redo functionality
- Multiple task lists or projects
- User authentication or multi-user support
- Configuration files or settings
- Color output or rich terminal formatting
- Export/import functionality

## Dependencies

- Python 3.13+ runtime environment
- UV package manager for project setup
- pytest for testing (development dependency only)
- mypy for type checking (development dependency only)

## Glossary

- **Task**: A single todo item with title, description, and completion status
- **Pending**: A task that has not been marked as complete
- **Completed**: A task that has been marked as done
- **Session**: The duration from application start to exit; all data exists only within a session
