import copy

content = {
    "adcbf313-3729-47f2-a92d-d5bae8cc73e6": {
        "task": "play ball",
        "status": "completed",
        "priority": "low",
        "due_date": "2026-10-13",
    },
    "cabe09a8-f8ba-414a-b1c5-2b5d27549d68": {
        "task": "sleep",
        "status": "pending",
        "priority": "low",
        "due_date": "null",
    },
    "8ffdc663-e70d-4367-bd1e-18ef0ae854bc": {
        "task": "working on",
        "status": "completed",
        "priority": "High",
        "due_date": "null",
    },
    "dc198474-428b-41a7-910a-dc25bf5a1cfb": {
        "task": "test2",
        "status": "pending",
        "priority": "low",
        "due_date": "2026-11-11",
    },
}

copied = {}

for key, value in content.items():
    if content[key]["status"] == "pending":
        copied[key] = value
        print(copied)
