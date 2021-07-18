from datetime import datetime
from codigram import db, login_manager
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid


@login_manager.user_loader
def load_user(user_uuid):
    return User.query.get(user_uuid)


class User(db.Model, UserMixin):
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = db.Column(db.String(32), unique=True, nullable=False)
    display_name = db.Column(db.String(32))
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    joined = db.Column(db.DateTime, nullable=False, default=datetime.now)
    bio = db.Column(db.Text)
    last_name_change = db.Column(db.DateTime, nullable=False, default=datetime.now)

    posts = db.relationship("Post", backref="author")
    sandboxes = db.relationship("Sandbox", backref="author")

    def get_id(self):
           return (self.uuid)
    def get_display_name(self):
        if self.display_name:
            return self.display_name
        return self.user_name


class Post(db.Model):
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    author_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey("user.uuid"))
    is_public = db.Column(db.Boolean, nullable=False, default=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_edit = db.Column(db.DateTime)
    title = db.Column(db.String(256), nullable=False)
    tags = db.Column(db.ARRAY(UUID(as_uuid=True)))
    likes = db.Column(db.Integer, nullable=False, default=0)
    content = db.Column(JSON, nullable=False)


class Sandbox(db.Model):
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    author_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey("user.uuid"))
    is_public = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text)


# class Post:
#     def __init__(self, author, date_posted, title, blocks=None):
#         self.author = author
#         self.date_posted = date_posted
#         self.title = title
#         self.blocks = blocks or []
#
#     def add_block(self, block):
#         self.blocks.append(block)
#
#     def get_block(self, block_name):
#         for block in self.blocks:
#             if block.get_name() == block_name:
#                 return block
#         raise ValueError(f"Element with name {block_name} not found.")
#
#     def get_json(self):
#         return {
#             "author": self.author,
#             "date_posted": self.date_posted,
#             "title": self.title,
#             "blocks": [block.get_json() for block in self.blocks]
#         }
#
#
# class Block:
#     def __init__(self, name):
#         self._name = name
#
#     def set_name(self, new_name):
#         self._name = new_name
#
#     def get_name(self):
#         return self._name
#
#     @abc.abstractmethod
#     def get_json(self):
#         return {
#             "name": self.get_name(),
#             "type": None
#         }
#
#
# class TextBlock(Block):
#     def __init__(self, name, text=None):
#         super().__init__(name)
#         self._text = text
#         self._type = "TextBlock"
#
#     def set_text(self, new_text):
#         self._text = new_text
#
#     def get_text(self):
#         return self._text
#
#     def get_json(self):
#         return {
#             "name": self.get_name(),
#             "text": self.get_text(),
#             "type": self._type
#         }
#
#
# class ChoiceBlock(TextBlock):
#     def __init__(self, name, choices, text=None, selected=""):
#         super().__init__(name, text=text)
#         self._choices = choices
#         self._selected = selected
#         self._type = "ChoiceBlock"
#
#     def set_choices(self, choices):
#         if isinstance(choices, list):
#             self._choices = choices
#
#     def add_choice(self, choice, index):
#         if choice not in self._choices:
#             self._choices.insert(index, choice)
#
#     def remove_choice(self, choice):
#         if choice in self._choices:
#             self._choices.remove(choice)
#
#     def get_choices(self):
#         return self._choices
#
#     def set_selected(self, choice):
#         if choice in self._choices:
#             self._selected = choice
#
#     def get_selected(self):
#         return self._selected
#
#     def reset_selected(self):
#         self._selected = None
#
#     def get_json(self):
#         return {
#             "name": self.get_name(),
#             "text": self.get_text(),
#             "choices": self.get_choices(),
#             "selected": self.get_selected(),
#             "type": self._type
#         }
#
#
# class CodeBlock(Block):
#     def __init__(self, name, code=None):
#         super().__init__(name)
#         self._code = code
#         self._type = "CodeBlock"
#
#     def set_code(self, new_code):
#         self._code = new_code
#
#     def get_code(self):
#         return self._code
#
#     def get_json(self):
#         return {
#             "name": self.get_name(),
#             "code": self.get_code(),
#             "type": self._type
#         }
#
#
# def get_sample_post():
#     post = Post("Paolo", "Thursday", "Example Post")
#     post.add_block(TextBlock("A", text="This is an example text block with some sample text."))
#     post.add_block(CodeBlock("B", code="for i in range(10):\n  print(i)"))
#     post.add_block(ChoiceBlock("C", ["Choice A", "Choice B", "Choice C"],
#                                text="This is an example text block with some sample text."))
#     post.add_block(CodeBlock("D", code="import post"))
#     return post