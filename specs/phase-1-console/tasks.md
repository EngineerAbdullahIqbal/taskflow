# Tasks: TaskFlow Console Application

**Input**: Design documents from `/specs/phase-1-console/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅
**Constitution**: TDD is NON-NEGOTIABLE - Tests MUST be written FIRST (Red-Green-Refactor)

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- All file paths are relative to repository root

## Path Conventions (from plan.md)

```
src/
├── __init__.py          # Package marker
├── main.py              # Entry point
├── cli.py               # Menu display, input handling
├── models.py            # Task dataclass
├── services.py          # TaskManager business logic
└── storage.py           # StorageProtocol + InMemoryStorage

tests/
├── conftest.py          # Shared fixtures
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_storage.py
└── integration/
    └── test_cli.py
```

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and development environment

- [ ] T001 Initialize Python 3.13+ project with UV: `uv init taskflow && cd taskflow`
- [ ] T002 Add development dependencies: `uv add --dev pytest mypy ruff`
- [ ] T003 [P] Create pyproject.toml with mypy strict configuration
- [ ] T004 [P] Create src/__init__.py package marker
- [ ] T005 [P] Create tests/__init__.py and tests/unit/__init__.py and tests/integration/__init__.py
- [ ] T006 Create tests/conftest.py with shared fixtures (empty TaskManager, sample tasks)
- [ ] T007 [P] Create README.md with project overview and quickstart

**Checkpoint**: Run `uv run pytest` and `uv run mypy --strict src/` - both should pass (no tests yet)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data model and storage layer that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Architecture Reference**: [ADR-001](../../history/adr/ADR-001-three-layer-architecture-with-protocol-abstraction.md), [ADR-002](../../history/adr/ADR-002-data-modeling-with-dataclass-and-validation.md)

### 2.1 Models Layer (TDD)

- [ ] T008 [P] Write failing tests for Task dataclass in tests/unit/test_models.py
  - Test Task creation with all fields
  - Test __str__ format: "[status] id. title"
  - Test status_indicator property: "[ ]" or "[✓]"
  - Test default values (completed=False, description="")
- [ ] T009 Implement Task dataclass in src/models.py (make T008 pass)
  - Fields: id, title, description, completed, created_at
  - Per data-model.md validation rules VR-001 to VR-004

### 2.2 Storage Layer (TDD)

- [ ] T010 [P] Write failing tests for StorageProtocol in tests/unit/test_storage.py
  - Test add() returns Task with assigned ID
  - Test get_all() returns list of all tasks
  - Test get(id) returns Task or None
  - Test update() modifies existing task
  - Test delete() returns True if found, False otherwise
  - Test sequential ID generation (1, 2, 3...)
  - Test IDs never reused after deletion
- [ ] T011 Implement StorageProtocol and InMemoryStorage in src/storage.py (make T010 pass)
  - typing.Protocol for interface (ADR-001)
  - InMemoryStorage with list + _next_id counter

### 2.3 Service Layer Shell (TDD)

- [ ] T012 [P] Write failing tests for TaskManager initialization in tests/unit/test_services.py
  - Test TaskManager accepts StorageProtocol
  - Test TaskManager with InMemoryStorage
- [ ] T013 Implement TaskManager class shell in src/services.py (make T012 pass)
  - Constructor accepts storage: StorageProtocol
  - No methods yet - just initialization

**Checkpoint**: `uv run pytest tests/unit/` - ALL tests GREEN. `uv run mypy --strict src/` - PASS

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks with title and optional description

**Independent Test**: Launch app → Select "Add Task" → Enter title → Verify confirmation

**Spec Reference**: FR-001, FR-002, FR-003, FR-012

### Tests for User Story 1 (TDD - Write First, Must FAIL)

- [ ] T014 [P] [US1] Write failing tests for TaskManager.add_task() in tests/unit/test_services.py
  - Test add_task(title, description) returns Task with ID
  - Test task has correct title and description
  - Test task has completed=False by default
  - Test task has created_at timestamp
  - Test empty title raises ValueError
  - Test whitespace-only title raises ValueError
- [ ] T015 [P] [US1] Write failing tests for CLI add task flow in tests/integration/test_cli.py
  - Test menu displays "1. Add Task" option
  - Test selecting 1 prompts for title
  - Test entering title prompts for description
  - Test confirmation message shows assigned ID
  - Test empty title shows error, re-prompts

### Implementation for User Story 1 (Make Tests GREEN)

- [ ] T016 [US1] Implement TaskManager.add_task() in src/services.py (make T014 pass)
  - Validate title not empty (FR-012)
  - Create Task with next ID (FR-002)
  - Store via storage.add()
  - Return created Task
- [ ] T017 [P] [US1] Implement get_task_title() in src/cli.py
  - Prompt for title input
  - Validate non-empty
  - Return stripped title
- [ ] T018 [P] [US1] Implement get_task_description() in src/cli.py
  - Prompt for optional description
  - Return stripped input (empty allowed)
- [ ] T019 [US1] Implement add task menu handler in src/main.py (make T015 pass)
  - Call get_task_title()
  - Call get_task_description()
  - Call manager.add_task()
  - Display confirmation with ID

**Checkpoint**: User Story 1 complete. Can add tasks and see confirmation. Tests GREEN.

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can see all tasks with ID, status, and title

**Independent Test**: Add 2-3 tasks → Select "View Tasks" → Verify all displayed correctly

**Spec Reference**: FR-004, FR-011

### Tests for User Story 2 (TDD - Write First, Must FAIL)

- [ ] T020 [P] [US2] Write failing tests for TaskManager.get_all_tasks() in tests/unit/test_services.py
  - Test returns empty list when no tasks
  - Test returns all added tasks
  - Test tasks in list have correct format
- [ ] T021 [P] [US2] Write failing tests for CLI view tasks in tests/integration/test_cli.py
  - Test menu displays "2. View Tasks" option
  - Test "No tasks found." when empty
  - Test displays tasks with "[status] id. title" format
  - Test pending shows "[ ]", completed shows "[✓]"

### Implementation for User Story 2 (Make Tests GREEN)

- [ ] T022 [US2] Implement TaskManager.get_all_tasks() in src/services.py (make T020 pass)
  - Delegate to storage.get_all()
  - Return list[Task]
- [ ] T023 [P] [US2] Implement display_tasks() in src/cli.py
  - Format each task using Task.__str__()
  - Handle empty list with "No tasks found."
- [ ] T024 [US2] Implement view tasks menu handler in src/main.py (make T021 pass)
  - Call manager.get_all_tasks()
  - Call display_tasks()

**Checkpoint**: User Stories 1 & 2 complete. Can add and view tasks. MVP deliverable!

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle task completion status

**Independent Test**: Add task → Mark complete → View (shows [✓]) → Mark again → View (shows [ ])

**Spec Reference**: FR-007, FR-014, FR-015

### Tests for User Story 3 (TDD - Write First, Must FAIL)

- [ ] T025 [P] [US3] Write failing tests for TaskManager.toggle_complete() in tests/unit/test_services.py
  - Test pending task becomes completed
  - Test completed task becomes pending
  - Test returns updated Task
  - Test non-existent ID returns None
- [ ] T026 [P] [US3] Write failing tests for CLI mark complete in tests/integration/test_cli.py
  - Test menu displays "5. Mark Complete" option
  - Test prompts for task ID
  - Test "Task marked as completed" for pending→complete
  - Test "Task marked as pending" for complete→pending
  - Test "Task not found." for invalid ID
  - Test "Invalid input" for non-numeric input

### Implementation for User Story 3 (Make Tests GREEN)

- [ ] T027 [US3] Implement TaskManager.toggle_complete() in src/services.py (make T025 pass)
  - Get task by ID from storage
  - If not found, return None
  - Toggle completed boolean
  - Update via storage.update()
  - Return updated Task
- [ ] T028 [P] [US3] Implement get_task_id() in src/cli.py
  - Prompt for task ID
  - Validate numeric input (FR-014)
  - Return integer ID
- [ ] T029 [US3] Implement mark complete menu handler in src/main.py (make T026 pass)
  - Call get_task_id()
  - Call manager.toggle_complete()
  - Display appropriate message based on result

**Checkpoint**: User Stories 1-3 complete. Core task management functional.

---

## Phase 6: User Story 4 - Update Task (Priority: P2)

**Goal**: Users can modify task title and description

**Independent Test**: Add task → Update title/description → View to verify changes

**Spec Reference**: FR-005, FR-014, FR-015

### Tests for User Story 4 (TDD - Write First, Must FAIL)

- [ ] T030 [P] [US4] Write failing tests for TaskManager.update_task() in tests/unit/test_services.py
  - Test updates title when provided
  - Test updates description when provided
  - Test preserves original if empty string passed
  - Test returns updated Task
  - Test non-existent ID returns None
- [ ] T031 [P] [US4] Write failing tests for CLI update task in tests/integration/test_cli.py
  - Test menu displays "3. Update Task" option
  - Test prompts for task ID
  - Test shows current title, prompts for new
  - Test shows current description, prompts for new
  - Test "Task updated" confirmation
  - Test "Task not found." for invalid ID
  - Test pressing Enter preserves original value

### Implementation for User Story 4 (Make Tests GREEN)

- [ ] T032 [US4] Implement TaskManager.update_task() in src/services.py (make T030 pass)
  - Get task by ID from storage
  - If not found, return None
  - Update title if non-empty provided
  - Update description if provided (empty allowed)
  - Update via storage.update()
  - Return updated Task
- [ ] T033 [US4] Implement TaskManager.get_task() in src/services.py
  - Delegate to storage.get()
  - Return Task or None
- [ ] T034 [US4] Implement update task menu handler in src/main.py (make T031 pass)
  - Call get_task_id()
  - Call manager.get_task() to show current values
  - Prompt for new title (Enter = keep original)
  - Prompt for new description (Enter = keep original)
  - Call manager.update_task()
  - Display confirmation

**Checkpoint**: User Stories 1-4 complete. Full CRUD except delete.

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Users can remove tasks with confirmation

**Independent Test**: Add task → Delete with confirmation → View to verify removed

**Spec Reference**: FR-006, FR-014, FR-015

### Tests for User Story 5 (TDD - Write First, Must FAIL)

- [ ] T035 [P] [US5] Write failing tests for TaskManager.delete_task() in tests/unit/test_services.py
  - Test returns True when task deleted
  - Test returns False when task not found
  - Test task removed from storage
- [ ] T036 [P] [US5] Write failing tests for CLI delete task in tests/integration/test_cli.py
  - Test menu displays "4. Delete Task" option
  - Test prompts for task ID
  - Test confirmation prompt "Are you sure? (y/n)"
  - Test "y" or "Y" deletes and shows "Task deleted"
  - Test "n" or "N" cancels and shows "Deletion cancelled"
  - Test other input treated as "no"
  - Test "Task not found." for invalid ID

### Implementation for User Story 5 (Make Tests GREEN)

- [ ] T037 [US5] Implement TaskManager.delete_task() in src/services.py (make T035 pass)
  - Delegate to storage.delete()
  - Return boolean result
- [ ] T038 [P] [US5] Implement get_confirmation() in src/cli.py
  - Prompt with message and (y/n)
  - Return True only for y/Y
  - Return False for all other input
- [ ] T039 [US5] Implement delete task menu handler in src/main.py (make T036 pass)
  - Call get_task_id()
  - Check task exists first
  - Call get_confirmation()
  - If confirmed, call manager.delete_task()
  - Display appropriate message

**Checkpoint**: User Stories 1-5 complete. Full CRUD functionality.

---

## Phase 8: User Story 6 - Exit Application (Priority: P3)

**Goal**: Users can exit gracefully

**Independent Test**: Select Exit → Verify "Goodbye!" displayed and app terminates

**Spec Reference**: FR-008, FR-009, FR-010

### Tests for User Story 6 (TDD - Write First, Must FAIL)

- [ ] T040 [P] [US6] Write failing tests for CLI menu and exit in tests/integration/test_cli.py
  - Test menu displays all 6 options in correct format
  - Test menu displays "=== TaskFlow ===" header
  - Test option 6 displays "Goodbye!"
  - Test invalid menu choice shows "Invalid choice. Please try again."
  - Test Ctrl+C handled gracefully

### Implementation for User Story 6 (Make Tests GREEN)

- [ ] T041 [P] [US6] Implement display_menu() in src/cli.py
  - Print header "=== TaskFlow ==="
  - Print all 6 options per FR-009
  - Print prompt "Enter choice (1-6): "
- [ ] T042 [P] [US6] Implement get_menu_choice() in src/cli.py
  - Read input
  - Validate 1-6 (FR-013)
  - Return integer choice
- [ ] T043 [P] [US6] Implement display_message() in src/cli.py
  - Print message to stdout
  - Used for confirmations and errors
- [ ] T044 [US6] Implement main loop in src/main.py (make T040 pass)
  - Create TaskManager with InMemoryStorage
  - Loop: display_menu → get_menu_choice → dispatch → repeat
  - Option 6: display "Goodbye!" and break
  - Handle KeyboardInterrupt gracefully
- [ ] T045 [US6] Create application entry point in src/main.py
  - if __name__ == "__main__": main()
  - Ensure clean startup and shutdown

**Checkpoint**: All User Stories complete. Full application functional.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Quality gates, documentation, and final validation

- [ ] T046 [P] Run quality gate: `uv run pytest` - all tests pass
- [ ] T047 [P] Run quality gate: `uv run mypy --strict src/` - no type errors
- [ ] T048 [P] Run quality gate: `uv run ruff check src/` - no lint violations
- [ ] T049 Verify all public functions have docstrings (Doc Gate)
- [ ] T050 [P] Update README.md with usage instructions
- [ ] T051 Manual testing: Run through all acceptance scenarios from spec.md
- [ ] T052 Manual testing: Test edge cases (empty input, invalid IDs, Ctrl+C)
- [ ] T053 Run quickstart.md validation if available

**Checkpoint**: All quality gates pass. Application ready for release.

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) ← BLOCKS all user stories
    ↓
┌───┴───┐
│       │
Phase 3 (US1: Add) ← MVP
    ↓
Phase 4 (US2: View) ← MVP Complete
    ↓
Phase 5 (US3: Mark Complete)
    ↓
Phase 6 (US4: Update)
    ↓
Phase 7 (US5: Delete)
    ↓
Phase 8 (US6: Exit + Main Loop)
    ↓
Phase 9 (Polish)
```

