import os
import abc
from datetime import datetime
from codigram import db, login_manager, DATE_FORMAT
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
        return self.uuid

    def get_display_name(self):
        if self.display_name:
            return self.display_name
        return self.user_name

    def get_profile_picture_path(self):
        profile_path = f"/static/images/profiles/{self.uuid}.png"
        if os.path.isfile(profile_path):
            return profile_path
        return f"/static/images/profiles/default.png"


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

    def add_block(self, block):
        if not self.content:
            self.content = []
        self.content.append(block.get_json())

    def get_block(self, block_name):
        if not self.content:
            raise ValueError(f"Element with name {block_name} not found.")
        for block in self.content:
            if block["name"] == block_name:
                return block
        raise ValueError(f"Element with name {block_name} not found.")

    def get_json(self):
        return {
            "author": self.author.get_display_name(),
            "date_posted": self.created.strftime(DATE_FORMAT),
            "title": self.title,
            "blocks": self.content if self.content else []
        }

    def get_all_blocks(self):
        if not self.content:
            return []
        return self.content


class Sandbox(db.Model):
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(), nullable=False)
    author_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey("user.uuid"))
    is_public = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(JSON)

    def add_block(self, block):
        if not self.content:
            self.content = []
        self.content.append(block.get_json())

    def get_block(self, block_name):
        if not self.content:
            raise ValueError(f"Element with name {block_name} not found.")
        for block in self.content:
            if block["name"] == block_name:
                return block
        raise ValueError(f"Element with name {block_name} not found.")

    def get_json(self):
        return {
            "author": self.author.get_display_name(),
            "date_created": self.created.strftime(DATE_FORMAT),
            "title": self.title,
            "blocks": self.content if self.content else []
        }

    def get_all_blocks(self):
        if not self.content:
            return []
        return self.content


class Block:
    def __init__(self, name):
        self._name = name

    def set_name(self, new_name):
        self._name = new_name

    def get_name(self):
        return self._name

    @abc.abstractmethod
    def get_json(self):
        return {
            "name": self.get_name(),
            "type": None
        }


class TextBlock(Block):
    def __init__(self, name, text=None):
        super().__init__(name)
        self._text = text
        self._type = "TextBlock"

    def set_text(self, new_text):
        self._text = new_text

    def get_text(self):
        return self._text

    def get_json(self):
        return {
            "name": self.get_name(),
            "text": self.get_text(),
            "type": self._type
        }


class ChoiceBlock(TextBlock):
    def __init__(self, name, choices, text=None, selected=""):
        super().__init__(name, text=text)
        self._choices = choices
        self._selected = selected
        self._type = "ChoiceBlock"

    def set_choices(self, choices):
        if isinstance(choices, list):
            self._choices = choices

    def add_choice(self, choice, index):
        if choice not in self._choices:
            self._choices.insert(index, choice)

    def remove_choice(self, choice):
        if choice in self._choices:
            self._choices.remove(choice)

    def get_choices(self):
        return self._choices

    def set_selected(self, choice):
        if choice in self._choices:
            self._selected = choice

    def get_selected(self):
        return self._selected

    def reset_selected(self):
        self._selected = None

    def get_json(self):
        return {
            "name": self.get_name(),
            "text": self.get_text(),
            "choices": self.get_choices(),
            "selected": self.get_selected(),
            "type": self._type
        }


class CodeBlock(Block):
    def __init__(self, name, code=None):
        super().__init__(name)
        self._code = code
        self._type = "CodeBlock"

    def set_code(self, new_code):
        self._code = new_code

    def get_code(self):
        return self._code

    def get_json(self):
        return {
            "name": self.get_name(),
            "code": self.get_code(),
            "type": self._type
        }


def get_sample_post():
    post = Post.query.first()
    # user = User.query.first()
    # post = Post(title="Example Post")
    # user.posts.append(post)
    #
    # post.add_block(TextBlock("A", text="This is an example text block with some sample text."))
    # post.add_block(CodeBlock("B", code="for i in range(10):\n  print(i)"))
    # post.add_block(ChoiceBlock("C", ["Choice A", "Choice B", "Choice C"],
    #                text="This is an example text block with some sample text."))
    # post.add_block(CodeBlock("D", code="import post"))
    # db.session.commit()
    return post


def get_sample_sandbox():
    sandbox = Sandbox.query.first()
    # user = User.query.first()
    # sandbox = Sandbox(title="Example Sandbox")
    # user.sandboxes.append(sandbox)
    #
    # sandbox.add_block(TextBlock("A", text="This is an example text block with some sample text."))
    # sandbox.add_block(CodeBlock("B", code="for i in range(10):\n  print(i)"))
    # sandbox.add_block(ChoiceBlock("C", ["Choice A", "Choice B", "Choice C"],
    #                   text="This is an example text block with some sample text."))
    # sandbox.add_block(CodeBlock("D", code="import post"))
    # db.session.commit()
    return sandbox
