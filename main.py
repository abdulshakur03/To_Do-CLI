import json
from datetime import datetime


def main():

    try:
        with open("todo.json", "r") as file:
            content = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        content = []

    start(content)


def start(content):
    while True:
        print("TO-DO List")
        print(
            "1. Add task\n2. View tasks\n3. Complete task\n4. Edit task\n5. Delete task\n6. Filter tasks\n7. Exit"
        )

        prompt = validate_input("Enter an option: ")

        match prompt:
            case 1:
                add_task(content)
            case 7:
                print("operation canceled!")
                break
            case _:
                print("chose an option from 1-7")
        with open("todo.json", "w") as file:
            json.dump(content, file, indent=4)


def add_task(content):

    task = get_input("add task: ")
    content.append({"task": task, "date": datetime.now().strftime("%A, %B %d, %Y")})


def get_input(text):
    return input(text).strip()


def validate_input(text):
    while True:
        try:
            return int(get_input(text))
        except ValueError:
            print("Invalid number")


if __name__ == "__main__":
    main()
