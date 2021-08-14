from codigram.modules.modules import Module

MODULE_ID = "python_9"

MODULE_DATA = {
    "title": "Module 9: Lists",
    "author": "Matt01",
    "author_uuid": "3473989f-0e1f-4488-9e98-847da1969d41",
    "sandbox_uuid": "3f23b12c-df8c-49e9-93e4-bdc3b6809173",
    "date_created": "Aug 05, 2021 04:38 PM",
    "blocks": [
        {
            "name": "Declaring Lists",
            "text": "It’s often preferred to store related values together in a single variable. In Python, this is called a list. In other languages, it is often called an array or a vector. A list can store multiple values of any variable type, including other lists. Each value is referred to as an item (or an element in other languages). Lists can be declared by setting a variable name equal to items separated by commas within brackets, as shown.    \n     \n        list = [“value1”,”value2”,”value3”]        ",
            "type": "TextBlock"
        },
        {
            "name": "Accessing Items",
            "text": "Recall that we could look at individual characters in a string by using brackets and the position of the character in the string, starting from 0. To access an item in a list, you can use list_name[index], where index starts at 0 for the first item.     \n     \n        list=[1,3,5,7,9]        \n        \nSo `list[1]` would return 3, and `list[0]` would return 1.",
            "type": "TextBlock"
        },
        {
            "name": "Looping Through Lists",
            "text": "Also recall that there were multiple ways to iterate over all the characters in a string using a for loop. We can iterate over all the items in a list using the same two methods, as demonstrated below.   \n    \n        list = [1,2,3]        \n        for i in range(0,3):        \n                print(list[i])        \n        \n        list2 = [1,2,3]        \n        for x in list2:        \n\t        print(x)        ",
            "type": "TextBlock"
        },
        {
            "name": "Adding and Deleting Items",
            "text": "There are various ways to add and remove items from lists. The first is the append method, which adds an item to the end of a list.     \n     \n        list = [1,2]        \n        list.append(3)        \n        # list = [1,2,3]        \n        \nThe second is the insert method, which lets you insert an item at a specific index. It pushes all items at and after that index over 1, so using the insert method does not replace items.        \n        \n        list=[1,3]        \n        list.insert(1,2)        \n        \nThe first parameter is the index at which the item will be inserted (1), and the value that is being inserted is the second parameter (2).        \nYou can append one list to another using the extend method as shown.        \n        \n        list = [1,2,3]        \n        list2 = [4,5,6]        \n        list.extend(list2)        \n        # print(list) will give [1,2,3,4,5,6]        \n        \nThere are also multiple methods for removing items. The remove method lets you choose exactly which item to remove.        \n        \n        list=[‘a’,’b’,’c’]        \n        list.remove(‘a’)        \n        # list is now [‘b’,’c’]        \n        \nThe pop method lets you choose the index of the item to remove.        \n        \n        list=[‘a’,’b’,’c’]        \n        list.pop(2)        \n        # list is now [‘a’,’b’]        \n        \nUsing pop() without an index just removes the last item in the list.\nYou can also use the del keyword to delete items at particular indices.        \n        \n        list=[‘a’,’b’,’c’]        \n        del list[0]        \n        # list is now [‘b’,’c’]        \n\nFinally, you can use the clear method to remove all items from a list. This does not delete the list, so you can continue to add and remove items from it.        \n        \n        list=[‘a’,’b’,’c’]        \n        list.clear()        \n        # list is now [ ]        ",
            "type": "TextBlock"
        },
        {
            "name": "Sorting",
            "text": "Python has its own method for sorting lists in ascending or descending order, if applicable.     \n     \n        list=[‘a’,’d’,’b’]        \n        list.sort()        \n        # The list is now sorted in alphabetical order.        \n        \n        list2=[5,2,9,-10]        \n        list2.sort(reverse=True)        \n        # The list is now sorted in descending order.        \n        \nThe sort method also can take in a special parameter that lets you sort based on a function that you define. You will learn more about functions in the next module, but below is an example for reference.        \n        \n        # A function that returns whether or not the value is less than 10:        \n        def compFunc(e):        \n                return e < 10        \n        \n        list = [12, 3, 2, 17]        \n        list.sort(key=compFunc)        \n        \n# print(list) will output [12,17,3,2] because the list was sorted into two groups - numbers less than 10, and numbers greater than or equal to 10.        ",
            "type": "TextBlock"
        },
        {
            "name": "Strings are Lists",
            "text": "Recall that we can access characters of a string using string_name[index]. Notice how this is identical to how we access items in a list. This is because strings are actually arrays (lists) of characters. So the length method works on both strings and lists.",
            "type": "TextBlock"
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
            "text": "What method will remove the item at index 3 in a 4 element list?",
            "choices": [
                "list.pop(2)",
                "list.pop(3)",
                "list.pop()",
                "Both a and b",
                "Both b and c",
                "All of the above"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Check for Understanding 3",
            "text": "What is the output of the following code?\n\n        list = [‘g’,’d’,’e’,’t’,’r’]        \n        for i in range(0,3):        \n\t        print(list[len(list)-i-1])        ",
            "choices": [
                "r t e",
                "g d e",
                "t e d",
                "e t r ",
                "d e t"
            ],
            "type": "ChoiceBlock"
        }
    ]
}

MODULE_CHECKERS = {"test": "This is a placeholder while answer checking is developed. For now, DO NOT DELETE THIS!"}

NEXT_MODULE_ID = "python_10"


def get_module():
    return Module(MODULE_ID, MODULE_DATA, MODULE_CHECKERS, NEXT_MODULE_ID)
