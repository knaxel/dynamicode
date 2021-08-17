from datetime import datetime

import flask
import base64
from codigram import bcrypt
from flask import request
from sqlalchemy import desc
from flask_login import login_user, logout_user, login_required, current_user
from codigram import app, db
from codigram.models import User, Sandbox, Post, PostLike, Comment, CommentLike, \
    get_sample_post, extract_and_validate_codepage
from codigram.modules.modules import get_module, get_all_modules


#########################################
# PAGES                                 #
#########################################


@app.route("/")
def landing_page():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("home"))
    return flask.render_template("landing_page.html", no_header=True)


@app.route("/home")
@login_required
def home():
    return flask.render_template("home.html", title=f"DynamiCode - {current_user.get_display_name()}")


@app.route("/python_runner")
@login_required
def python_runner():
    return flask.render_template("python_runner.html", post=get_sample_post(), title="DynamiCode - Prototype Post")


@app.errorhandler(404)
def page_not_found(_):
    return flask.render_template('errors/404.html', no_header=True), 404


@app.route("/user_profile/<user_uuid>", methods=['POST', 'GET'])
@login_required
def user_profile(user_uuid):
    viewed_user = User.query.get(user_uuid)
    if not viewed_user:
        return flask.render_template("errors/user_profile_does_not_exist.html", no_header=True)
    return flask.render_template("user_profile.html", title=f"Profile - {viewed_user.get_display_name()}",
                                 viewed_user=viewed_user)


def render_picture(data):
    return base64.b64encode(data).decode('ascii')


@app.route("/edit_profile", methods=['POST', 'GET'])
@login_required
def edit_profile():
    if request.method == 'POST' and "update_profile" in request.form:
        email = request.form.get('email')
        user_name = request.form.get('user_name')
        display_name = request.form.get('display_name')
        bio = request.form.get('biography')

        if current_user.email != email:
            user = User.query.filter_by(email=email).first()
            if user:
                return flask.render_template('edit_profile.html', info=f"{email} is already in use",
                                             title=f"Edit Profile - {current_user.get_display_name()}")
            current_user.email = email
            db.session.commit()
        if current_user.user_name != user_name:
            user = User.query.filter_by(user_name=user_name).first()
            if user:
                return flask.render_template('edit_profile.html', info=f"{user_name} is already taken",
                                             title=f"Edit Profile - {current_user.get_display_name()}")
            current_user.user_name = user_name
            db.session.commit()
        if current_user.display_name != display_name:
            current_user.display_name = display_name
            db.session.commit()
        if current_user.bio != bio:
            current_user.bio = bio
            db.session.commit()
        return flask.render_template("edit_profile.html", info='',
                                     title=f"Edit Profile - {current_user.get_display_name()}")

    if request.method == 'POST' and "update_picture" in request.form:
        picture = request.files['pic']

        if not picture:
            return flask.render_template("edit_profile.html", info='No picture was chosen',
                                         title=f"Edit Profile - {current_user.get_display_name()}")
        data = picture.read()
        rendered_pic = render_picture(data)
        if current_user.picture != rendered_pic:
            current_user.picture = rendered_pic
            db.session.commit()
        return flask.render_template("edit_profile.html", info='',
                                     title=f"Edit Profile - {current_user.get_display_name()}")

    return flask.render_template("edit_profile.html", info='',
                                 title=f"Edit Profile - {current_user.get_display_name()}")


@app.route("/settings/delete", methods=['POST'])
@login_required
def delete_account():
    if "delete_account" in request.form:
        db.session.delete(current_user)
        db.session.commit()
        for sandbox in Sandbox.query.filter_by(author_uuid=current_user.uuid).all():
            db.session.delete(sandbox)
            db.session.commit()
        for post in Post.query.filter_by(author_uuid=current_user.uuid).all():
            db.session.delete(post)
            db.session.commit()
        # TODO: delete module progress, delete content of comments the user made, change username in comment to "deleted"
        return flask.redirect(flask.url_for("login"))
    return flask.render_template("settings.html", title=f"Settings - {current_user.get_display_name()}")


@app.route("/settings")
@login_required
def settings():
    return flask.render_template("settings.html", title=f"Settings - {current_user.get_display_name()}")


