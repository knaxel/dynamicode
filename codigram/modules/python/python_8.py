from codigram.modules.modules import Module

MODULE_ID = "python_8"

MODULE_DATA = {
    "title": "Module 8: I/O",
    "author": "Codigram",
    "author_uuid": "",
    "codepage_uuid": "7c862055-115f-4858-ac68-e6892dc18473",
    "date_created": "Aug 14, 2021 11:51 AM",
    "blocks": [
        {
            "name": "The Input Function",
            "text": "We’ve been using `print()` to output useful information, but this is only half of I/O, which stands for Input/Output. You may want your program to take input from a user and then print relevant information based on this input. You can use the `input()` function as shown to allow users to type strings as input:\n```    \nx = input()     \n```\nIf you want to add a prompt, you can add text in-between the parentheses:    \n```    \nx = input(‘What’s your name? Type here: ’)      \n```\nA user’s input will always be treated as a string unless you type cast it to a different data type.",
            "type": "TextBlock"
        },
        {
            "name": "String Formatting",
            "text": "A user’s input will often need to show up in some way in output. Since the input is a string by default, we can concatenate it with other strings in a print statement like shown:     \n```     \nname = input()     \nprint(“Hi ” + name)     \n```\nThere are much fancier ways of doing this that are useful for non-string values as well. Take a look at the following code.    \n```    \nx = “World!”     \nprint(f ‘Hello {x}’)    \n```\nLet’s break this down. We start by declaring a string variable called `x` which has a value of “World!” We then have a print statement which holds a string preceded by the character ‘f’. The f character is used to make the string inside the print statement a formatted string literal. By doing so, we can place variable names inside brackets to easily add them to the print statement, as shown above.\nNow take a look at this block of code.     \n```    \nname = “George”     \nprint(“Hi, my name is {0}”.format(name))     \n```\nWe can use the `format` method to insert values into strings just like before. Instead of putting the variable name in brackets, you put the index of the argument that is in the format method. For example, if we had .format(name, age) instead, we would use {0} to insert the name and {1} to insert the age.",
            "type": "TextBlock"
        },
        {
            "name": "Madlibs",
            "text": "We can make strings that are very dependent on user input with very little effort. The following program can be completed with just a single line of code! Fill out the format method so that all 6 values are determined by user input. Add prompts so that each value the user inputs is only a specific type of word - the first and fourth inputs should be adjectives, the second and fifth inputs should be colors, and the third and sixth inputs should be nouns. Then try it out for yourself!",
            "type": "TextBlock"
        },
        {
            "name": "Madlibs Activity",
            "code": "print('The {0} {1} {2} jumped over the {3} {4} {5}'.format())",
            "type": "CodeBlock"
        },
        {
            "name": "Check for Understanding",
            "text": "What output will the following code produce?    \n```    \n\ta = “b”     \n\tb = “c”     \n\tc = “d”     \n     \n\tprint(‘{1}{2}{0}{2}’.format(c,b,d,a))     \n```",
            "choices": [
                "cdba",
                "bbcd",
                "bcdc",
                "acbc",
                "Error"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Check for Understanding ",
            "text": "What output will the following code produce?    \n```    \n\ta = “b”    \n\tb = “c”    \n\tc = “d”    \n     \n\tprint(‘{1}{2}{0}{2}’.format(c,a,a))     \n```",
            "choices": [
                "ccdc",
                "bbdb",
                "acba",
                "ddbc",
                "Error"
            ],
            "type": "ChoiceBlock"
        }
    ]
}

MODULE_CHECKERS = {"test": "This is a placeholder while answer checking is developed. For now, DO NOT DELETE THIS!"}

NEXT_MODULE_ID = "python_9"


def get_module():
    return Module(MODULE_ID, MODULE_DATA, MODULE_CHECKERS, NEXT_MODULE_ID)
