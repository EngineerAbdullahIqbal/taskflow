# Phase I: Todo In-Memory Python Console App

**Due Date:** December 7, 2025  
**Points:** 100

## Objective

Build a command-line todo application that stores tasks in memory using Claude Code and Spec-Kit Plus.

## Development Approach

💡 **Use the Agentic Dev Stack workflow:** Write spec → Generate plan → Break into tasks → Implement via Claude Code. **No manual coding allowed.** We will review the process, prompts, and iterations to judge each phase and project.

## Basic Level Functionality

These form the foundation—quick to build, essential for any MVP:

1. **Add Task** – Create new todo items
2. **Delete Task** – Remove tasks from the list
3. **Update Task** – Modify existing task details
4. **View Task List** – Display all tasks
5. **Mark as Complete** – Toggle task completion status

## Requirements

* Implement all 5 Basic Level features (Add, Delete, Update, View, Mark Complete)
* Use spec-driven development with Claude Code and Spec-Kit Plus
* Follow clean code principles and proper Python project structure

## Technology Stack

* **UV** - Python package manager
* **Python 3.13+**
* **Claude Code** - AI coding assistant
* **Spec-Kit Plus** - Specification management

## Windows Users: WSL 2 Setup

Windows users must use WSL 2 (Windows Subsystem for Linux) for development:

```bash
# Install WSL 2
wsl --install

# Set WSL 2 as default
wsl --set-default-version 2

# Install Ubuntu
wsl --install -d Ubuntu-22.04
```

## Project Structure

Your repository should follow this structure:

```
phase1-todo-console/
├── constitution.md           # Project constitution and principles
├── specs/                    # Specifications history
│   ├── requirements.md       # What needs to be built
│   ├── plan.md              # How it will be built
│   └── tasks.md             # Breakdown of implementation tasks
├── src/                     # Source code
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── todo.py              # Todo logic
│   └── models.py            # Data models
├── tests/                   # Test files
│   └── test_todo.py
├── CLAUDE.md                # Claude Code instructions
├── README.md                # Setup and usage instructions
├── pyproject.toml           # Project dependencies
└── .gitignore
```

## Spec-Driven Development Workflow

### Step 1: Initialize Spec-Kit Plus

```bash
uv specifyplus init phase1-todo-console
```

This creates the necessary structure for spec-driven development.

### Step 2: Create Constitution

Write your project constitution defining principles and constraints:

```markdown
# Todo Console App Constitution

## Purpose
A simple, in-memory command-line todo application for learning spec-driven development.

## Principles
1. **Simplicity First** - Keep it simple, no unnecessary complexity
2. **User-Friendly** - Clear prompts and feedback
3. **Data Integrity** - Validate all inputs
4. **Testable** - All functions should be unit-testable

## Constraints
- Must run in terminal/console
- No external dependencies except UV
- Data stored in memory only (no persistence)
- Python 3.13+ only

## Standards
- Follow PEP 8 style guide
- Use type hints
- Include docstrings for all functions
- Handle errors gracefully
```

### Step 3: Write Specifications

Using Spec-Kit Plus commands:

```bash
# Create requirement specifications
uv specifyplus specify

# Create technical plan
uv specifyplus plan

# Break down into tasks
uv specifyplus tasks
```

## Example Specifications

### requirements.md

```markdown
# Requirements Specification

## User Stories

### US-001: Add Task
As a user, I want to add a new task with a title and description, so I can track what I need to do.

**Acceptance Criteria:**
- User can enter a task title (required, 1-200 characters)
- User can enter a task description (optional, max 1000 characters)
- System assigns a unique ID to each task
- System displays confirmation message with task ID

### US-002: View Tasks
As a user, I want to see all my tasks, so I can review what I need to do.

**Acceptance Criteria:**
- Display task ID, title, and status (pending/completed)
- Show empty message if no tasks exist
- Tasks numbered for easy reference

### US-003: Update Task
As a user, I want to update a task's details, so I can correct mistakes or add information.

**Acceptance Criteria:**
- User can select task by ID
- User can modify title and/or description
- System validates new inputs
- System displays confirmation

### US-004: Delete Task
As a user, I want to delete a task, so I can remove tasks I no longer need.

**Acceptance Criteria:**
- User can select task by ID
- System asks for confirmation
- System removes task and displays confirmation

### US-005: Mark Complete
As a user, I want to mark tasks as complete, so I can track my progress.

**Acceptance Criteria:**
- User can toggle task status by ID
- Completed tasks shown with [✓] indicator
- Pending tasks shown with [ ] indicator
```

