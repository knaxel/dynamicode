from codigram.modules.modules import Module

MODULE_ID = "python_0"

MODULE_DATA = {
        "title": "Module 0: Introduction to Programming",
        "author": "Codigram",
        "author_uuid": "",
        "sandbox_uuid": "386a0c4c-288c-4e0a-8849-f2a5cbbbd74e",
        "date_created": "Aug 11, 2021 08:47 PM",
        "blocks": [
            {
                "name": "Defining Programming",
                "text": "Think about how you would make a peanut butter and jelly sandwich. You would probably start by getting two slices of bread. You would then spread peanut butter on the slices, and finally spread the jelly on the slices as well. It wouldn't make much sense to start by spreading the jelly before getting the two slices of bread. You have to do each step in a particular order to make the sandwich. When you program, you are explaining to a computer what steps to perform and in what order to complete some task.       \n     \nProgramming is where a programmer (you) writes a program (a set of instructions) that a computer can perform. But how does the computer understand your program? Computers at their lowest level do not understand human language. They instead rely on 1s and 0s in order to do everything. Writing 1s and 0s to program would be tedious, confusing, and limiting for a programmer, so we instead use what are called programming languages.      \n      \nA programming language defines keywords, strings, and commands that can be written by a programmer and transformed into code that a computer can understand. Over the course of these modules, you will learn one of these programming languages, Python, but there are dozens more, each with their own strengths and drawbacks. ",
                "type": "TextBlock"
            },
            {
                "name": "Applications of Programming",
                "text": "What exactly can you do with programming? The possibilities grow every day as technology improves, but almost anything you do with your computer, your tablet, or your phone is enabled by programming. Programming allows you to play videogames, check the weather, write emails, and view this very webpage. Programming is used for robotics, animation, communication, manufacturing, and in every industry that uses computers. ",
                "type": "TextBlock"
            },
            {
                "name": "Check for Understanding",
                "text": "A program is a [blank].",
                "choices": [
                    "type of computer",
                    "set of instructions",
                    "group of coders"
                ],
                "type": "ChoiceBlock"
            },
            {
                "name": "Conclusion",
                "text": "At the end of each module, you will find a button that says complete. Clicking it completes the module and returns you to the modules page. You can return to any completed module at any time. Some modules may be more than one page, so this button will instead say continue.",
                "type": "TextBlock"
            }
        ]
    }

MODULE_CHECKERS = {}

NEXT_MODULE_ID = "python_1"


def get_module():
    return Module(MODULE_ID, MODULE_DATA, MODULE_CHECKERS, NEXT_MODULE_ID)
