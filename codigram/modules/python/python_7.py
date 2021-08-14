from codigram.modules.modules import Module

MODULE_ID = "python_7"

MODULE_DATA = {
    "title": "Module 7: Loops",
    "author": "Codigram",
    "author_uuid": "3473989f-0e1f-4488-9e98-847da1969d41",
    "sandbox_uuid": "d2285df3-bb71-4bb4-b1f1-2c416948dd0e",
    "date_created": "Aug 04, 2021 08:25 PM",
    "blocks": [
        {
            "name": "For Loops",
            "text": "Up until now, most, if not all, of the programs you have written have been relatively small. Many real-world programs may need hundreds or even thousands of lines of code. Often these programs will need to perform the same tasks over and over again. For example, maybe you have a string variable and you need to use each character in that string separately. You can access a character in a string by doing variable_name[index], where index is the location of a character in that string. Note that indices always start at 0, not 1, but we’ll cover this again in the Lists module. So say the string is 10 characters long (indices 0 through 9) and we need to look at each individual character. Rather than writing the same lines of code 10 times, we can use what is called a for loop. A for loop will execute a block of code a specified number of times before finishing. There are multiple ways to declare for loops in Python, so we’ll start with one of the simplest ways:    \n     \n        for i in range(5):     \n\t        # Code here      \n      \nThis for loop will execute its code block 5 times. If you were to print the value i during each iteration (each time the loop runs), you would get the numbers 0, 1, 2, 3, and 4, because range(5) means we are looping 5 times by incrementing the variable i by 1 each time. An alternative to this is      \n     \n         for i in range(0,5):     \n\t        # Code here     \n         \nThis is identical to the first for loop because using range(number) means our starting index defaults to 0. With this method we can make our starting and ending index anything we want. You can even put variables in the range like this: range(x,y). Just make sure they are integer values. \nIf we reconsider our string example from earlier, you may already see that we can just use i to access the characters of the string by putting string_name[i] in the for loop. But there is an even easier way to do this. If str is the name of our string, we can say      \n      \n        for x in str:     \n\t        print(x)     \n      \nThis for loop will iterate over each character in the string, no matter how long the string is, and x holds the value of each character.  ",
            "type": "TextBlock"
        },
        {
            "name": "While Loops",
            "text": "For loops can repeat code for a particular number of times. But what if you need to repeat code an unknown number of times? This is where a while loop comes in. While loops depend on conditional statements to run - as long as the condition is true, the loop will run. Here’s an example:    \n      \n        i=0    \n        while i < 5:     \n\t        i=i+1    \n      \nThis example is somewhat unnecessary because it has the same functionality as a for loop, but note that if i was not increased in the loop, it would run forever because i would always be less than 5. What if we wanted to exit the loop even if i < 5 was still true? We can use the break keyword like this:     \n     \n         i = 0    \n         while i < 5:    \n\t         if i > 1:    \n\t\t         break    \n\t         i = i + 1    \n         \nThe loop will repeat until i is greater than or equal to 2, at which point i > 1 will be true and the break statement will run. When break runs, the loop stops even if the condition is still true. You can use the break keyword in for loops as well.",
            "type": "TextBlock"
        },
        {
            "name": "Nested Loops",
            "text": "Just like if statements, you can nest different kinds of loops inside each other.     \n      \n        str = “abc”    \n        x = True    \n        while(x == True):    \n\t        for x in str:    \n\t\t        if x==”o”:   \n\t\t\t        x = False    \n\t\t\t        break   \n\t        str = “abco”   \n    \nHow many times do you think the while loop will run in this example?",
            "type": "TextBlock"
        },
        {
            "name": "Activity: Fibonacci",
            "text": "A sequence can be described as a set of numbers that follow a particular pattern. One famous example is the Fibonacci sequence, where each number is the sum of the previous two numbers. We start with our first number as 0 and our second number as 1. It follows that the third number is 1 because 0+1=1. The fourth number is 2 because 1+1=2, and the fifth number is 3 because 1+2=3. In the code window, use a for loop to print out the first 15 Fibonacci numbers. Hint: You will need to save previous values to a variable so that you can calculate the next Fibonacci number in the sequence.",
            "type": "TextBlock"
        },
        {
            "name": "Fibonacci Activity ",
            "code": "",
            "type": "CodeBlock"
        }
    ]
}

MODULE_CHECKERS = {"test": "This is a placeholder while answer checking is developed. For now, DO NOT DELETE THIS!"}

NEXT_MODULE_ID = "python_8"


def get_module():
    return Module(MODULE_ID, MODULE_DATA, MODULE_CHECKERS, NEXT_MODULE_ID)
