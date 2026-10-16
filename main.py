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
        print()
        print(f"\n{"="*30}TO-DO List{"="*30}")
        print(
            ""
            "\n1. Add task\n"
            "2. View tasks\n"
            "3. Complete task\n"
            "4. Edit task\n"
            "5. Delete\n"
            "6. Filter tasks\n"
            "7. Exit\n"
            ""
        )

        prompt = validate_input("Enter an option: ")

        match prompt:
            case 1:
                add_task(content)
            case 2:
                view_task(content)
            case 3:
                complete_task(content)
            case 4:
                edit_task(content)
            case 5:
                delete_task(content)
            case 6:
                get_filtered_task(content)
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
    set_priority = get_input("Set task priority to h(High)/l(low): ")
    if set_priority in ("high" or "h"):
        priority = "high"
        print("priority set to high")
    elif set_priority in ("low" or "l"):
        priority = "low"
        print("priority set to low")
    else:
        priority = "low"
        print("Invalid option detected:\npriority set to low")

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
        "priority": priority,
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


def edit_task(content):
    if not content:
        print("No Available Task")
        return
    view_task(content)
    task_number = validate_input("\nEnter the task number you want to edit: ")
    task_keys = list(content.keys())
    if 1 <= task_number <= len(task_keys):
        task_key = task_keys[task_number - 1]
        print("\n1. Task\n2. Status\n3.Priority\n4.Due date")
        edit_option = validate_input("\nEnter option to edit: ")
        if edit_option == 1:
            content[task_key]["task"] = get_input("\nTitle: ")
            print(f"Task updated to: {content[task_key]["task"]}")
        elif edit_option == 2:
            if content[task_key]["status"] == "completed":
                content[task_key]["status"] = "pending"
                print("status set to pending")
            else:
                content[task_key]["status"] = "completed"
                print("status set to completed")
        elif edit_option == 3:
            if content[task_key]["priority"] == "low":
                content[task_key]["priority"] = "high"
                print("Priority set to high")
            else:
                content[task_key]["priority"] = "low"
                print("priority set to low")
        elif edit_option == 4:
            while True:
                add_date = get_input("is there a due date? [y/n]: ").strip().lower()
                if add_date == "y":
                    d = get_date()
                    today = date.today()
                    while d < today:
                        print("Date cannot be from the past.\nPick a present date!")
                        d = get_date()
                    content[task_key]["due_date"] = d.isoformat()
                    print("Date updated")
                    break

                elif add_date == "n":
                    content[task_key]["due_date"] = None
                    print("Date updated")
                    break
                else:
                    print("Invalid Input. type: [y/n]: ")
        else:
            print("Pick a valid option from [1-4]")


def get_filtered_task(content):
    if not content:
        print("No Available Task")
        return
    print(
        "Filter by:\n1. Status(pending)\n2. Status(completed)\n3. Priority(low)\n4. Priority(High)\n"
    )
    user_prompt = validate_input("Input Filter Method: ")

    if user_prompt == 1:
        filter_task(content, "status", "pending")
    elif user_prompt == 2:
        filter_task(content, "status", "completed")
    elif user_prompt == 3:
        filter_task(content, "priority", "low")
    elif user_prompt == 4:
        filter_task(content, "priority", "high")
    else:
        print("Invalid option.\nSelect from (1) - (4) to Filter by Status OR Priority")


def filter_task(content, field, target):
    copied = {}
    for key, value in content.items():
        if value[field] == target:
            copied[key] = value
    view_task(copied)


if __name__ == "__main__":
    main()
