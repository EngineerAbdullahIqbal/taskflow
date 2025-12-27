"""TaskFlow application entry point."""

from src.services import TaskManager
from src.storage import InMemoryStorage
from src.cli import (
    display_menu,
    get_menu_choice,
    get_task_title,
    get_task_description,
    get_task_id,
    get_confirmation,
    display_tasks,
    display_message,
)


def main() -> None:
    """Run the TaskFlow application main loop."""
    storage = InMemoryStorage()
    manager = TaskManager(storage)

    print("Welcome to TaskFlow!")

    try:
        while True:
            display_menu()

            try:
                choice = get_menu_choice()

                if choice == 1:
                    # Add Task
                    title = get_task_title()
                    description = get_task_description()
                    task = manager.add_task(title, description)
                    display_message(f"Task added with ID: {task.id}")

                elif choice == 2:
                    # View Tasks
                    tasks = manager.get_all_tasks()
                    display_tasks(tasks)

                elif choice == 3:
                    # Update Task
                    task_id = get_task_id()
                    current_task = manager.get_task(task_id)

                    if current_task is None:
                        display_message("Task not found.")
                        continue

                    print(f"Current title: {current_task.title}")
                    new_title = input("Enter new title (press Enter to keep): ").strip()

                    print(f"Current description: {current_task.description}")
                    new_description = input("Enter new description (press Enter to keep): ").strip()

                    updated = manager.update_task(
                        task_id,
                        title=new_title if new_title else None,
                        description=new_description if new_description else None
                    )

                    if updated:
                        display_message("Task updated")
                    else:
                        display_message("Task not found.")

                elif choice == 4:
                    # Delete Task
                    task_id = get_task_id()
                    task_to_delete = manager.get_task(task_id)

                    if task_to_delete is None:
                        display_message("Task not found.")
                        continue

                    if get_confirmation("Are you sure you want to delete this task? (y/n): "):
                        manager.delete_task(task_id)
                        display_message("Task deleted")
                    else:
                        display_message("Deletion cancelled")

                elif choice == 5:
                    # Mark Complete
                    task_id = get_task_id()
                    toggled_task = manager.toggle_complete(task_id)

                    if toggled_task is None:
                        display_message("Task not found.")
                    elif toggled_task.completed:
                        display_message("Task marked as completed")
                    else:
                        display_message("Task marked as pending")

                elif choice == 6:
                    # Exit
                    display_message("Goodbye!")
                    break

            except ValueError as e:
                display_message(f"Error: {e}")
            except KeyboardInterrupt:
                display_message("\nGoodbye!")
                break

    except KeyboardInterrupt:
        display_message("\nGoodbye!")


if __name__ == "__main__":
    main()