@app.route("/change_password", methods=['POST', 'GET'])
@login_required
def change_password():
    if request.method == "POST" and "update_password" in request.form:
        new_password = request.form.get('new_password')
        new_password_copy = request.form.get('new_password_copy')
        if new_password == "":
            return flask.render_template("change_password.html", info='',
                                         title=f"Change Password - {current_user.get_display_name()}")
        if new_password != "" and new_password_copy == "":
            return flask.render_template("change_password.html",
                                         info='Please type your new password again next to *New Password',
                                         title=f"Change Password - {current_user.get_display_name()}")
        if new_password != new_password_copy:
            return flask.render_template("change_password.html",
                                         info='Your new password did not match the second copy',
                                         title=f"Change Password - {current_user.get_display_name()}")
        if new_password == current_user.password:
            return flask.render_template("change_password.html",
                                         info='Your new password is the same as your old password. '
                                              'Please choose something else.',
                                         title=f"Change Password - {current_user.get_display_name()}")
        current_user.password = new_password
        db.session.commit()
        return flask.render_template("change_password.html", info='Your password has been changed',
                                     title=f"Change Password - {current_user.get_display_name()}")

    return flask.render_template("change_password.html", info='',
                                 title=f"Change Password - {current_user.get_display_name()}")


@app.route("/profile")
@login_required
def profile():
    return flask.render_template("profile.html", title=f"Profile - {current_user.get_display_name()}")


@app.route("/modules")
@login_required
def modules():
    return flask.render_template("modules/modules.html", title="Modules", modules=get_all_modules())


@app.route("/modules/<module_id>")
@login_required
def view_module(module_id):
    module = get_module(module_id)
    if not module:
        return flask.redirect(flask.url_for("modules"))
    return flask.render_template("modules/view_module.html", title=module.title, module=module,
                                 progress=module.get_progress())


@app.route("/modules/<module_id>/check-answer", methods=["POST"])
@login_required
def check_module_answer(module_id):
    module = get_module(module_id)
    if not request.content_type.startswith("application/json") or not module:
        return flask.jsonify({"success": False, "message": "", "module_completed": False})

    request_json = request.get_json()
    if request_json.get("name"):
        success, message = module.check_answer(request_json["name"], request_json)
        module_completed = module.get_progress() == 100
        return flask.jsonify({"success": success, "message": message, "module_completed": module_completed})

    return flask.jsonify({"success": False, "message": "", "module_completed": False})


@app.route("/sandbox")
@login_required
def sandboxes():
    return flask.render_template("sandbox/sandbox_menu.html", sandboxes=current_user.sandboxes,
                                 title="DynamiCode Sandbox")


@app.route("/sandbox/new", methods=["POST"])
@login_required
def new_sandbox():
    title = request.form.get("sandbox_name") if request.form.get("sandbox_name") else "Sandbox"
    sandbox = Sandbox(title=title)
    current_user.sandboxes.append(sandbox)
    db.session.commit()
    return flask.redirect(flask.url_for("edit_sandbox", sandbox_uuid=sandbox.uuid))


@app.route("/sandbox/delete", methods=["POST"])
@login_required
def delete_sandbox():
    if not request.form.get("sandbox_uuid"):
        return flask.redirect(flask.url_for("sandboxes"))
    sandbox = Sandbox.query.get(request.form.get("sandbox_uuid"))
    if sandbox and sandbox.author_uuid == current_user.uuid:
        db.session.delete(sandbox)
        db.session.commit()
    return flask.redirect(flask.url_for("sandboxes"))


@app.route("/sandbox/<sandbox_uuid>")
@login_required
def edit_sandbox(sandbox_uuid):
    sandbox = Sandbox.query.get(sandbox_uuid)
    if not sandbox or sandbox.author_uuid != current_user.uuid:
        return flask.redirect(flask.url_for("sandboxes"))
    return flask.render_template("sandbox/edit_sandbox.html", sandbox=sandbox, title="DynamiCode Sandbox")


@app.route("/sandbox/save", methods=["POST"])
@login_required
def save_sandbox():
    sandbox, new_title, new_content = extract_and_validate_codepage(request.get_json(), "sandbox")
    if sandbox and sandbox.author_uuid == current_user.uuid:
        sandbox.title = new_title
        sandbox.content = new_content
        db.session.commit()
        return flask.jsonify({"success": True})
    return flask.jsonify({"success": False, "message": "Sandbox data malformed."})


