from flask import Flask, render_template, session, redirect, url_for
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, RadioField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Flask2JSP'

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


if __name__ == '__main__':
    app.run(debug=True)

