from codigram.modules.modules import Module

MODULE_ID = "python_4"
NEXT_MODULE_ID = "python_5"

MODULE_DATA = {
    "title": "Module 4: Arithmetic",
    "author": "Codigram",
    "author_uuid": "",
    "sandbox_uuid": "bb84f1e4-719c-46c9-9aca-f1cc33d600f7",
    "date_created": "Aug 12, 2021 05:55 PM",
    "blocks": [
        {
            "name": "Arithmetic Operators",
            "text": "Math is an essential part of coding that makes many software solutions possible. Not all mathematical functions are supported by default, but the ones that you are most familiar with are. Say we have a variable called counter and it’s set to 0. How could we set it to 1? We could do `counter = 1`, but as you may have guessed from the variable name, we want to increase its value regularly. This is where arithmetic operators come in, which allow for the most basic mathematical functions to be used. Instead of saying `counter = 1`, we can say `counter = counter + 1`. Now the value will always increase by 1 no matter what it was set to before. There are other shorthand ways of doing addition as well. For example, we could also say `counter+=1`. This also works for subtraction - we can say `counter = counter - 1` or `counter-=1`. The operator for multiplication is `*` and the operator for division is `/`.     \n       \nPython also has several operators that you may be unfamiliar with. The first is `%`, which is called a modulus. The modulus operator divides one number by another, and returns the remainder. For example, 5 % 4 is equal to 1 because 4 goes into 5 once, and 1 is the remainder. The next operator is `**`, which represents an exponent. 2**2, for example, is 4. The final operator is `//`, which is for floor division. We’ll go into more detail in the next section.     \n     \nIt’s important to note that the results of performing arithmetic with floats is different from with integers. For example, 3.0*3 is equal to 9.0, but 3*3 is 9.",
            "type": "TextBlock"
        },
        {
            "name": "Division",
            "text": "We established that there are two operators for division - `/` and `//`. Let’s say we have two variables, `a` and `b`, which are both floats. We’ll say `a` is 1.5 and `b` is 2.0. If we divided like usual by using `/`, we would have `a`/`b` = 0.75. However, we might not want a decimal number as our output. Say we only wanted integers (whole numbers) - we could say `a`//`b` = 0.0. The `//` operator performs floor division, which takes the result of a regular division and rounds it down (hence the use of the word floor). If the result was negative, the result would be rounded down away from zero, whereas a positive result would be rounded down towards zero. ",
            "type": "TextBlock"
        },
        {
            "name": "Adding Numbers vs Appending Strings",
            "text": "You will often see the arithmetic operators (`+`,`-`,`*`,`/`,`//`,`%`,`**`,`=`) used in other areas of coding. For example, we already saw that the way to assign a value to a variable is by using the equals sign. We also use some of these operators for building strings. Let’s consider the following variables.    \n```      \na = “Hello”     \nb = “ World!”       \n```\nWe can use the addition operator to append the word “ World!” to “hello”. So if we did `a = a + b`, we would get “Hello World!”. You cannot mix and match adding numbers and strings. For example, 1 + “2” will only result in an error.",
            "type": "TextBlock"
        },
        {
            "name": "Equations Activity",
            "text": "The code below has a series of incomplete expressions. Comments denote what the results of each expression should be. Finish the expressions so that the correct values are printed out by changing the value of `a` and `b`.",
            "type": "TextBlock"
        },
        {
            "name": "Equations Activity ",
            "code": "a = 0\nb = 0\n# This expression should return 3\nx = 17%a \n# This expression should return 7\ny = ((a**2) + b)//a   \n# This expression should return 0\nz = (b//6)     \nprint(x)\nprint(y)\nprint(z)",
            "type": "CodeBlock"
        },
        {
            "name": "Check for Understanding",
            "text": "Which of the following expressions is equal to 4.0?",
            "choices": [
                "7//2",
                "9%5",
                "16.0/4.0"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Check for Understanding ",
            "text": "Which of the following expressions is equal to 169?",
            "choices": [
                "13**2",
                "139-48",
                "567%365"
            ],
            "type": "ChoiceBlock"
        }
    ]
}

MODULE_CHECKERS = {"test": "This is a placeholder while answer checking is developed. For now, DO NOT DELETE THIS!"}


def get_module():
    return Module(MODULE_ID, MODULE_DATA, MODULE_CHECKERS, NEXT_MODULE_ID)
