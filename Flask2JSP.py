from flask import Flask, render_template, session, redirect, url_for, make_response, request
from flask.ext.wtf import Form
from flask.ext.login import LoginManager
from wtforms import StringField, PasswordField, SubmitField, RadioField

app = Flask(__name__)
login_manager = LoginManager()
login_manager.session_protection = 'basic'
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


if __name__ == '__main__':
    app.run(debug=True)

