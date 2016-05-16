from flask import Flask, render_template, session, redirect, url_for, make_response, request
from flask.ext.wtf import Form
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager, login_required, login_user, logout_user, UserMixin
from wtforms import StringField, PasswordField, SubmitField, RadioField

app = Flask(__name__)
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'basic'
bootstrap.init_app(app)
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'Flask2JSP'

class LoginForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

class NameForm(Form):
    name = StringField('Username')
    passwd = PasswordField('Password')
    gender = RadioField('gender', choices=[('M', 'Male'), ('F', 'Female')])
    submit = SubmitField('Submit')

class User(UserMixin):
    def __init__(self, name):
        self.name = name

    def get_id(self):
        return self.name

@login_manager.user_loader
def load_user(name):
    return User(name=name)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['password'] = form.passwd.data
        session['gender'] = form.gender.data
        return redirect(url_for('.info'))
    return render_template('index.html', form=form)

@app.route('/info')
def info():
    return render_template('info.html', name=session.get('name'), passwd=session.get('password'), gender=session.get('gender'))

@app.route('/make_cookie')
def makeCookie():
    response = make_response('<h1>This document carries a cookie</h1>')
    response.set_cookie('cookie', 'tasty')
    if not request.cookies.get('cookie'):
        print request.cookies.get('cookie')
    return response

@app.route('/get_session', methods=['GET', 'POST'])
def getSession():
    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        session['password'] = form.password.data
        return session['username'] + '<br>' + session['password']
    return render_template('session.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = load_user(form.username.data)
        login_user(user)
        return redirect(url_for('main'))
    return render_template('login.html', form=form)

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

