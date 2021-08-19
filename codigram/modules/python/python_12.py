from codigram.modules.modules import Module

MODULE_ID = "python_12"
NEXT_MODULE_ID = None
REQUIRED_MODULES = ["python_11"]

MODULE_DATA = {
    "title": "Module 12: Data Structures",
    "author": "MattMoran01",
    "author_uuid": "6b8e8025-0595-4b55-9faf-801238ed4654",
    "codepage_uuid": "30326b6b-f2d1-4f2b-a219-b01889986667",
    "codepage_type": "sandbox",
    "date_created": "Aug 18, 2021 09:02 PM",
    "blocks": [
        {
            "name": "What is a Data Structure?",
            "text": "You have learned that variables can be used to store different kinds of information to be used later. You have also learned that lists are like variables that can store many values that can be retrieved individually or all at once. Lists are actually one of many different ways of data storage, which are called data structures. Data structures store data in different ways so that they can be used in different ways to meet tasks more efficiently. For example, lists are simple, one-dimensional data structures that provide easy access to certain data elements. Lists can also be sorted in different ways, which can be useful for many different situations. Imagine you are a teacher, and you have just given a test to your students. You have a very large class, and you want to easily see who passed the test and who failed it. By using the `sort()` function, you can arrange the scores into passing and failing groups, or perhaps alphabetically by the student’s names. Lists can be very versatile, but there are other data structures that each have their own strengths as well. We will explore some of the data structures that are unique to Python in this section.",
            "type": "TextBlock"
        },
        {
            "name": "Dictionaries",
            "text": "Dictionaries in Python are in many ways similar to dictionary books. With a physical dictionary, you can look up a certain word and find its definition. With Python dictionaries, you can store pairs of data that are in a key:value format. For example, let’s say you wanted to create a dictionary that describes yourself. You might want to store your name, your age, and your height. To do this, you would create several key:value pairs to do this - name:”John Doe”, age:55, height:”67 inches”. To declare a dictionary in code, you can type:     \n```    \ndictionary_name = {}     \n```\nYou can put any key value pairs inside the curly braces like this:    \n```     \nwhoAmI = {“name”:”John Doe”,”age”:55}     \n```\nNote that the name of each key must be in quotes, but the actual value assigned can be an integer, a string, or some other type of value.      \n     \nWe can access this data in a slightly different way compared to lists. If we wanted to access the “name” value in the previous example, we would do `dictionary_name[“name”]`, which returns “John Doe”. To add a new item to the dictionary, you can just use the same method.     \n```     \nx = whoAmI[“name”] # x is now “John Doe”     \nwhoAmI[“favoriteColor”] = “Blue” # Adds “favoriteColor”:”Blue” as a pair to the dictionary    \n```\nTo remove items, you can either use the `del` keyword or the `pop()` function.    \n```    \nwhoAmI = {“name”:”John Doe”,”age”:55}    \nwhoAmI.pop(“name”)     \ndel whoAmI[“age”]     \n# Dictionary is now empty     \n```\nTo change items, just use the same method you would use to add an item, but make sure the key is from the key:value pair you want to change.     ",
            "type": "TextBlock"
        },
        {
            "name": "Dream Car",
            "text": "Imagine you have been given the chance to design your dream car. The possibilities are endless, but you must make sure you know exactly what you want. Let’s make a dictionary called dreamCar and add some traits to it that you want your car to have. Below is a list of all the traits your car *must* have as well as the type of values they must be. Feel free to add any unlisted traits that you want.    \n- numOfWheels - Integer\n- color - String\n- hasTurbo - Boolean\n- length - String\n- height - String\n- gasTankSize - Float\n",
            "type": "TextBlock"
        },
        {
            "name": "Dream Car Activity",
            "code": "",
            "type": "CodeBlock"
        },
        {
            "name": "Tuples",
            "text": "Lists are very useful for holding a number of items of various types and making them easily accessible, but what if you wanted those values to not change? Tuples are similar to lists, except they are fixed in nature. Once created, elements cannot be added or removed from a tuple, and so the size of the tuple will never change. It is for this reason that tuples are called “immutable”, as opposed to being “mutable” like a list. Whenever you want to store information that you want to keep from accidentally being changed or removed, you can use a tuple.     \n    \nTo declare a tuple, use parentheses:     \n```    \nmyTuple = (‘a’,’b’,’c’)     \n```\nRemember, you cannot add or remove items from the tuple, but you can access the items from it just as you would with a list. So `myTuple[0]` would return ‘a’.     \n      \nIf you ever want to declare a one item tuple, you must add a comma after the item like this:     \n```    \nmyTuple=(‘a’,)    \n```\nTuples can store any data type, and multiple data types within the same tuple. Duplicates are allowed like with lists but unlike with dictionaries.",
            "type": "TextBlock"
        },
        {
            "name": "Sets",
            "text": "Sets are a way of storing multiple items in a single variable, like lists, dictionaries, and tuples. However, they are considered both unordered and immutable, so their items cannot be changed and you cannot access their items with indices like with lists or tuples. Additionally, duplicate items are not allowed. However, unlike tuples, you can add or remove items.     \n     \nTo declare a set, use curly braces like this:    \n```    \nmySet = {1,2,3}    \n```\nYou can get the length of a set using the `len()` function as usual. If you want to access the items, you must loop through them with a for loop.    \n```    \nfor item in mySet:    \n\tprint(item)    \n```\nRemember, since sets are unordered, the order in which the items are accessed by the for loop will be different every time.    \n     \nAlthough set items are unchangeable, you can add new items to the set using the `add()` method.   \n```    \nmySet = {1,2,3}    \nmySet.add(4)    \n```\nTo add one set to another, use the `update()` method.    \n```     \nmySet = {1,2,3}    \nmySet2 = {4,5,6}    \nmySet.update(mySet2)    \n```\nThere are also different ways to remove items.    \n      \nIf we use the `remove()` method, we can remove a specific item from the set. If it doesn’t exist, you will get an error message.    \n```     \nmySet = {“a”,”b”,”c”}    \nmySet.remove(“a”)     \n```\nIf we use the `discard()` method, we can also remove a specific item, but if it doesn’t exist, no error will be raised.     \n```     \nmySet = {“a”,”b”,”c”}    \nmySet.discard(“a”)   \n```\nThe `pop()` method can be used here as well, but it always removes the “last” item. Since sets are unordered, you will not know what this item is going to be.     \n```     \nmySet = {“a”,”b”,”c”}    \nmySet.pop()    \n```\nFinally, use the `clear()` method to remove all items from the set and the `del` keyword to delete a set.     \n```    \nmySet = {“a”,”b”,”c”}     \nmySet.clear()     \ndel mySet    \n```",
            "type": "TextBlock"
        },
        {
            "name": "Venn Diagrams",
            "text": "A Venn diagram is a type of diagram that can show traits that are common or uncommon between two sets.    \n     \nThe space in-between the two circles holds the traits that are common between the two sets. We can replicate this idea with sets.     \n     \nTo find the items that are common between two sets, we can use the `intersection()` method.    \n```     \nmySet = {“a”,”b”,”c”}     \nmySet2 = {“a”,”d”,”e”}    \nmySet3 = mySet.intersection(mySet2)    \n# print(mySet3) will give {“a”}    \n```\nThe function below takes in 3 sets as arguments. Fill out the function so that it returns a set that holds the items that all 3 argument sets have in common.",
            "type": "TextBlock"
        },
        {
            "name": "Check for Understanding 1",
            "text": "What kind of data type would be useful for keeping track of usernames and their associated passwords?",
            "choices": [
                "Lists",
                "Sets",
                "Dictionaries",
                "Tuples"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Check for Understanding 2",
            "text": "What kind of data type would be useful for storing the year of birth and year of death for a historical figure?",
            "choices": [
                "Lists",
                "Sets",
                "Dictionaries",
                "Tuples"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Check for Understanding 3",
            "text": "What kind of data type would be useful for keeping track of a store’s items and their related information (quantity, price, etc.)?",
            "choices": [
                "List of lists",
                "List of sets",
                "List of dictionaries",
                "List of tuples"
            ],
            "type": "ChoiceBlock"
        },
        {
            "name": "Venn Diagram Activity",
            "code": "def inCommon(set1,set2,set3):\n\tpass",
            "type": "CodeBlock"
        }
    ]
}

MODULE_CHECKERS = {"test": "This is a placeholder while answer checking is developed. For now, DO NOT DELETE THIS!"}


def get_module():
    return Module(MODULE_ID, MODULE_DATA, MODULE_CHECKERS, NEXT_MODULE_ID, REQUIRED_MODULES)