### plan.md

```markdown
# Technical Plan

## Architecture

### Components
1. **Task Model** - Data structure for todo items
2. **Task Manager** - Business logic for CRUD operations
3. **CLI Interface** - User interaction layer

### Data Model

```python
class Task:
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
```

### Task Manager Operations

```python
class TaskManager:
    def add_task(title: str, description: str) -> Task
    def get_tasks() -> List[Task]
    def get_task(task_id: int) -> Task
    def update_task(task_id: int, title: str, description: str) -> Task
    def delete_task(task_id: int) -> bool
    def toggle_complete(task_id: int) -> Task
```

## Implementation Approach

1. Create Task data model
2. Implement TaskManager with in-memory storage
3. Build CLI menu system
4. Add input validation
5. Implement error handling
6. Write tests
```

### tasks.md

```markdown
# Implementation Tasks

## Task Breakdown

### T-001: Setup Project Structure
- [ ] Create project directory
- [ ] Initialize UV project
- [ ] Create folder structure
- [ ] Setup .gitignore

### T-002: Implement Task Model
- [ ] Create models.py
- [ ] Define Task dataclass
- [ ] Add type hints
- [ ] Add validation

### T-003: Implement Task Manager
- [ ] Create todo.py
- [ ] Initialize in-memory storage (list)
- [ ] Implement add_task()
- [ ] Implement get_tasks()
- [ ] Implement get_task()
- [ ] Implement update_task()
- [ ] Implement delete_task()
- [ ] Implement toggle_complete()

### T-004: Build CLI Interface
- [ ] Create main.py
- [ ] Implement menu system
- [ ] Add user input handlers
- [ ] Add display formatters
- [ ] Add input validation

### T-005: Error Handling
- [ ] Add try-except blocks
- [ ] Validate user inputs
- [ ] Handle invalid task IDs
- [ ] Display user-friendly errors

### T-006: Testing
- [ ] Write unit tests for TaskManager
- [ ] Test all CRUD operations
- [ ] Test edge cases
- [ ] Run all tests

### T-007: Documentation
- [ ] Write README.md
- [ ] Add usage examples
- [ ] Document setup steps
```

## CLAUDE.md Instructions

Create a CLAUDE.md file to guide Claude Code:

```markdown
# Claude Code Instructions - Phase I Todo Console

## Project Context
This is Phase I of the Hackathon II project: an in-memory console-based todo application.

## Development Rules
1. **Spec-Driven Only**: Never write code without referencing a task from @specs/tasks.md
2. **Constitution First**: Always check @constitution.md before making decisions
3. **Reference Format**: Include task IDs in comments: `# Task: T-003`

## Project Structure
- @specs/ - All specifications (requirements, plan, tasks)
- @src/ - Application code
- @tests/ - Unit tests

## How to Work
1. Read the relevant spec file first
2. Implement ONLY what the task describes
3. Follow the technical plan in @specs/plan.md
4. Write tests for each feature
5. Keep code simple and readable

## Code Standards
- Use Python 3.13+ features
- Add type hints to all functions
- Write docstrings for all public functions
- Follow PEP 8 style guide
- Keep functions small and focused

## Testing
- Write tests in @tests/ directory
- Use pytest framework
- Test all CRUD operations
- Test error cases

## Commands to Run
- Run app: `uv run python src/main.py`
- Run tests: `uv run pytest`
```

## Example Implementation

### models.py

```python
# Task: T-002
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    """Represents a todo task."""
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        status = "✓" if self.completed else " "
        return f"[{status}] {self.id}. {self.title}"
```

### todo.py

```python
# Task: T-003
from typing import List, Optional
from models import Task

class TaskManager:
    """Manages todo tasks in memory."""
    
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id: int = 1
    
    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task."""
        task = Task(id=self.next_id, title=title, description=description)
        self.tasks.append(task)
        self.next_id += 1
        return task
    
    def get_tasks(self) -> List[Task]:
        """Get all tasks."""
        return self.tasks
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a specific task by ID."""
        return next((t for t in self.tasks if t.id == task_id), None)
    
    def update_task(self, task_id: int, title: str, description: str) -> Optional[Task]:
        """Update a task's details."""
        task = self.get_task(task_id)
        if task:
            task.title = title
            task.description = description
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
    
    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """Toggle task completion status."""
        task = self.get_task(task_id)
        if task:
            task.completed = not task.completed
        return task
