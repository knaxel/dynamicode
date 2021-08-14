from flask_login import current_user
from codigram.models import db, ModuleExercise


MODULES = {}
ORDERED_MODULE_IDS = []


class Module:
    def __init__(self, module_id, module_data, module_checkers, next_module_id=None):
        self.module_id = module_id
        self.blocks = module_data["blocks"]
        self.title = module_data["title"]
        self.answer_checkers = module_checkers
        self.next_module_id = next_module_id

    def get_json(self):
        return {
            "author": "Codigram",
            "title": self.title,
            "blocks": self.blocks
        }

    def check_answer(self, block_name, data):
        if block_name in self.answer_checkers and self.answer_checkers[block_name](data):
            if not ModuleExercise.query.filter_by(user_uuid=current_user.uuid, module_id=self.module_id,
                                                  block_name=block_name).first():
                module_exercise = ModuleExercise(
                    user_uuid=current_user.uuid,
                    module_id=self.module_id,
                    block_name=block_name
                )
                db.session.add(module_exercise)
                db.session.commit()
            return True
        else:
            return False

    def get_progress(self):
        # This is potentially very inefficient
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


def get_module(module_id):
    module = MODULES.get(module_id)
    if module and len(module.answer_checkers) == 0 and module.get_progress() == 0:
        empty_exercise = ModuleExercise(user_uuid=current_user.uuid, module_id=module_id, block_name="")
        db.session.add(empty_exercise)
        db.session.commit()
    return module


def get_all_modules():
    return [MODULES[module_id] for module_id in ORDERED_MODULE_IDS]


load_modules()
