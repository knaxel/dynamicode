from codigram.modules.modules import Module

MODULE_ID = "python_8"

MODULE_DATA = {
    "title": "Module 8: I/O",
    "author": "Codigram",
    "author_uuid": "3473989f-0e1f-4488-9e98-847da1969d41",
    "sandbox_uuid": "ea536da3-84bf-4b07-a34b-43befbff5ce8",
    "date_created": "Aug 05, 2021 04:15 PM",
    "blocks": [
        {
            "name": "Input Function",
            "text": "We’ve been using print() to output useful information, but this is only half of I/O - Input/Output. You may want your program to take input from a user and then print relevant information based on this input. You can use the input() function as shown to allow users to type anything as input:    \n     \n        x = input()        \n        \nIf you want to add a prompt, you can add text in-between the parentheses:        \n        \n        x = input(‘What’s your name? Type here: ’)        \n",
            "type": "TextBlock"
        },
        {
            "name": "String Formatting",
            "text": "A user’s input will often need to show up in some way in output. If the input was a string, we can also concatenate it to other strings in a print statement like shown:       \n       \n       name = input()       \n       print(“Hi “ + name)       \n       \nThere are much fancier ways of doing this that are useful for non-string values as well. Take a look at the following code.       \n       \n       x = “World!”       \n       print(f ‘Hello {x}’)       \n       \nLet’s break this down. We start by declaring a string variable called x whose value is “World!” We then have a print statement which holds a string preceded by the character ‘f’. The f character is used to make the string inside the print statement a formatted string literal. By doing so, we can place variable names inside brackets to easily add them to the print statement, as shown above.\nNow take a look at this block of code.       \n       \n       name = “George”       \n       print(“Hi, my name is {0}”.format(name))       \n       \nWe can use the format method to insert values into strings just like with the formatted string variables. Instead of putting the variable name in brackets, you put the index of the entry in the format method. For example, if we had `.format(name, age)` instead, we would use {0} to insert the name and {1} to insert the age.",
            "type": "TextBlock"
        },
        {
            "name": "Madlibs Activity",
            "text": "We can make strings that are very dependent on user input with very little effort. The following program can be completed with just a single line of code! Fill out the format method so that all 6 values are determined by user input. Add prompts so that each value the user inputs is only a specific type of word - the first and fourth inputs should be adjectives, the second and fifth inputs should be colors, and the third and sixth inputs should be nouns. Then try it out for yourself!",
            "type": "TextBlock"
        },
        {
            "name": "Madlibs Activity ",
            "code": "print('The {0} {1} {2} jumped over the {3} {4} {5}'.format())",
            "type": "CodeBlock"
        },
        {
            "name": "Check for Understanding 1",
            "text": "What output will the following code produce?\n\n\ta = “b”\n\tb = “c”\n\tc = “d”\n\n\tprint(‘{1}{2}{0}{2}’.format(c,b,d,a))",
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
            "name": "Check for Understanding 2",
            "text": "What output will the following code produce?\n\n\ta = “b”\n\tb = “c”\n\tc = “d”\n\n\tprint(‘{1}{2}{0}{2}’.format(c,a,a))",
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