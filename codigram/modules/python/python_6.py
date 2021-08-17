from codigram.modules.modules import Module

MODULE_ID = "python_6"
NEXT_MODULE_ID = "python_7"

MODULE_DATA = {
    "title": "Module 6: Conditionals",
    "author": "Codigram",
    "author_uuid": "",
    "codepage_uuid": "131c7649-7875-4b79-8463-6e2e6db1a045",
    "date_created": "Aug 13, 2021 02:32 PM",
    "blocks": [
        {
            "name": "Introduction",
            "text": "You will often find that you want your program to do different things depending on certain conditions. For example, a weather app will want to display that it’s snowing, raining, or sunny depending on the actual weather. So we use what are called conditionals, which are commands and statements that direct a program to a certain output depending on a certain input. Conditionals essentially control the “flow” of a program.",
            "type": "TextBlock"
        },
        {
            "name": "Conditional Operators",
            "text": "Much like with arithmetic, conditional expressions rely on conditional operators that are used to generate true and false values. These operators are > (greater than), < (less than), >= (greater than or equal to), <= (less than or equal to), == (equal to), and != (not equal to). Each of these operators require two values that are compared to each other using the operator. For example, if we compared 5 and 3 with the greater than operator, we would have 5 > 3, which is true. If we compared 7 and 9 with the equal to operator, we would have 7==9, which is false, but with the not equal to operator, we have 7!=9, which is true. These operators can compare variables to different kinds of values, including integers, strings, and booleans, in order to change the flow of the program.",
            "type": "TextBlock"
        },
        {
            "name": "If Statements",
            "text": "Say we only want to execute a certain line or block of code if the result of comparing a variable to a certain value is true. Let’s say it’s the variable `x`, and it can be any integer, positive or negative. We can write an if statement as shown.     \n```          \nif x > 0:    \n        print(“x is greater than zero”)    \nprint(“Next line”)     \n```\nIf we break this down, the `x` > 0 is the conditional expression that will determine the flow of the program. When `x` is greater than zero, the conditional statement is true, and so the print statement that is indented will run. If `x` is not greater than zero, the print statement that is indented will not run and will instead be ignored. The next print statement will run regardless of if `x` is greater than zero because it is not within the scope of the if statement, as it is not indented.     \n      \nWhat if we want to use multiple conditions in the same if statement? Say we have another variable `y` and we want `print(“x and y are greater than zero”)` to only run if both `x` and `y` are greater than zero. We can use the `and` keyword as shown:      \n```       \nif (x > 0 and y > 0):     \n\tprint(“x and y are greater than zero”)     \nprint(“Next line”)     \n```\nIt’s good practice to wrap multiple conditional expressions in parentheses, especially when you have more than two, or when you have conditional expressions used inside other conditional expressions. \nWhat if we want the print statement to run if at least one of the expressions is true? We can use the `or` keyword as shown:     \n```      \nif (x > 0 or y > 0):      \n\t\tprint(“x and y are greater than zero”)     \nprint(“Next line”)     \n ```\nWhat if we want the print statement to run if `x` is not greater than zero? As an alternative to using a different operator, we can use the `not` keyword as shown:     \n ```      \nif not x > 0:      \n\t\tprint(“x is not greater than zero”)      \nprint(“Next line”)\t    \n```",
            "type": "TextBlock"
        },
        {
            "name": "Nested If Statements",
            "text": "To make more choices within your program, you can nest if statements inside each other like the following:     \n```     \nif(x > 2):     \n\tif(x > 3):     \n\t\tprint(“x is greater than 3”)     \nprint(“x is greater than 2”)     \nprint(“Continuing...”)       \n```\nWrite a program using either nested if statements or keywords like `and`, `not`, and `or` that meet the following conditions: if `x` is less than 7 but greater than 0, print “A”. If `x` is less than 7 and less than zero, print “B”. If `x` is greater than 7, print “C”.",
            "type": "TextBlock"
        },
        {
            "name": "Nested If Statements Activity",
            "code": "",
            "type": "CodeBlock"
        },
        {
            "name": "If-Elif-Else",
            "text": "Our previous example used the conditional expression `x > 0` to determine if a print statement should be run. However, this single conditional does not cover all the possible values `x` can take on. Perhaps we want our code to do other things if `x` is less than zero, or equal to 0. We can use a if-elif-else statement to accomplish this. Say we want to print a certain statement if `x` is greater than zero and another only if `x` is less than or equal to zero. We can write the following code:     \n```     \nif(x>0):      \n\tprint(“X is greater than zero”)     \nelse:     \n\tprint(“X is not greater than zero”)     \n```\nWe use the `else` keyword for all cases not covered by the conditional expression in the if statement. If we wanted to run a line of code only if `x` is equal to zero, we can add the `elif` keyword:     \n```     \nif(x>0):    \n\tprint(“X is greater than zero”)     \nelif(x==0):      \n\tprint(“X is equal to zero”)      \nelse:     \n\tprint(“X is not greater than zero”)     \n```     \nWhenever we have multiple cases, we use `if` for the first and `elif` for the rest, while `else` is for all cases not covered by those statements.",
            "type": "TextBlock"
        },
        {
            "name": "Try/Except",
            "text": "Say we want to try to run a line of code, and if it generates an error, we want to run another line of code. Look at the following code:     \n```     \ntry:    \n\tprint(mysteryVar)     \nexcept:     \n\tprint(“An error occurred”)     \n```\nIf `mysteryVar` is not defined before these lines, then the print statement will fail and the line under the `except` keyword will run. If it doesn’t fail, the line under `except` will not run. If we want to run a line regardless of whether or not an error occurs, we can use the `finally` keyword:     \n```    \ntry:     \n\tprint(mysteryVar)     \nexcept:     \n\tprint(“An error occurred”)     \nfinally:     \n\tprint(“Moving on…”)\n```",
            "type": "TextBlock"
        },
        {
            "name": "Error Handling",
            "text": "The following function takes in a variable `mysteryVar` as input. Write a try-except-finally block of code to handle the possible errors that may arise from printing `mysteryVarStr`. Add the following code to the except block: try to type cast mysteryVarStr to an integer and print it. If mysteryVarStr is any other kind of data type, print “Error”. Hint: You can nest try-except blocks.",
            "type": "TextBlock"
        },
        {
            "name": "Error Handling Activity",
            "code": "def function(mysteryVar):\n  mysteryVarStr = str(mysteryVar)\n  try:\n  \tprint(mysteryVarStr+4)\n  except: \n  \t# Add code here\nfunction(4)\nfunction(\"4\")\nfunction(4.0)\nfunction(True)",
            "type": "CodeBlock"
        },
        {
            "name": "Check for Understanding 1",
            "text": "Which of the following conditional statements returns a value of false?",
            "choices": [
                "6!=6",
                "17>3",
                "(2**3) <= (3**2)"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Check for Understanding 2",
            "text": "What is the output of this code? \n```      \nif not(5 > 3 and 3 > 4):      \n\tprint(“Yes”)      \nelse:     \n\tprint(“No”)      \n```",
            "choices": [
                "Yes",
                "No",
                "None of the above / error"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Check for Understanding 3",
            "text": "Does the following code cover all possible cases?     \n```     \n# Let x be any number     \nif (x > 10):      \n\t...    \nelif(x < 10 and x > 0):     \n\t…     \nelif(x < 0):     \n\t...     \n```",
            "choices": [
                "Yes",
                "No"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Check for Understanding 4",
            "text": "What is the output of this code?\n```     \ny = “0”     \ntry:     \n\tprint(y + 5)      \nexcept:      \n\tprint(“Error”)      \nfinally:     \n\tprint(“Continuing”)     \n```\n",
            "choices": [
                "y+5",
                "\"05\"",
                "5",
                "Error Continuing",
                "Continuing"
            ],
            "type": "ChoiceBlock"
        }
    ]
}


MODULE_CHECKERS = {"test": "This is a placeholder while answer checking is developed. For now, DO NOT DELETE THIS!"}


def get_module():
    return Module(MODULE_ID, MODULE_DATA, MODULE_CHECKERS, NEXT_MODULE_ID)