### User Story Dependencies

| Story | Depends On | Can Parallelize With |
|-------|------------|---------------------|
| US1 (Add) | Foundation | None (first story) |
| US2 (View) | Foundation | US1* |
| US3 (Mark Complete) | Foundation | US1, US2* |
| US4 (Update) | Foundation | US1, US2, US3* |
| US5 (Delete) | Foundation | US1-US4* |
| US6 (Exit) | Foundation | US1-US5 (needs main loop) |

*Limited parallelization: Stories share files but tests are independent.

### Within Each User Story

1. **Tests FIRST** (TDD - RED phase)
2. Service layer implementation (GREEN phase)
3. CLI layer implementation (GREEN phase)
4. Main.py handler integration
5. **Refactor** if needed

---

## Parallel Opportunities

### Phase 2 Parallelization

```bash
# These can run in parallel (different files):
Task T008: "tests for Task dataclass in tests/unit/test_models.py"
Task T010: "tests for StorageProtocol in tests/unit/test_storage.py"
Task T012: "tests for TaskManager init in tests/unit/test_services.py"
```

### Within User Stories

```bash
# US1 Tests (parallel):
Task T014: "tests for add_task() in tests/unit/test_services.py"
Task T015: "tests for CLI add flow in tests/integration/test_cli.py"

# US1 Implementation (parallel after T014 passes):
Task T017: "get_task_title() in src/cli.py"
Task T018: "get_task_description() in src/cli.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup ✓
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: User Story 1 (Add Task)
4. Complete Phase 4: User Story 2 (View Tasks)
5. **STOP and VALIDATE**: Can add and view tasks
6. Run quality gates
7. Deploy/demo MVP

### Incremental Delivery

| Increment | Stories | Value Delivered |
|-----------|---------|-----------------|
| MVP | US1 + US2 | Add and view tasks |
| Core | +US3 | Track completion |
| Full CRUD | +US4, US5 | Update and delete |
| Complete | +US6 | Clean exit, full app |

### Task Count Summary

| Phase | Tasks | Parallel |
|-------|-------|----------|
| Setup | 7 | 4 |
| Foundation | 6 | 3 |
| US1 (Add) | 6 | 4 |
| US2 (View) | 5 | 3 |
| US3 (Mark) | 5 | 3 |
| US4 (Update) | 6 | 2 |
| US5 (Delete) | 5 | 3 |
| US6 (Exit) | 6 | 4 |
| Polish | 8 | 4 |
| **Total** | **54** | **30** |

---

## Notes

- [P] tasks = different files, no dependencies
- [US#] label maps task to specific user story
- TDD is NON-NEGOTIABLE: Write tests FIRST, see them FAIL
- Constitution requires: All quality gates pass before merge
- Each checkpoint = independently testable increment
- Commit after each GREEN phase (tests pass)
