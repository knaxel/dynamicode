from codigram.modules.modules import Module

MODULE_ID = "python_10"

MODULE_DATA = {
    "title": "Module 10: Functions",
    "author": "Codigram",
    "author_uuid": "3473989f-0e1f-4488-9e98-847da1969d41",
    "sandbox_uuid": "13ffa4cf-8054-4542-938b-626c8d1f21e2",
    "date_created": "Aug 05, 2021 05:18 PM",
    "blocks": [
        {
            "name": "What is a Function?",
            "text": "A function is a block of code that will run when it is called from somewhere else in a program. An often utilized function in Python is the main function. When coupled with a special if statement, the main function will always be the first function to run in a python file.    \n      \n        def main():        \n                pass        \n        \n        if __name__ == \"__main__\":\n                main()\n        \nFunctions can make code much more readable and concise by taking commonly used blocks of code and condensing them down to one line function calls. You have already used a number of functions throughout these modules - `print()`, `sort()`,`len()`, etc. We called these functions methods because they are functions associated with classes and objects, but we will go over this more in a future module.",
            "type": "TextBlock"
        },
        {
            "name": "Defining Functions",
            "text": "To define a function, the def keyword is used, followed by the function name and parentheses. Any parameters that will provide the function with input go into the parentheses as shown below.    \n    \n        def function_name():        \n                print(“This is a function”)        \n        \n        def function2_name(parameter_name):        \n\t        print(parameter)        \n        \nTo call these functions, just use the function names.        \n        \n        function_name()        \n        function2_name(parameter_value)        \n        \nIt is important here to remember how scope can affect your code. If you were to call a custom function and try to access a variable created inside the main function, you would be unable to do so because that variable would not be in the scope of your function. An example is below.        \n        \n        def function_name():        \n\t        x = x + 1 # This would not work!        \n        \n        def main():        \n\t        x = 0\n\t        function_name()\n        \nHowever, if you were to define a variable outside of both functions (a global variable), your function could access it since now it is in scope.        \n        \n        y = 0        \n        \n        def function_name():        \n\t        print(y) # This would work!        \n        \n        function_name()        ",
            "type": "TextBlock"
        },
        {
            "name": "Parameters and Arguments",
            "text": "Parameters give the advantage of being able to pass values (that may or may not be in scope) to functions without necessarily changing them. When we used len(), we passed in a string as input like this: len(string_name). Doing so effectively created a copy of the string for the method to use. To define the parameters of a function, we put the names that we want to call them inside the parentheses of the function declaration.     \n     \n        def name(parameter1, parameter2):        \n                pass        \n        \nWe then pass values to these parameters in the function call.        \n        \n        name(“value1”,”value2”)        \n        \nYou cannot pass more or less values than there are parameters. So in the case above, you must always pass two parameters. If you wish to add default parameters values in the case the function is called without arguments, you can add them by setting the parameter names equal to a value.        \n        \n        def name(parameter=”default”):        \n                pass        ",
            "type": "TextBlock"
        },
        {
            "name": "The Pass and Return Keyword",
            "text": "Finally, let’s discuss two of Python’s many keywords: pass and return. Pass is used whenever you don’t want to execute code. For example, if you want to declare an empty function but you haven’t written any code for it, you can simply put “pass” on a new line in the function. This can be used to prevent any errors from declaring an empty function.      \n      \nReturn is used to “return” a value from a function to the original caller of that function. The example below shows how we can set a variable equal to a function call, and that function call can return a value that becomes the value of the variable. Once the line with return is run, the function will terminate - no lines of code after a return keyword will run, assuming they’re in the same block of code.    \n     \n        def name():        \n                return 2        \n        \n        x = name()        \n        print(x) # Prints 2        ",
            "type": "TextBlock"
        },
        {
            "name": "Recursion Activity",
            "text": "You may or may not have heard the term recursion before. In the field of computer science, recursive problems are problems that are solved by solving smaller but identical problems. A common example of recursion is what is called a factorial. In math, if you have a number followed by an exclamation mark, that is the factorial of that number, and its value is the first value multiplied by itself minus 1, and then multiplied by that minus 1, and so on until 1. For example, 4! is 4 times 3 times 2 times 1, or 24.         \n        \nYou may find it easier to understand recursion by writing recursive functions. Take a look at the function below.      \n\n        def function(x):        \n        if(x==1):        \n                print(1)        \n        else:        \n                function(x-1)        \n        \nNotice how we call the function within itself when x is not equal to 1. Assuming we pass a positive value to the function, the function will call itself using the argument minus 1 until the argument is 1, where it will terminate. If we gave a negative value (or zero), this function would never terminate because the arguments being passed to the function would simply decrease to negative infinity and never reach 1.        \n        \nYour task will be to use a recursive function to calculate the factorial of a number as we described above. Remember that you should use conditional statements so that the function terminates at a certain point. The skeleton code is provided for you below.        \n",
            "type": "TextBlock"
        },
        {
            "name": "A",
            "code": "def factorial(inputNumber):\n\tpass \n  \n  \n  ",
            "type": "CodeBlock"
        }
    ]
}

MODULE_CHECKERS = {"test": "This is a placeholder while answer checking is developed. For now, DO NOT DELETE THIS!"}

NEXT_MODULE_ID = "python_11"


def get_module():
    return Module(MODULE_ID, MODULE_DATA, MODULE_CHECKERS, NEXT_MODULE_ID)
