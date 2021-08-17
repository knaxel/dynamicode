from codigram.modules.modules import Module

MODULE_ID = "python_5"
NEXT_MODULE_ID = "python_6"

MODULE_DATA = {
    "title": "Module 5: Strings",
    "author": "Codigram",
    "author_uuid": "",
    "sandbox_uuid": "6f152499-62fd-4919-94cf-b4c17b367644",
    "date_created": "Aug 13, 2021 11:59 AM",
    "blocks": [
        {
            "name": "How to Make Strings",
            "text": "As mentioned in module 3, strings are made using single or double quotes. However, you can also layer these two types of quotes when making a string. Say you have a variable called `my_string` with a value of “Hello, I’m ‘Bob’”. If you print `my_string` out it will look like this: Hello, I’m ‘Bob’. This also works the other way around where the outermost quote is a single quote and the innermost quote is a double quote. If you want to layer more quotes inside another quote, you have to be careful of two things: 1. Make sure all of your quotes are closed and 2. Make sure that all inner quotes are the opposite of the outer quote (in other words, if you used double quotes for the outside, then you must use single quotes for all inner quotes and vice versa). The result of not following these two rules can lead to syntax errors.",
            "type": "TextBlock"
        },
        {
            "name": "Accessing Characters",
            "text": "To get a character from a string, you have to call the index (or position) of that character in the string using square brackets - `[ ]`. In Python, the beginning of the string always starts at the 0 index and therefore ends at an index that is one less than the length of the string. For example, the variable `statement = “Hello World”` has a length of 11 (spaces count as characters), but its index range is from 0 to 10. To get the o in Hello, you would type `statement[4]` and not `statement[5]`. You can also use negative indices in Python to access the characters from the end of the string. So -1 would be the last character, -2 would be the second-to-last character, and so on and so forth. In the same example, you can get the o from Hello using `statement[-7]`. You can also access subparts of a string by using `:` with the `[ ]`. To get “World” from `statement`, you can type `statement[6: ]`, and to get “Hello” from `statement` you can type `statement[ :4]`.",
            "type": "TextBlock"
        },
        {
            "name": "Getting String Length",
            "text": "To find the length of a string, you just need to use the `len()` function on the string variable. So to find the length of `statement`, you would do `len(statement)`, which would give you 11.",
            "type": "TextBlock"
        },
        {
            "name": "Sentence Activity",
            "code": "#Given the variable sentence, complete the tasks outlined in the comments below.\nsentence = \"Strings are so fun!\"\n#print the length of sentence on line 4\n\n#find and print out the word “fun” in sentence on line 6\n",
            "type": "CodeBlock"
        },
        {
            "name": "Check for Understanding",
            "text": "You can only make a string with single or double quotes, not both.",
            "choices": [
                "True",
                "False"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Check for Understanding ",
            "text": "If you do want to layer more quotes inside another quote, make sure that all ____ quotes are the ______ of the ______ quote.",
            "choices": [
                "inner; opposite; outer",
                "outer; same; inner"
            ],
            "type": "ChoiceBlock"
        }
    ]
}

MODULE_CHECKERS = {"test": "This is a placeholder while answer checking is developed. For now, DO NOT DELETE THIS!"}


def get_module():
    return Module(MODULE_ID, MODULE_DATA, MODULE_CHECKERS, NEXT_MODULE_ID)
