from codigram.modules.modules import Module

MODULE_ID = "python_9"
NEXT_MODULE_ID = "python_10"

MODULE_DATA = {
    "title": "Module 9: Lists",
    "author": "Codigram",
    "author_uuid": "",
    "codepage_uuid": "9e19eaa7-9da4-4f85-aac4-6d340580bf5b",
    "date_created": "Aug 14, 2021 04:11 PM",
    "blocks": [
        {
            "name": "Declaring Lists",
            "text": "It’s often preferred to store related values together in coding to make it easier to access them and use them at the same time. In Python, we can use what is called a list. In other languages, it is often called an array or a vector. A list can store multiple values of any variable type, including other lists. Each value is referred to as an item (or an element in other languages). Lists can be declared by setting a variable name equal to items separated by commas within brackets, as shown.\n```    \nlist = [“value1”,”value2”,”value3”]     \n```",
            "type": "TextBlock"
        },
        {
            "name": "Accessing Elements",
            "text": "Recall that we could look at individual characters in a string by using brackets and the position of the character in the string, starting from 0. To access an item in a list, you can use `list_name[index]`, where index always starts at 0 for the first item.     \n```       \nlist=[1,3,5,7,9]      \n```\nSo `list[1]` would return 3, and `list[0]` would return 1.",
            "type": "TextBlock"
        },
        {
            "name": "Looping Through Lists",
            "text": "Also recall that there were multiple ways to iterate over all the characters in a string using a for loop. We can iterate over all the items in a list using the same two methods, as demonstrated below.    \n```    \nlist = [1,2,3]     \nfor i in range(0,3):     \n\tprint(list[i])     \n```\n```    \nlist2 = [1,2,3]    \nfor item in list2:     \n\tprint(item)      \n```",
            "type": "TextBlock"
        },
        {
            "name": "Adding and Deleting Items",
            "text": "There are various ways to add and remove items from lists. The first is the `append` method, which adds an item to the end of a list.    \n```    \nlist = [1,2]     \nlist.append(3)      \n# list = [1,2,3]     \n```\nThe second is the `insert` method, which lets you insert an item at a specific index. It pushes all items at and after that index over 1, so using the insert method does not replace items.       \n```     \nlist=[1,3]     \nlist.insert(1,2)     \n# list = [1,2,3]     \n```\nThe first parameter is the index at which the item will be inserted (1), and the value that is being inserted is the second parameter (2).    \nYou can append one list to another using the `extend` method as shown.      \n```     \nlist = [1,2,3]      \nlist2 = [4,5,6]     \nlist.extend(list2)     \n# print(list) will give [1,2,3,4,5,6]      \n```\nThere are also multiple methods for removing items. The `remove` method lets you choose exactly which item to remove.      \n```     \nlist=[‘a’,’b’,’c’]     \nlist.remove(‘a’)     \n# list is now [‘b’,’c’]     \n```\nThe `pop` method lets you choose the index of the item to remove.    \n```    \nlist=[‘a’,’b’,’c’]     \nlist.pop(2)    \n# list is now [‘a’,’b’]     \n```\nUsing `pop()` without an index just removes the last item in the list.    \nYou can also use the `del` keyword to delete items at particular indices.      \n```     \nlist=[‘a’,’b’,’c’]    \ndel list[0]    \n# list is now [‘b’,’c’]     \n```\nFinally, you can use the `clear` method to remove all items from a list. This does not delete the list, so you can continue to add and remove items from it.     \n```     \nlist=[‘a’,’b’,’c’]    \nlist.clear()    \n# list is now [ ]     \n```",
            "type": "TextBlock"
        },
        {
            "name": "Sorting",
            "text": "Python has its own method for sorting lists in ascending or descending order, if applicable.      \n```    \nlist=[‘a’,’d’,’b’]     \nlist.sort()      \n# The list is now sorted in alphabetical order.     \n    \nlist2=[5,2,9,-10]     \nlist2.sort(reverse=True)      \n# The list is now sorted in descending order.     \n```\nThe `sort` method also can take in a special parameter that lets you sort based on a function that you define. You will learn more about functions in the next module, but below is an example for reference.    \n```   \n# A function that returns whether or not the value is less than 10:     \ndef compFunc(e):    \n        return e < 10     \n     \nlist = [12, 3, 2, 17]    \n     \nlist.sort(key=compFunc)    \n```\nPrinting the list will output [12,17,3,2] because the list was sorted into two groups - numbers less than 10, and numbers greater than or equal to 10.      ",
            "type": "TextBlock"
        },
        {
            "name": "Swiss Cheese",
            "text": "If we want to actually manipulate the characters of a string, we can turn the string into a list, modify the items, and then turn the list back into a string. Below is some skeleton code that you should complete so that all of the outputted strings are correct.",
            "type": "TextBlock"
        },
        {
            "name": "Swiss Cheese Activity",
            "code": "def addHoles(originalString):\n\t# First, convert the string into a list using an add function of your choice.\n\t# Add a for loop that replaces each “a” character in the list with a “.“ (space) character in order to add the \"holes\".\n\t# Call the sort function on the list to sort each character alphabetically.\n\t# Convert the list back into a string and print it\n\naddHoles(\"abcdefg\")\naddHoles(\"03keodle\")\naddHoles(\"..cad\")",
            "type": "CodeBlock"
        },
        {
            "name": "Check for Understanding 1",
            "text": "What method will sort a list in ascending order?",
            "choices": [
                "list.sort(reverse=False)",
                "list.sort(reverse=True)",
                "list.sort()",
                "Both a and c",
                "Both b and c",
                "All of the above"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Check for Understanding 2",
            "text": "What method will remove the item at index 3 in a 4 item list?",
            "choices": [
                "list.pop(2)",
                "list.pop(3)",
                "list.pop()",
                "Both a and b",
                "Both b and c",
                "Both a, b, and c"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Check for Understanding 3",
            "text": "What is the output of the following code?\n```   \nlist = [‘g’,’d’,’e’,’t’,’r’]     \nfor counter in range(0,3):     \n\tprint(list[len(list)-counter-1])     \n```",
            "choices": [
                "rte",
                "gde",
                "ted",
                "etr",
                "det"
            ],
            "type": "ChoiceBlock"
        }
    ]
}

MODULE_CHECKERS = {"test": "This is a placeholder while answer checking is developed. For now, DO NOT DELETE THIS!"}


def get_module():
    return Module(MODULE_ID, MODULE_DATA, MODULE_CHECKERS, NEXT_MODULE_ID)
