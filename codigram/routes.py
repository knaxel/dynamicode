import flask
from flask import request
from flask_login import login_user,logout_user, login_required, current_user
from codigram import app,db
from codigram.models import User

#########################################
# PAGES                                 #
#########################################

@app.route("/")
def landing_page():
    return flask.render_template("index.html")

@app.route("/home")
@login_required
def home():
    return flask.render_template("/home/index.html", user=current_user)

@app.route("/modules")
@login_required
def modules():
    return flask.render_template("/modules/index.html", user=current_user)

@app.route("/settings")
@login_required
def settings():
    return flask.render_template("/settings/index.html", user=current_user)

@app.route("/profile")
@login_required
def profile():
    return flask.render_template("/profile/index.html", user=current_user)

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
				return flask.render_template('/login/index.html', info=info)

			user = User.query.filter_by(email=email).first()
			if user:
				info.append("The email address is already in use")
				return flask.render_template('/login/index.html', info=info)

			user = User.query.filter_by(user_name=user_name).first()
			if user:
				info.append("This username is already taken")
				return flask.render_template('/login/index.html', info=info)

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
				return flask.render_template('/login/index.html', info=info)
			
			user = User.query.filter_by(email=email).first()
			if not user or user.password != password:
				info.append("your login information is incorrect...")
				return flask.render_template('/login/index.html', info=info)
				
			login_user(user, remember=True)

			return flask.redirect(flask.url_for('profile'))
	return flask.render_template('/login/index.html', info=info)


