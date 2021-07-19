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
        return self.uuid

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


def get_sample_post():
    # post = Post("Paolo", "Thursday", "Example Post")
    # post.add_block(TextBlock("A", text="This is an example text block with some sample text."))
    # post.add_block(TextBlock("E", text="Yet another example of a text block."))
    # post.add_block(CodeBlock("B", code="for i in range(10):\n  print(i)"))
    # post.add_block(ChoiceBlock("C", ["Choice A", "Choice B", "Choice C"],
    #                            text="This is an example text block with some sample text."))
    # post.add_block(CodeBlock("D", code="import post"))
    return {}