@app.route("/sandbox/to-post", methods=["POST"])
@login_required
def sandbox_to_post():
    sandbox, new_title, new_content = extract_and_validate_codepage(request.get_json(), "sandbox")
    if sandbox and sandbox.author_uuid == current_user.uuid:
        sandbox.title = new_title
        sandbox.content = new_content
        post = Post(title=sandbox.title, content=sandbox.content)
        current_user.posts.append(post)
        db.session.commit()
        return flask.jsonify({"success": True, "codepage_uuid": str(post.uuid)})
    return flask.jsonify({"success": False, "message": "Sandbox data malformed."})


@app.route("/community")
@login_required
def community():
    return flask.redirect(flask.url_for("view_posts"))


@app.route("/post")
@login_required
def view_posts():
    drafts = Post.query.filter(Post.author_uuid == current_user.uuid,
                               Post.posted == None).all()
    posted = Post.query.filter(Post.author_uuid == current_user.uuid,
                               Post.posted != None).all()
    return flask.render_template("posts/posts_menu.html", drafts=drafts, posted=posted,
                                 title="My Posts")


@app.route("/post/new", methods=["POST"])
@login_required
def new_post():
    title = request.form.get("post_title") if request.form.get("post_title") else "Post"
    post = Post(title=title)
    current_user.posts.append(post)
    db.session.commit()
    return flask.redirect(flask.url_for("edit_post", post_uuid=post.uuid))


@app.route("/post/delete", methods=["POST"])
@login_required
def delete_post():
    if not request.form.get("post_uuid"):
        return flask.redirect(flask.url_for("view_posts"))
    post = Post.query.get(request.form.get("post_uuid"))
    if post and post.author_uuid == current_user.uuid:
        db.session.delete(post)
        # TODO: Delete related tables
        db.session.commit()
    return flask.redirect(flask.url_for("view_posts"))


@app.route("/post/edit/<post_uuid>")
@login_required
def edit_post(post_uuid):
    post = Post.query.get(post_uuid)
    if not post or post.author_uuid != current_user.uuid:
        return flask.redirect(flask.url_for("view_posts"))
    return flask.render_template("posts/edit_post.html", post=post, title="My Posts")


@app.route("/post/<post_uuid>")
@login_required
def view_post(post_uuid):
    post = Post.query.get(post_uuid)
    if not post or not post.is_public:
        return flask.redirect(flask.url_for("view_posts"))
    liked = bool(PostLike.query.filter_by(user_uuid=current_user.uuid, post_uuid=post.uuid).first())
    comments = Comment.query.filter_by(post_uuid=post.uuid).order_by(desc(Comment.created)).limit(20).all()
    return flask.render_template("posts/view_post.html", title=post.title, post=post, liked=liked, comments=comments)


@app.route("/post/save", methods=["POST"])
@login_required
def save_post():
    post, new_title, new_content = extract_and_validate_codepage(request.get_json(), "post")
    if post and post.author_uuid == current_user.uuid:
        post.title = new_title
        post.content = new_content
        if post.posted:
            post.last_edit = datetime.now()
        db.session.commit()
        return flask.jsonify({"success": True})
    return flask.jsonify({"success": False, "message": "Post data malformed."})


@app.route("/post/publish", methods=["POST"])
@login_required
def publish_post():
    post, new_title, new_content = extract_and_validate_codepage(request.get_json(), "post")
    if post and post.author_uuid == current_user.uuid:
        post.title = new_title
        post.content = new_content
        if post.posted:
            post.last_edit = datetime.now()
        else:
            post.posted = datetime.now()
        db.session.commit()
        return flask.jsonify({"success": True})
    return flask.jsonify({"success": False, "message": "Post data malformed."})


