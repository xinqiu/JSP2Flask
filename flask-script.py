from flask import Flask
from flask.ext.script import Command, Manager, Option
from flask.ext.script import Manager


app = Flask(__name__)
manager = Manager(app)

@manager.command
def mysql(password):
    print "password is", password

@manager.option('-n', '--name', dest='name', default='joe')
def hello(name):
    print "hello", name

if __name__ == "__main__":
    manager.run()