```

### main.py

```python
# Task: T-004
from todo import TaskManager

def display_menu():
    """Display the main menu."""
    print("\n=== Todo Console App ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete/Incomplete")
    print("6. Exit")
    print("=" * 24)

def main():
    """Main application loop."""
    manager = TaskManager()
    
    while True:
        display_menu()
        choice = input("Enter choice (1-6): ").strip()
        
        if choice == "1":
            # Add task
            title = input("Enter task title: ").strip()
            description = input("Enter description (optional): ").strip()
            task = manager.add_task(title, description)
            print(f"✓ Task added with ID: {task.id}")
            
        elif choice == "2":
            # View tasks
            tasks = manager.get_tasks()
            if not tasks:
                print("No tasks found.")
            else:
                print("\nYour Tasks:")
                for task in tasks:
                    print(f"  {task}")
                    
        elif choice == "3":
            # Update task
            task_id = int(input("Enter task ID: "))
            task = manager.get_task(task_id)
            if not task:
                print("Task not found.")
                continue
            title = input(f"Enter new title [{task.title}]: ").strip() or task.title
            desc = input(f"Enter new description [{task.description}]: ").strip() or task.description
            manager.update_task(task_id, title, desc)
            print("✓ Task updated")
            
        elif choice == "4":
            # Delete task
            task_id = int(input("Enter task ID: "))
            if manager.delete_task(task_id):
                print("✓ Task deleted")
            else:
                print("Task not found.")
                
        elif choice == "5":
            # Toggle complete
            task_id = int(input("Enter task ID: "))
            task = manager.toggle_complete(task_id)
            if task:
                status = "completed" if task.completed else "pending"
                print(f"✓ Task marked as {status}")
            else:
                print("Task not found.")
                
        elif choice == "6":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
```

## Deliverables

1. **GitHub repository with:**
   * Constitution file (`constitution.md`)
   * Specs history folder containing all specification files (`specs/`)
   * `/src` folder with Python source code
   * `README.md` with setup instructions
   * `CLAUDE.md` with Claude Code instructions

2. **Working console application demonstrating:**
   * Adding tasks with title and description
   * Listing all tasks with status indicators
   * Updating task details
   * Deleting tasks by ID
   * Marking tasks as complete/incomplete

## README.md Example

```markdown
# Phase I - Todo Console App

A simple in-memory command-line todo application built using spec-driven development.

## Setup

1. Install UV:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone the repository:
```bash
git clone <your-repo-url>
cd phase1-todo-console
```

3. Run the application:
```bash
uv run python src/main.py
```

## Usage

The application provides a menu-driven interface:
- **Add Task**: Create a new todo item
- **View Tasks**: See all your tasks
- **Update Task**: Modify an existing task
- **Delete Task**: Remove a task
- **Mark Complete**: Toggle task completion status
- **Exit**: Close the application

## Development

This project was built using:
- Spec-Driven Development with Spec-Kit Plus
- Claude Code for implementation
- UV for Python package management

See `specs/` folder for all specifications.
```

## Submission Requirements

Submit via form: https://forms.gle/KMKEKaFUD6ZX4UtY8

1. **Public GitHub Repo Link**
2. **Demo video link** (must be under 90 seconds). You can use NotebookLM or record your demo
3. **WhatsApp number** (top submissions will be invited to present live)

## Live Presentation

**Date:** Sunday, December 7, 2025 at 8:00 PM  
**Platform:** Zoom  
**Join Zoom Meeting:**
- **Link:** https://us06web.zoom.us/j/84976847088?pwd=Z7t7NaeXwVmmR5fysCv7NiMbfbhIda.1
- **Meeting ID:** 849 7684 7088
- **Passcode:** 305850

Everyone is welcome to join the Zoom meeting to watch the presentations. Only invited participants will present their submissions.

---

## Tips for Success

1. **Start with Specs**: Write detailed specifications before any code
2. **Use Claude Code**: Let Claude Code generate the implementation
3. **Iterate**: Refine specs if Claude Code's output isn't right
4. **Keep it Simple**: Focus on working features, not complexity
5. **Document Everything**: Clear documentation helps judges understand your process

---

*Note: Top submissions will be invited via WhatsApp to present live on Zoom. All submissions will be evaluated. Live presentation is by invitation only, but does not affect final scor