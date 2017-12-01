#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


# @manager.command
# def test():
#     """Run the unit tests."""
#     import unittest
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()


#
# import os
# from flask import Flask, render_template, session, redirect, url_for, flash
# from flask_script import Manager, Shell
# from flask_bootstrap import Bootstrap
# from flask_moment import Moment
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import Required
# from flask_mail import Mail, Message
# from flask_sqlalchemy import SQLAlchemy
# from threading import Thread
#
# basedir = os.path.abspath(os.path.dirname(__file__))
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'hard to guess string'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# app.config['MAIL_SERVER'] = 'smtp.qq.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'minghui_gong@qq.com'
# app.config['MAIL_PASSWORD'] = 'vhvynhabpnioeigf'
# app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
# app.config['FLASKY_MAIL_SENDER'] = 'minghui_gong@qq.com'
#
# manager = Manager(app)
# bootstrap = Bootstrap(app)
# moment = Moment(app)
# mail = Mail(app)
# db = SQLAlchemy(app)
#
#
# class User(db.Model):
#     __tablename__ = 'users'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True, index=True)
#     password_hash = db.Column(db.String(128))
#     email = db.Column(db.String(64), unique=True, index=True)
#
#     def __repr__(self):
#         return '<User %r>' % self.name
#
#
# class NameForm(FlaskForm):
#     name = StringField('User name:', validators=[Required()])
#     password = StringField('User name:', validators=[Required()])
#     email = StringField('Email:', validators=[Required()])
#     submit = SubmitField('Register')
#
#
# user_list = []
# email_list = []
#
# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)
#
# def send_email(email, name):
#     msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' Welcome to Flask Web!',
#                   sender=app.config['FLASKY_MAIL_SENDER'], recipients=[email])
#     # msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template('new_user.html', name = name)
#     thr = Thread(target=send_async_email, args=[app, msg])
#     thr.start()
#     return thr
#
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     # name = None
#     # email = None
#     if form.validate_on_submit():
#         # name = form.name.data
#         # email = form.email.data
#         user_finded_by_name = User.query.filter_by(name=form.name.data).first()
#         user_finded_by_email = User.query.filter_by(email=form.email.data).first()
#         if user_finded_by_name is None and user_finded_by_email is None:
#             # user_list.append(name)
#             # email_list.append(email)s
#             # app.config['FLASKY_ADMIN'] = email
#             name = form.name.data
#             email = form.email.data
#             user = User(name = name, email = email)
#             db.session.add(user)
#             # session['known'] = False
#             send_email(email, name)
#             return redirect(url_for('welcome', name = name))
#         elif user_finded_by_name is not None:
#             flash('This name has already been used.')
#         elif user_finded_by_email is not None:
#             flash('This email has already been registed.')
#         return redirect(url_for('index'))
#     return render_template('index.html', form = form)
#
#
# @app.route('/welcome/<name>')
# def welcome(name):
#     return render_template('welcome.html', name = name)
#
#
# # @app.route('/manager')
# # def manager():
# #     return render_template('manager.html')
#
#
# if __name__ == '__main__':
#     app.run()
