from codigram.modules.modules import Module

MODULE_ID = "python_10"

MODULE_DATA = {
    "title": "Module 10: Functions",
    "author": "Codigram",
    "author_uuid": "",
    "codepage_uuid": "2dabb8d7-0eb2-43b8-9d90-8b4869caaa8c",
    "date_created": "Aug 14, 2021 05:10 PM",
    "blocks": [
        {
            "name": "What is a Function?",
            "text": "A function is a block of code that will run when a call is made to it from somewhere else in a program. An often utilized function in Python is the main function. When coupled with a special if statement, the main function will always be the first function to run in a python file.    \n```     \ndef main():    \n\t...     \n     \nif __name__ == \"__main__\":     \n   \tmain()     \n```\nFunctions can make code much more readable and concise by taking commonly used blocks of code and condensing them down to one line function calls. You have already used a number of functions throughout these modules - `print()`, `sort()`, `len()`, etc. We called these functions methods because they are functions associated with classes and objects, but we will go over this more in a future module.",
            "type": "TextBlock"
        },
        {
            "name": "Defining Functions",
            "text": "To define a function, the `def` keyword is used, followed by the function name and parentheses. Any parameters that will provide the function with input go into the parentheses as shown below.     \n```    \ndef function_name():    \n\tprint(“This is a function”)     \n     \ndef function2_name(parameter_name):    \n\tprint(parameter)     \n```\nTo call these functions, just use the function names.     \n```     \nfunction_name()      \nfunction2_name(parameter_value)      \n```\nIt is important here to remember how scope can affect your code. If you were to call a custom function and try to access a variable created inside the main function, you would be unable to do so because that variable would not be in the scope of your custom function. An example is below.     \n```     \ndef function_name():     \n\tx = x + 1 # This would not work! x is not defined in the scope of function_name    \n     \ndef main():    \n\tx = 0     \n\tfunction_name()      \n```\nHowever, if you were to define a variable outside of both functions (a global variable), your function could access it since now it is in scope.    \n```    \ny = 0    \n     \ndef function_name():     \n\tprint(y) # This would work!      \n      \nfunction_name()      \n```\nYou can also pass values, called arguments, to a function, whether or not they are in scope.",
            "type": "TextBlock"
        },
        {
            "name": "Parameters and Arguments",
            "text": "Parameters and arguments give the advantage of being able to pass values (that may or may not be in scope) to functions without necessarily changing them. When we used `len()`, we passed in a string as input like this: `len(string_name)`. Doing so effectively created a copy of the string for the method to use. To define the parameters of a function, we put the names that we want to call them inside the parentheses of the function declaration.     \n```      \ndef name(parameter1, parameter2):    \n\t...    \n```\nWe then pass values to these parameters in the function call.     \n```    \nname(“value1”,”value2”)     \n```\nYou cannot pass more or less arguments than there are parameters. So in the case above, you must always pass two arguments. If you wish to add default parameters values in the case the function is called without arguments, you can add them by setting the parameter names equal to a value.    \n```     \ndef name(parameter=”default”):    \n\t...     \n```",
            "type": "TextBlock"
        },
        {
            "name": "The Pass and Return Keywords",
            "text": "Finally, let’s discuss two of Python’s many keywords: `pass` and `return`. `pass` is used whenever you don’t want to execute code. For example, if you want to declare an empty function but you haven’t written any code for it, you can simply put `pass` on a new line in the function. This can be used to prevent any errors from declaring an empty function.        \n```     \ndef name():    \n\tpass     \n ```\n`return` is used to “return” a value from a function to the original caller of that function. The example below shows how we can set a variable equal to a function call, and that function call can return a value that becomes the value of the variable. Once the line with return is run, the function will terminate - no lines of code after a return keyword will run, assuming they’re in the same block of code.\n```   \ndef name():    \n\treturn 2     \n    \nx = name()     \nprint(x) # Prints 2    \n```",
            "type": "TextBlock"
        },
        {
            "name": "Recursion",
            "text": "You may or may not have heard the term recursion before. In the field of computer science, recursive problems are problems that are solved by looking at smaller but identical problems and solving those. A common example of recursion is what is called a factorial. In math, if you have a number followed by an exclamation mark, that is the factorial of that number. Its value is itself multiplied by itself minus 1, and then multiplied by that minus 1, and so on until 1. For example, 4! is 4 times 3 times 2 times 1 (4 * 3 * 2 * 1), or 24.      \nYou may find it easier to understand recursion by writing recursive functions. Take a look at the function below.     \n```   \ndef function(x):     \n\tif(x==1):     \n\t\tprint(1)     \n\telse:     \n\t\tfunction(x-1)      \n```\nNotice how we call the function within itself when `x` is not equal to 1. Assuming we pass a positive integer to the function as an argument, the function will call itself using the argument minus 1 until the argument is actually equal to 1, at which point it will terminate. So if we originally called the function with an argument of 3, `function(x-1)` would be called, passing an argument of 2 to the function. If we provide a negative value (or zero) as an argument, this function would never terminate because the arguments being passed to the function would simply decrease to negative infinity and never reach 1.     \n       \nYour task will be to use a recursive function to calculate the factorial of a number as we described above. Remember that you should use conditional statements so that the function terminates at a certain point. The skeleton code is provided for you below.     ",
            "type": "TextBlock"
        },
        {
            "name": "Recursion Activity",
            "code": "def factorial(inputNumber):\n\tpass ",
            "type": "CodeBlock"
        },
        {
            "name": "Check for Understanding 1",
            "text": "What is wrong with the following code?\n```   \ndef mysteryFunc(y):    \n\tprint(“Input: “ + (x+y))    \n    \nx = 2    \nmysteryFunc(5)      \n```",
            "choices": [
                "x is not in scope in mysteryFunc",
                "x is declared after it is used in mysteryFunc",
                "x is not a string",
                "There is nothing wrong with the code"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Check for Understanding 2",
            "text": "What is wrong with the following code?\n```    \ndef mysteryFunc(z):    \n\tprint(“Input: “ + (x+z))     \n      \nx = 2    \nmysteryFunc(x)      \n```",
            "choices": [
                "x is not in scope in mysteryFunc",
                "x is declared after it is used in mysteryFunc",
                "x is not a string",
                "There is nothing wrong with the code"
            ],
            "type": "ChoiceBlock"
        }
    ]
}

MODULE_CHECKERS = {"test": "This is a placeholder while answer checking is developed. For now, DO NOT DELETE THIS!"}

NEXT_MODULE_ID = "python_11"


def get_module():
    return Module(MODULE_ID, MODULE_DATA, MODULE_CHECKERS, NEXT_MODULE_ID)
