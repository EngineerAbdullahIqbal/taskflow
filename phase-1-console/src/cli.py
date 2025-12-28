"""Command-line interface for TaskFlow."""

from src.models import Task


def display_menu() -> None:
    """Display the main menu."""
    print("\n=== TaskFlow ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete")
    print("6. Exit")
    print()


def get_menu_choice() -> int:
    """Get and validate menu choice from user.

    Returns:
        Integer choice 1-6

    Raises:
        ValueError: If choice is not 1-6
    """
    while True:
        try:
            choice_str = input("Enter choice (1-6): ").strip()
            choice = int(choice_str)
            if 1 <= choice <= 6:
                return choice
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid choice. Please try again.")


def get_task_title() -> str:
    """Get and validate task title from user.

    Returns:
        Non-empty task title
    """
    while True:
        title = input("Enter task title: ").strip()
        if not title:
            print("Title cannot be empty")
            continue
        return title


def get_task_description() -> str:
    """Get optional task description from user.

    Returns:
        Task description (can be empty)
    """
    description = input("Enter task description (optional): ").strip()
    return description


def get_task_id() -> int:
    """Get and validate task ID from user.

    Returns:
        Valid task ID
    """
    while True:
        try:
            task_id_str = input("Enter task ID: ").strip()
            task_id = int(task_id_str)
            return task_id
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_confirmation(prompt: str = "Are you sure? (y/n): ") -> bool:
    """Get y/n confirmation from user.

    Args:
        prompt: Confirmation prompt text

    Returns:
        True if user enters y/Y, False otherwise
    """
    response = input(prompt).strip().lower()
    return response == "y"


def display_tasks(tasks: list[Task]) -> None:
    """Display list of tasks with status and ID.

    Args:
        tasks: List of tasks to display
    """
    if not tasks:
        print("No tasks found.")
        return

    print("\nYour Tasks:")
    for task in tasks:
        print(f"  {task}")
    print()


def display_message(message: str) -> None:
    """Display a message to the user.

    Args:
        message: Message to display
    """
    print(message)
