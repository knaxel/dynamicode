from codigram.modules.modules import Module

MODULE_ID = "python_2"

MODULE_DATA = {
    "title": "Module 2: Introduction to Python 2",
    "author": "Codigram",
    "author_uuid": "",
    "sandbox_uuid": "d35598f1-5ae2-4e1c-9e37-371d3906b213",
    "date_created": "Aug 11, 2021 09:28 PM",
    "blocks": [
        {
            "name": "Print Statements",
            "text": "In the previous module, you wrote a program that produced an output of the phrase “Hello World!”. You accomplished this by using what is called a print statement. Although called different things across different languages, a print statement is a standard function that prints any words, phrases, or sentences to some sort of output interface, such as a terminal or a file. Throughout these modules, any output produced by print statements can be seen in the box below where you type code. The format for using a print statement is always the same: type `print(‘’)` and put whatever you would like to print in between the quotes. Almost anything with quotes around in it is considered a String in Python, but we will explain this in further detail in a future module. You can also print things like numbers with or without quotes, such as by typing `print()` and putting a number in between the parentheses. This will not work for words. Print statements are incredibly useful for giving programs a way of producing output that is meaningful to the programmer or a user.",
            "type": "TextBlock"
        },
        {
            "name": "Python Syntax",
            "text": "Syntax is a set of rules that govern the structure and usage of symbols, words, and code layout in a programming language. In many languages for example, every line of code must end with a semicolon. However, this is not true in Python. Python uses indentation to denote blocks of code. For example, take the program on the right:      \n```     \nif x < 0:        \n\tprint(“X is less than zero”)       \nprint(“Next line”)       \n```\nNote how the second line is indented compared to the first. That line of code will only execute if x is less than zero, whereas the line `print(“Next line”)` will always run because it is not indented, and thus not a part of that block of code. We say that the print statement `print(“X is less than zero”)` is \"in the scope\" of the if statement (you will learn more about if statements later).          \n         \nPython is also quite lenient when it comes to declaring variables, which you will explore in the next module. For example, in many languages, declaring a variable requires some kind of keyword, such as var. In Python, no keywords are necessary. Variables can be declared by writing the name of a variable and setting it equal to a value, like:       \n```     \nx = 0     \ny = “this is a string”     \nz = True      \n```\nBehind the scenes, Python will decide what kind of variable each declaration is. Note that variable names are case-sensitive, variable names cannot be a keyword, and String variables can be declared using single or double quotes.",
            "type": "TextBlock"
        },
        {
            "name": "Comments",
            "text": "It’s good practice to include notes in your code, for yourself or others, to explain what your code does. This can be accomplished with comments. Every comment must start with the `#` character, and anything written on that line after the `#` will be considered a comment and not be run as code.\n```      \n#The next line will not run.    \n#print(“Hello World!”)    \n#But the next line will.     \nprint(“Hello World!”)      \n```",
            "type": "TextBlock"
        },
        {
            "name": "Check for Understanding",
            "text": "Which of the following is a correct print statement in Python?",
            "choices": [
                "print(“Hello World!”)",
                "print(“Hello World!)",
                "print(Hello World!)"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Check for Understanding ",
            "text": "Which of these keywords is used to declare a variable in Python?",
            "choices": [
                "var",
                "int",
                "let",
                "const",
                "All of the above",
                "None of the above"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Check for Understanding  ",
            "text": "Comments are declared using the [blank] character.",
            "choices": [
                "$",
                "/",
                "#",
                "="
            ],
            "type": "ChoiceBlock"
        }
    ]
}

MODULE_CHECKERS = {"test": "This is a placeholder while answer checking is developed. For now, DO NOT DELETE THIS!"}

NEXT_MODULE_ID = "python_3"


def get_module():
    return Module(MODULE_ID, MODULE_DATA, MODULE_CHECKERS, NEXT_MODULE_ID)
