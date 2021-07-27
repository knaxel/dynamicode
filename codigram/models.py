import os
import abc
from datetime import datetime
from codigram import db, login_manager, DATE_FORMAT
from flask_login import UserMixin, current_user
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
    picture = db.Column(db.Text, nullable=False, default="/static/images/profiles/default.png")

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
            "sandbox_uuid": str(self.uuid),
            "author": self.author.get_display_name(),
            "date_created": self.created.strftime(DATE_FORMAT),
            "title": self.title,
            "blocks": self.content if self.content else []
        }

    def get_all_blocks(self):
        if not self.content:
            return []
        return self.content


def extract_and_validate_sandbox(sandbox_data):
    if not isinstance(sandbox_data, dict):
        return None, None, None
    if not keys_exist({"sandbox_uuid": str, "title": str, "blocks": list}, sandbox_data):
        return None, None, None
    if not sandbox_data["sandbox_uuid"] or not sandbox_data["title"]:
        return None, None, None
    sandbox = Sandbox.query.get(sandbox_data["sandbox_uuid"])
    if not sandbox or sandbox.author_uuid != current_user.uuid:
        return None, None, None

    if not validate_blocks(sandbox_data["blocks"]):
        return None, None, None
    return sandbox, sandbox_data["title"], sandbox_data["blocks"]


def validate_blocks(blocks):
    block_names = []
    for block in blocks:
        if not isinstance(block, dict):
            return False
        if not keys_exist({"name": str, "type": str}, block, nullable=False):
            return False
        if block["name"] in block_names:
            return False
        block_names.append(block["name"])
        block_type = block["type"]

        if block_type == "TextBlock":
            return validate_text_block(block)
        elif block_type == "ChoiceBlock":
            return validate_choice_block(block)
        elif block_type == "CodeBlock":
            return validate_code_block(block)

        return False


def validate_text_block(block):
    if "text" not in block:
        block["text"] = ""
        return True
    if isinstance(block["text"], str):
        return True
    return False


def validate_choice_block(block):
    if "text" not in block:
        block["text"] = ""
    elif not isinstance(block["text"], str):
        return False

    if "choices" not in block or not block["choices"]:
        block["choices"] = [""]
        return True
    if not isinstance(block["choices"], list):
        return False
    for choice in block["choices"]:
        if not isinstance(choice, str):
            return False
    return True


def validate_code_block(block):
    if "code" not in block:
        block["code"] = ""
        return True
    if isinstance(block["code"], str):
        return True
    return False


def keys_exist(keys, data, nullable=True):
    for key, key_type in keys.items():
        if key not in data:
            return False
        if not nullable and not data[key]:
            return False
        if not isinstance(data[key], key_type):
            return False
    return True


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
