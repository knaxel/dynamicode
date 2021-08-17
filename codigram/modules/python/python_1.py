from codigram.modules.modules import Module

MODULE_ID = "python_1"
NEXT_MODULE_ID = "python_2"

MODULE_DATA = {
    "title": "Module 1: Introduction to Python",
    "author": "Codigram",
    "author_uuid": "",
    "sandbox_uuid": "a1f03ab2-061f-4eac-89c2-ef1edb905005",
    "date_created": "Aug 11, 2021 09:17 PM",
    "blocks": [
        {
            "name": "What is Python?",
            "text": "In the previous module, you learned that a programming language is a computer language that both humans and computers can understand. There are many programming languages out there, including Python. Python is known for being particularly easy to understand and learn. The language was first developed in the 1980s and is one of the most popular programming languages today. To get to know it better, let's jump into your first coding activity!     \n     \nBelow this paragraph, you will find the code window where you will be able to write code for any activity or project. When you're ready to test code that you have written, you can press run (the green arrow) and whatever your code outputs will appear in the box below the code window. Let's write your first program now! Type the following into the code window: `print(\"Hello World!\")`. Press run when you're ready and see what happens.",
            "type": "TextBlock"
        },
        {
            "name": "Hello World! Activity",
            "code": "",
            "type": "CodeBlock"
        }
    ]
}


def check_code(data):
    if data.get("terminal") and data["terminal"] == "Hello World!\n":
        return True, ""
    return False, "Did you run your code before checking the answer?"


MODULE_CHECKERS = {"Hello World! Activity": check_code}


def get_module():
    return Module(MODULE_ID, MODULE_DATA, MODULE_CHECKERS, NEXT_MODULE_ID)
