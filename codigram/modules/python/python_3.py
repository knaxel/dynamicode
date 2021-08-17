from codigram.modules.modules import Module

MODULE_ID = "python_3"
NEXT_MODULE_ID = "python_4"

MODULE_DATA = {
    "title": "Module 3: Variables",
    "author": "Codigram",
    "author_uuid": "",
    "sandbox_uuid": "7e07132b-ef49-4846-8128-03e364827438",
    "date_created": "Aug 12, 2021 03:22 PM",
    "blocks": [
        {
            "name": "Variable Types",
            "text": "The most used and well known variable types are strings, integers, floats, and booleans. You’ve already learned a bit about strings from the last module, but to go into further detail here, strings are words, phrases or sentences that are bracketed by either double quotes or single quotes (ex: “Hi”, ‘Welcome’, “Come on in”). Integers (also called ints) and floats are similar in that they both store numbers, but what makes them different is that ints store whole numbers while floats store decimal numbers. So the number 15 would be an int but the number 8.5 would be a float. While the other variable types can have a range of values, the boolean type can only have two: True or False.",
            "type": "TextBlock"
        },
        {
            "name": "Creating a Variable",
            "text": "As mentioned in the previous module, variables in Python don’t need to be declared with a keyword or given a variable type. The variable’s type is automatically known once it is created. For example, if you were to simply type `x = False`, Python knows right away that the variable x is a boolean with a value of False.",
            "type": "TextBlock"
        },
        {
            "name": "Type Casting",
            "text": "There may be times when you want to change the type of one variable to another type. To do this you would use these constructor functions: `str()`, `int()`, and `float()`. Below are some examples of how you could use them.      \n```        \n\tx = int(3.8) #x will be 3      \n\ty = int(“5”) #y will be 5      \n```\nYou can only turn strings variables into ints if the string represents a whole number.   \n```     \n\tz = float(7) #z will be 7.0    \n\ta = float(“4.5”) #a will be 4.5     \n```\nYou can  only turn string variables into floats if the string represents a whole or decimal number.     \n```        \n\tb = str(2) #b will be “2”     \n\tc = str(3.9) #c will be “3.9”     \n```\nComplete the activity below to practice type casting.",
            "type": "TextBlock"
        },
        {
            "name": "Type Casting Activity",
            "code": "#print the variable below as a string\nmy_var = 30\n\n#print the variable below as an int\nsecond_var = \"11\"\n\n#try printing the variable below as a float\nthird_var = \"Typecast me!\"",
            "type": "CodeBlock"
        },
        {
            "name": "Naming Conventions",
            "text": "There are many naming conventions in the computer science world that give code an organized look so that you and whoever reads your code understands what is happening. One naming convention is called camelCase. As the name shows, the first letter of the first word is lowercase, but every word after that has a capital first letter. A more common naming convention in Python is separating each word of the variable by an underscore (ex: `my_variable = “underscores”`). This is more commonly used because the underscore acts as a blank space between words which allows readers to quickly understand the variable name.        \n         \nRegardless of how you name your variables, the most important rule is to make sure to name them according to what they are being used for. For example, say I want to make a variable to keep track of how many times I print something. Although naming it something as simple as `x` may be nice and quick, further down the line when you want to revisit the variable it may be harder to find, especially if there are many lines of code. So in order to prevent confusion or stress in the future, you should name the variable something like `counter`. This will not only make it easier to find the specific variable but it will also allow others reading your code to quickly realize that this variable is being used to count something.",
            "type": "TextBlock"
        },
        {
            "name": "Check for Understanding",
            "text": "What is the type of the variable `my_age = 20` ?",
            "choices": [
                "String",
                "Int",
                "Float",
                "Boolean"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Check for Understanding ",
            "text": "In Python, you have to declare a variable type when you’re making a variable.",
            "choices": [
                "True",
                "False"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Check for Understanding   ",
            "text": "What is the most important rule when naming a variable?",
            "choices": [
                "There is no rule.",
                "It must be camelCase.",
                "Its name should make it clear what its purpose is.",
                "It must have underscores between each word of the name."
            ],
            "type": "ChoiceBlock"
        }
    ]
}

MODULE_CHECKERS = {"test": "This is a placeholder while answer checking is developed. For now, DO NOT DELETE THIS!"}


def get_module():
    return Module(MODULE_ID, MODULE_DATA, MODULE_CHECKERS, NEXT_MODULE_ID)
