from datetime import datetime
from codigram import db, login_manager, DATE_FORMAT
from flask_login import UserMixin, current_user
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid
from flask import Markup


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
    picture = db.Column(db.Text, nullable=False, default="")
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
        if self.picture:
            return f"data:image/jpeg;base64, {self.picture}"
        else:
            return "/static/images/profiles/default.png"


class Post(db.Model):
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    author_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey("user.uuid"), nullable=False)
    is_public = db.Column(db.Boolean, nullable=False, default=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    posted = db.Column(db.DateTime)
    last_edit = db.Column(db.DateTime)
    title = db.Column(db.String(256), nullable=False)
    tags = db.Column(db.ARRAY(UUID(as_uuid=True)))
    likes = db.Column(db.Integer, nullable=False, default=0)
    content = db.Column(JSON)

    def get_json(self):
        return {
            "codepage_uuid": str(self.uuid),
            "author": self.author.get_display_name(),
            "author_uuid": str(self.author_uuid),
            "date_created": (self.posted or self.created).strftime(DATE_FORMAT),
            "date_edited": self.last_edit.strftime(DATE_FORMAT) if self.last_edit else None,
            "title": self.title,
            "blocks": self.content if self.content else [],
            "codepage_type": "sandbox"
        }


class Sandbox(db.Model):
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(), nullable=False)
    author_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey("user.uuid"), nullable=False)
    is_public = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(JSON)

    def get_json(self):
        return {
            "codepage_uuid": str(self.uuid),
            "author": self.author.get_display_name(),
            "author_uuid": str(self.author_uuid),
            "date_created": self.created.strftime(DATE_FORMAT),
            "title": self.title,
            "blocks": self.content if self.content else [],
            "codepage_type": "sandbox"
        }


def extract_and_validate_codepage(codepage_data, codepage_type):
    if not isinstance(codepage_data, dict):
        return None, None, None
    if not keys_exist({"codepage_uuid": str, "title": str, "blocks": list}, codepage_data):
        return None, None, None
    if not codepage_data["codepage_uuid"] or not codepage_data["title"]:
        return None, None, None

    if codepage_type == "sandbox":
        codepage = Sandbox.query.get(codepage_data["codepage_uuid"])
    elif codepage_type == "post":
        codepage = Post.query.get(codepage_data["codepage_uuid"])
    else:
        return None, None, None

    if not codepage or codepage.author_uuid != current_user.uuid:
        return None, None, None

    if not validate_blocks(codepage_data["blocks"], codepage_type):
        return None, None, None
    codepage_data["title"] = html_safe(codepage_data["title"])
    return codepage, codepage_data["title"], codepage_data["blocks"]


def validate_blocks(blocks, codepage_type):
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
            if not validate_text_block(block):
                return False
        elif block_type == "ChoiceBlock":
            if not validate_choice_block(block):
                return False
        elif block_type == "CodeBlock":
            if not validate_code_block(block):
                return False
        elif block_type == "ImageBlock":
            if not validate_image_block(block):
                return False
        elif block_type == "SliderBlock":
            if not validate_slider_block(block):
                return False
        else:
            raise NotImplementedError(f"Validation for {block_type} has not been created yet.")

    return True


def validate_text_block(block):
    if "text" not in block:
        block["text"] = ""
        return True
    if isinstance(block["text"], str):
        return True
    clean_block_data(block, ["name", "type", "text"])
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
    for i, choice in enumerate(block["choices"]):
        if not isinstance(choice, str):
            return False
        block["choices"][i] = html_safe(choice)
    clean_block_data(block, ["name", "type", "text", "choices"])
    return True


def validate_code_block(block):
    if "code" not in block:
        block["code"] = ""
        return True
    if isinstance(block["code"], str):
        return True
    clean_block_data(block, ["name", "type", "code"], no_sanitize=["code"])
    return False


def validate_image_block(block):
    if "text" not in block:
        block["text"] = ""
    elif not isinstance(block["text"], str):
        return False
    if "src" not in block:
        block["src"] = ""
    elif not isinstance(block["text"], str):
        return False
    clean_block_data(block, ["name", "type", "text", "src"])
    return True


def validate_slider_block(block):
    if "text" not in block:
        block["text"] = ""
    elif not isinstance(block["text"], str):
        return False

    try:
        block["lower"] = float(block["lower"])
        block["upper"] = float(block["upper"])
        block["default"] = float(block["default"])
    except (ValueError, TypeError):
        return False

    if block["lower"] >= block["upper"]:
        block["lower"] = block["upper"] - 1
    if block["default"] < block["lower"]:
        block["default"] = block["lower"]
    if block["default"] > block["upper"]:
        block["default"] = block["upper"]
    clean_block_data(block, ["name", "type", "text", "lower", "upper", "default"])
    return True


def clean_block_data(block, fields, no_sanitize=()):
    erase_fields = []
    for key, value in block.items():
        if key in fields:
            if isinstance(value, str) and key not in no_sanitize:
                value = html_safe(value)
            block[key] = value
        else:
            erase_fields.append(key)

    for field in erase_fields:
        del block[field]


def keys_exist(keys, data, nullable=True):
    for key, key_type in keys.items():
        if key not in data:
            return False
        if not nullable and not data[key]:
            return False
        if not isinstance(data[key], key_type):
            return False
    return True


def html_safe(unsafe_string):
    return str(Markup.escape(unsafe_string))


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
