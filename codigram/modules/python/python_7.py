from codigram.modules.modules import Module

MODULE_ID = "python_7"

MODULE_DATA = {
    "title": "Module 7: Loops",
    "author": "Codigram",
    "author_uuid": "",
    "codepage_uuid": "10803e1e-0e34-4a87-8c28-179eade857ac",
    "date_created": "Aug 14, 2021 11:36 AM",
    "blocks": [
        {
            "name": "For Loops",
            "text": "Up until now, most, if not all, of the programs you have written have been relatively small. Many real-world programs need hundreds or even thousands of lines of code. Often these programs will need to perform the same tasks over and over again. For example, maybe you have a string variable and you need to use each character in that string separately. You can access a character in a string by doing `string_name[index]`, where index is the location of a character in that string. So say the string is 10 characters long (indices 0 through 9) and we need to look at each individual character. Rather than writing the same line of code 10 times, we can use what is called a for loop. A for loop will execute a block of code a specified number of times before the program moves on. There are multiple ways to declare for loops in Python, so we’ll start with one of the simplest ways:     \n```     \nfor counter in range(5):     \n\t# Code here     \n```\nThis for loop will execute its code block 5 times. If you were to print the value of `counter` during each iteration (each time the loop runs), you would get the numbers 0, 1, 2, 3, and 4, because `range(5)` means we are looping 5 times by incrementing the variable `counter` by 1 each time, starting at 0. An alternative to this is      \n```    \nfor counter in range(0,5):     \n\t# Code here     \n```\nThis is identical to the first for loop because using `range(number)` means our starting index defaults to 0. With this method we can make our starting and ending index anything we want. You can even put variables in the range like this: `range(varOne,varTwo)`. Just make sure they are integer values. \nIf we reconsider our string example from earlier, you may already see that we can just use `counter` to access the characters of the string by putting `string_name[counter]` in the for loop. But there is an even easier way to do this. If `str` is the name of our string, we can say     \n```     \nfor char in str:      \n\tprint(char)      \n```\nThis for loop will iterate over each character in the string, no matter how long the string is, and `char` holds the value of each character.",
            "type": "TextBlock"
        },
        {
            "name": "Powers of 2",
            "text": "Recall that you can access the value of the iterator of a for loop with code that is inside the loop. For example, you can access the value of `counter `with the following code:     \n```     \nfor counter in range(5):    \n\tprint(counter)     \n```\nAlso recall that the operator for doing exponents is `**`. So 3**2 is 9, because “3 squared” is 9. Let’s write a for loop that prints out the first ten powers of 2 by using the value of the iterator in the for loop as the exponent. For example, the first power of 2 is 2 to the zero power, or 2**0. The second power of 2 is 2^1, or 2**1.",
            "type": "TextBlock"
        },
        {
            "name": "Powers of 2 Activity",
            "code": "",
            "type": "CodeBlock"
        },
        {
            "name": "While Loops",
            "text": "For loops can repeat code for a particular number of times. But what if you need to repeat code an unknown number of times? This is where a while loop comes in. While loops depend on conditional statements to run - as long as the condition is true, the loop will run. Here’s an example:     \n```    \ncounter=0    \nwhile counter < 5:     \n\tcounter=counter+1     \n```\nThis example is somewhat unnecessary because it has the same functionality as a for loop, but note that if counter was not increased in the loop, it would run forever because `counter < 5`  would always be true. What if we wanted to exit the loop even if `counter < 5` was still true? We can use the `break` keyword like this:     \n```     \ncounter = 0    \nwhile counter < 5:    \n\tif counter > 1:     \n\t\tbreak    \n\tcounter = counter + 1     \n```\nThe loop will repeat until `counter` is greater than 1, at which point the if statement will be true and the `break` statement will run. When `break` runs, the loop stops even if the condition is still true. You can use the `break` keyword in for loops as well.",
            "type": "TextBlock"
        },
        {
            "name": "Nested Loops",
            "text": "Just like with if statements, you can nest different kinds of loops inside each other.    \n```     \nstr = “abc”    \nx = True    \nwhile(x == True):    \n\tfor char in str:     \n\t\tif char==”o”:    \n\t\t\tx = False    \n\t\t\tbreak     \n\tstr = “abco”     \n```\nHow many times do you think the while loop will run in this example?",
            "type": "TextBlock"
        },
        {
            "name": "Fibonacci Sequences",
            "text": "A sequence can be described as a set of numbers that follow a particular pattern. One famous example is the Fibonacci sequence, where each number is the sum of the previous two numbers. We start with our first number as 0 and our second number as 1. It follows that the third number is 1 because 0+1=1. The fourth number is 2 because 1+1=2, and the fifth number is 3 because 1+2=3. In the code window below, use a while loop to print out all Fibonacci numbers that are less than 611. Hint: You will need to save previous values to a variable so that you can calculate the next Fibonacci number in the sequence.",
            "type": "TextBlock"
        },
        {
            "name": "Fibonacci Activity",
            "code": "",
            "type": "CodeBlock"
        }
    ]
}

MODULE_CHECKERS = {"test": "This is a placeholder while answer checking is developed. For now, DO NOT DELETE THIS!"}

NEXT_MODULE_ID = "python_8"


def get_module():
    return Module(MODULE_ID, MODULE_DATA, MODULE_CHECKERS, NEXT_MODULE_ID)
