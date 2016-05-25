# coding=utf-8
import os
from flask import Flask, render_template, session, redirect, url_for, \
    make_response, request, flash
from flask.ext.wtf import Form
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager, login_required, login_user, \
    logout_user, UserMixin
from wtforms import StringField, PasswordField, SubmitField, RadioField
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'basic'
bootstrap.init_app(app)
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'Flask2JSP'
#此处密码应该保存在环境变量中,这样更安全
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@115.159.96.43/jsp2flask'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

dic = {'count': 0}

class LoginForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')

class NameForm(Form):
    name = StringField('Username')
    passwd = PasswordField('Password')
    gender = RadioField('gender', choices=[('M', 'Male'), ('F', 'Female')])
    submit = SubmitField('Submit')

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

    def __init__(self, name, password=None):
        self.name = name
        self.password = password

    def get_id(self):
        return self.name

    def __repr__(self):
        return '<User %s>' % self.name

@login_manager.user_loader
def load_user(name):
    return User(name=name)

@app.route('/', methods=['GET', 'POST'])
def index():
    dic['count'] += 1
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['password'] = form.passwd.data
        session['gender'] = form.gender.data
        return redirect(url_for('.info'))
    return render_template('index.html', form=form, dic=dic)

@app.route('/info')
def info():
    return render_template('info.html', name=session.get('name'), passwd=
    session.get('password'), gender=session.get('gender'))

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

    if form.validate_on_submit() and form.password.data != '':
        username = form.username.data
        password = form.password.data
        userInfo = User(name=form.username.data, password=form.password.data)
        user = User.query.filter_by(name=username).first()
        if user.name == username and user.password == password:
            login_user(load_user(form.username.data))
            return redirect(url_for('main'))
        else:
            flash('Wrong password!')
            redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/main')
def main():
    return render_template('main.html')

@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]

@app.route('/lists')
def lists():
    s = range(10)
    return render_template('lists.html', mylist=s)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    manager.run()


