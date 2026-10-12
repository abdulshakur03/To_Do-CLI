import json
import uuid
from datetime import datetime, date


def main():
    content = {}

    try:
        with open("todo.json", "r") as file:
            content = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        content = {}

    start(content)


def start(content):
    while True:
        print(f"\n{"="*30}TO-DO List{"="*30}")
        print("""
            "1. Add task"
            "2. View tasks"
            "3. Complete task"
            "4. Edit task"
            "5. Delete task"
            "6. Filter tasks"
            "7. Exit"
            """)

        prompt = validate_input("Enter an option: ")

        match prompt:
            case 1:
                add_task(content)
            case 2:
                view_task(content)
            case 3:
                complete_task(content)
            case 5:
                delete_task(content)
            case 7:
                print("operation canceled!")
                break
            case _:
                print("chose an option from 1-7")
        with open("todo.json", "w") as file:
            json.dump(content, file, indent=4)


def add_task(content):
    task_id = str(uuid.uuid4())
    task = get_input("add task: ")
    while True:
        add_date = get_input("is there a due date? [y/n]: ").strip().lower()
        if add_date == "y":
            d = get_date()
            today = date.today()
            while d < today:
                print("Date cannot be from the past.\nPick a present date!")
                d = get_date()
            due_date = d.isoformat()
            break

        elif add_date == "n":
            due_date = None
            break
        else:
            print("Invalid Input. type: [y/n]: ")

    content[task_id] = {
        "task": task,
        "status": "pending",
        "priority": "low",
        "due_date": due_date,
    }


def view_task(content):
    if not content:
        print("No task found.")
        return

    print(
        f"\n{'No.':<5} | {'TASK':<20} | {'STATUS':<10} | {'PRIORITY':<10} | {'DUE DATE':<10}"
    )

    for index, (task_id, details) in enumerate(content.items(), start=1):
        print("_" * 70)
        due = details["due_date"] or "-"
        print(
            f"{index:<5} | {details["task"]:<20} | {details["status"]:<10} | {details["priority"]:<10} | {due:<10}"
        )


def delete_task(content):
    if not content:
        print("No task to delete.")
        return
    view_task(content)

    task_num = validate_input("Enter the task number you want to delete: ")

    task_keys = list(content.keys())

    if 1 <= task_num <= len(task_keys):
        task_id_to_delete = task_keys[task_num - 1]
        removed = content.pop(task_id_to_delete, None)
        print(f"Deleted task: {removed["task"]}")
    else:
        print("Invalid task number")


def get_input(text):
    return input(text).strip()


def validate_input(text):
    while True:
        try:
            return int(get_input(text))
        except ValueError:
            print("Invalid number")


def get_date():
    while True:
        prompt = get_input("Enter date (YYYY-MM-DD): ")
        try:
            return datetime.strptime(prompt, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD, e.g. 2026-10-11")


def complete_task(content):
    if not content:
        print("No Available Task")
        return
    view_task(content)

    task_number = validate_input("\nEnter the task number to mark as completed: ")

    task_keys = list(content.keys())
    if 1 <= task_number <= len(task_keys):
        task_key = task_keys[task_number - 1]
        content[task_key]["status"] = "completed"
        print(f"\n{content[task_key]["task"]} has been marked completed")
    else:
        print("Invalid task number")


if __name__ == "__main__":
    main()
