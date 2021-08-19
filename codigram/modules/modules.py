from flask_login import current_user
from codigram.models import db, ModuleExercise


MODULES = {}
ORDERED_MODULE_IDS = []


class Module:
    def __init__(self, module_id, module_data, answer_checkers, next_module_id=None, required_modules=()):
        self.module_id = module_id
        self.blocks = module_data["blocks"]
        self.title = module_data["title"]
        self.answer_checkers = answer_checkers
        self.next_module_id = next_module_id
        self.required_modules = required_modules

    def get_json(self):
        return {
            "author": "Codigram",
            "title": self.title,
            "blocks": self.blocks,
            "codepage_type": "module"
        }

    def is_locked(self, user_exercises=None):
        if self.module_id == "python_5":
            print("here")
        if not user_exercises:
            user_exercises = ModuleExercise.query.filter_by(user_uuid=current_user.uuid).all()
        for module_id in self.required_modules:
            module = get_module(module_id)
            if module.get_progress(user_exercises=user_exercises) < 100:
                return True
        return False

    def get_quiz_block_data(self):
        quiz_blocks = {}
        module_exercises = ModuleExercise.query.filter_by(user_uuid=current_user.uuid, module_id=self.module_id).all()
        completed_exercises = [exercise.block_name for exercise in module_exercises]
        for quiz_block in self.answer_checkers:
            quiz_blocks[quiz_block] = quiz_block in completed_exercises
        return quiz_blocks

    def check_answer(self, block_name, data):
        if block_name not in self.answer_checkers:
            return False, ""
        success, message = self.answer_checkers[block_name](data)

        if success and not ModuleExercise.query.filter_by(user_uuid=current_user.uuid, module_id=self.module_id,
                                                          block_name=block_name).first():
            module_exercise = ModuleExercise(
                user_uuid=current_user.uuid,
                module_id=self.module_id,
                block_name=block_name
            )
            db.session.add(module_exercise)
            db.session.commit()

        return success, message

    def get_progress(self, user_exercises=None):
        if user_exercises:
            completed_exercises = len([exercise for exercise in user_exercises if exercise.module_id == self.module_id])
        else:
            completed_exercises = len(ModuleExercise.query.filter_by(
                user_uuid=current_user.uuid,
                module_id=self.module_id
            ).all())
        total_exercises = len(self.answer_checkers)

        if total_exercises > 0:
            return int(round(100 * completed_exercises/total_exercises))
        elif completed_exercises > 0:
            return 100
        else:
            return 0


def add_module(module):
    MODULES[module.module_id] = module
    ORDERED_MODULE_IDS.append(module.module_id)


def get_module(module_id):
    module = MODULES.get(module_id)
    if module and len(module.answer_checkers) == 0 and module.get_progress() == 0:
        empty_exercise = ModuleExercise(user_uuid=current_user.uuid, module_id=module_id, block_name="")
        db.session.add(empty_exercise)
        db.session.commit()
    return module


def get_all_modules():
    return [MODULES[module_id] for module_id in ORDERED_MODULE_IDS]


"""
HOW TO CHECK ANSWERS:

In each module, set the MODULE_CHECKERS variable to a dictionary. The keys are the names of the blocks that you
want to check answers for, and the values are functions (the functions themselves, so don't call them) that will
check the answer. Write the functions in the following way:

def check_answer(data):  # When the user clicks "Check Answer", this function will be called and passed the block data
    if [some condition]:
        return True, ""  # If the answer is correct, return this.
    else:
        return False, "An optional message as a hint"  # If the answer is incorrect, return this.
        
(Look at the python_1 and python_2 modules for simple examples)
        
------------------------
BLOCK DATA:

The answer checking functions will receive data from the block they are checking. This is the data returned by
each of the different types of blocks:

- TextBlock
{"text": "The text contained in the block", "block_type": "TextBlock", "name": "The name of the block"}

- CodeBlock (note that clicking the "Check Answer" button will not run the user's code - they must do that themselves)
{"block_type": "CodeBlock",
 "name": "The name of the block",
 "code": "The code that the user has written",
 "terminal": "The output of the code (from the most recent run)",
 "scope": {"var": "value"}  # "scope" is a dictionary of the global variables and their values from the most recent run
                            # (functions and classes not included)
                            
- ChoiceBlock
{"block_type": "ChoiceBlock", "name": "The name of the block", "text": "The text contained in the block",
 "value": "The selected answer"}
 
- ImageBlock
{"block_type": "ImageBlock", "name": "The name of the block", "text": "The text contained in the block",
 "src": "The image url"}
 
- SliderBlock
{"block_type": "SliderBlock", "name": "The name of the block", "text": "The text contained in the block",
 "lower": The lower bound of the slider (float),
 "upper": The upper bound of the slider (float),
 "default": The default value of the slider (float),
 "value": The user set value of the slider (float)
    
"""

# Simple answer checkers


def check_choice_answer(right_answer):
    def check_specific_answer(data):
        if data.get("block_type") == "ChoiceBlock" and data.get("value"):
            return data["value"] == right_answer, ""
    return check_specific_answer


# Load Modules

from codigram.modules.python import python_0
from codigram.modules.python import python_1
from codigram.modules.python import python_2
from codigram.modules.python import python_3
from codigram.modules.python import python_4
from codigram.modules.python import python_5
from codigram.modules.python import python_6
from codigram.modules.python import python_7
from codigram.modules.python import python_8
from codigram.modules.python import python_9
from codigram.modules.python import python_10
from codigram.modules.python import python_11


def load_modules():
    add_module(python_0.get_module())
    add_module(python_1.get_module())
    add_module(python_2.get_module())
    add_module(python_3.get_module())
    add_module(python_4.get_module())
    add_module(python_5.get_module())
    add_module(python_6.get_module())
    add_module(python_7.get_module())
    add_module(python_8.get_module())
    add_module(python_9.get_module())
    add_module(python_10.get_module())
    add_module(python_11.get_module())


load_modules()