@app.route("/post/like", methods=["POST"])
@login_required
def like_post():
    if not request.content_type.startswith("application/json"):
        return flask.jsonify({"success": False, "message": "You must use ContentType='application/json'."})
    request_json = request.get_json()
    post = Post.query.get(str(request_json.get("post_uuid")))
    if not post or not post.posted or (not post.is_public and not post.author_uuid == current_user.uuid):
        return flask.jsonify({"success": False, "message": "Post does not exist."})
    previous_like = PostLike.query.filter_by(user_uuid=current_user.uuid, post_uuid=post.uuid).first()
    if bool(request_json.get("like")) == bool(previous_like):
        return flask.jsonify({"success": False, "message": "No action needed."})

    if previous_like:
        db.session.delete(previous_like)
    else:
        current_user.liked_posts.append(post)
    db.session.commit()
    return flask.jsonify({"success": True})


@app.route("/post/comment/new", methods=["POST"])
@login_required
def comment_on_post():
    post = Post.query.get(str(request.form.get("post_uuid")))
    if post and post.is_public and post.posted and request.form.get("text"):
        new_comment = Comment(post_uuid=post.uuid, author_uuid=current_user.uuid, text=str(request.form["text"]))
        db.session.add(new_comment)
        db.session.commit()
        return flask.redirect(flask.url_for("view_post", post_uuid=post.uuid) + "#comments")
    return flask.redirect(flask.url_for("community"))


@app.route("/post/comment/like", methods=["POST"])
@login_required
def like_comment():
    if not request.content_type.startswith("application/json"):
        return flask.jsonify({"success": False, "message": "You must use ContentType='application/json'."})
    request_json = request.get_json()
    comment = Comment.query.get(str(request_json.get("comment_uuid")))
    if not comment:
        return flask.jsonify({"success": False, "message": "Comment does not exist."})
    previous_like = CommentLike.query.filter_by(user_uuid=current_user.uuid, comment_uuid=comment.uuid).first()
    if bool(request_json.get("like")) == bool(previous_like):
        return flask.jsonify({"success": False, "message": "No action needed."})

    if previous_like:
        db.session.delete(previous_like)
    else:
        current_user.liked_comments.append(comment)
    db.session.commit()
    return flask.jsonify({"success": True})


@app.route("/friends", methods=['GET'])
@login_required
def friends():
    search_results = None

    if request.method and request.method == 'GET':
        search = request.args.get("search")

        if search is None or search == "":
            search_results = User.query.limit(30).all()
        else:
            search_results = User.query.filter(User.user_name.contains(search)).limit(30).all()
    return flask.render_template("friends.html", user=current_user, search_results=search_results, title="Friends")


#########################################
# AUTHENTICATION                        #
#########################################


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for('landing_page'))


@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('home'))

    info = []
    if request.method == 'POST':
        if "button_register" in request.form:
            info.append("register")

            email = request.form.get('email')
            user_name = request.form.get('user_name')
            password = request.form.get('password')
            password_repeat = request.form.get('passwordRepeat')

            if user_name == "":
                info.append("You need to enter a username")
            if email == "":
                info.append("You need to enter an email")
            if password == "":
                info.append("You need to enter a password")
            if password_repeat == "":
                info.append("You need to enter your password again")
            if password_repeat != password:
                info.append("The passwords entered do not match")

            if len(info) != 1:
                return flask.render_template('login.html', info=info, title="Login / Register", no_header=True)

            user = User.query.filter_by(email=email).first()
            if user:
                info.append("The email address is already in use")
                return flask.render_template('login.html', info=info, title="Login / Register", no_header=True)

            user = User.query.filter_by(user_name=user_name).first()
            if user:
                info.append("This username is already taken")
                return flask.render_template('login.html', info=info, title="Login / Register", no_header=True)

            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            new_user = User(email=email, user_name=user_name, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()

            info.append('registration submitted, try logging in!')

        if "button_login" in request.form:
            info.append("login")
            email = request.form.get('email')
            password = request.form.get('password')

            if email == "":
                info.append("You need to enter an email")
            if password == "":
                info.append("You need to enter a password")

            if len(info) != 1:
                return flask.render_template('login.html', info=info, title="Login / Register", no_header=True)

            user = User.query.filter_by(email=email).first()
            if not user or not bcrypt.check_password_hash(user.password, password):
                info.append("your login information is incorrect...")
                return flask.render_template('login.html', info=info, title="Login / Register", no_header=True)

            login_user(user, remember=True)

            return flask.redirect(flask.url_for('profile'))
    return flask.render_template('login.html', info=info, title="Login / Register", no_header=True)
