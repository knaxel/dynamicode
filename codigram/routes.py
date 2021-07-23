import flask
from flask import request
from flask_login import login_user, logout_user, login_required, current_user
from codigram import app, db
from codigram.models import User, get_sample_post, get_sample_sandbox


#########################################
# PAGES                                 #
#########################################


@app.route("/python_runner")
@login_required
def python_runner():
    return flask.render_template("python_runner.html", post=get_sample_post())


@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('errors/404.html'), 404

@app.route("/user_profile", methods=['POST','GET'])
def user_profile():
	user_name = request.args.get('user_name')
	if user_name is None:
		return flask.render_template("/errors/user_profile_does_not_exist.html", user=current_user, user_name= user_name)
	viewed_user = User.query.filter_by(user_name=user_name).first()
	if not viewed_user:
		return flask.render_template("/errors/user_profile_does_not_exist.html", user=current_user, user_name= user_name)
	return flask.render_template("/user_profile.html", user=current_user, viewed_user= viewed_user)

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
                return flask.render_template('/edit_profile.html', user=current_user, info=f"{email} is already in use")
            current_user.email = email
            db.session.commit()
        if current_user.user_name != user_name:
            user = User.query.filter_by(user_name=user_name).first()
            if user:
                return flask.render_template('/edit_profile.html', user=current_user, info=f"{user_name} is already taken")
            current_user.user_name = user_name
            db.session.commit()
        if current_user.display_name != display_name:
            current_user.display_name = display_name
            db.session.commit()
        if current_user.bio != bio:
            current_user.bio = bio
            db.session.commit()
        return flask.render_template("/edit_profile.html", user=current_user, info='')

    return flask.render_template("/edit_profile.html", user=current_user, info='')



@app.route("/")
def landing_page():
    return flask.render_template("/landing_page.html")

@app.route("/home")
@login_required
def home():
    return flask.render_template("/home.html", user=current_user)

@app.route("/settings")
@login_required
def settings():
    return flask.render_template("/settings.html", user=current_user)

@app.route("/profile")
@login_required
def profile():
    return flask.render_template("/profile.html", user=current_user)


@app.route("/sandbox")
@login_required
def sandbox():
    return flask.render_template("/sandbox.html", sandbox=get_sample_sandbox())


@app.route("/modules/")
@login_required
def modules():
    return flask.render_template("/modules.html", user=current_user)

@app.route("/community")
@login_required
def community():
    return flask.redirect(flask.url_for("friends"))

@app.route("/friends", methods=['GET'])
@login_required
def friends():
	search_results =None

	if request.method and request.method == 'GET':
		search = request.args.get("search")

		if search is None or search=="":
			search_results = User.query.limit(30).all()
		else:
			search_results = User.query.filter(User.user_name.contains(search)).limit(30).all()
	return flask.render_template("/friends.html", user=current_user, search_results=search_results)


@app.route("/modules/python/module_<int:module_number>")
def python_module(module_number):
    module_files = [f"modules/python/module_0.html", f"modules/python/module_1.html", f"modules/python/module_2.html"]
    if 0 <= module_number <= 2:
        return flask.render_template(module_files[module_number], user=current_user, title=f"Python Module {module_number}")
    return flask.redirect(flask.url_for("modules"))

#########################################
# AUTHENTICATION                        #
#########################################


@app.route("/logout")
@login_required
def logout():
	logout_user()
	return flask.redirect(flask.url_for('landing_page'))

@app.route("/login", methods=['POST','GET'])
def login():

	if current_user.is_authenticated:
		return flask.redirect(flask.url_for('home'))

	info=[]
	if request.method == 'POST':
		if "button_register" in request.form:
			info.append("register")

			email = request.form.get('email')
			user_name = request.form.get('user_name')
			password = request.form.get('password')
			passwordRepeat = request.form.get('passwordRepeat')

			if user_name == "":
				info.append("You need to enter a username")
			if email == "":
				info.append("You need to enter an email")
			if password == "":
				info.append("You need to enter a password")
			if passwordRepeat == "":
				info.append("You need to enter your password again")
			if passwordRepeat != password:
				info.append("The passwords entered do not match")

			if len(info) != 1:
				return flask.render_template('/login.html', info=info)

			user = User.query.filter_by(email=email).first()
			if user:
				info.append("The email address is already in use")
				return flask.render_template('/login.html', info=info)

			user = User.query.filter_by(user_name=user_name).first()
			if user:
				info.append("This username is already taken")
				return flask.render_template('/login.html', info=info)

			new_user = User(email=email, user_name=user_name, password=password)

			db.session.add(new_user)
			db.session.commit()

			info.append('registeration submited, try loging in!')

		if "button_login" in request.form:
			info.append("login")
			email = request.form.get('email')
			password = request.form.get('password')

			if email == "":
				info.append("You need to enter an email")
			if password == "":
				info.append("You need to enter a password")

			if len(info) != 1:
				return flask.render_template('/login.html', info=info)

			user = User.query.filter_by(email=email).first()
			if not user or user.password != password:
				info.append("your login information is incorrect...")
				return flask.render_template('/login.html', info=info)

			login_user(user, remember=True)

			return flask.redirect(flask.url_for('profile'))
	return flask.render_template('/login.html', info=info)
