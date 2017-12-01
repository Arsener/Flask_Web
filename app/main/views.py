from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from . import main
from .forms import PostForm, EditProfileForm
from .. import db
from ..models import Post, User


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('index.html', form=form, posts=posts)

@main.route('/user/<name>')
def user(name):
    user = User.query.filter_by(name=name).first_or_404()
    posts = user.posts.order_by(Post.id.desc()).all()
    return render_template('user.html', user=user, posts = posts)


@main.route('/welcome/<name>')
def welcome(name):
    return render_template('welcome.html', name=name)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.real_name = form.real_name.data
        current_user.location = form.location.data
        current_user.school = form.school.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been undated.')
        return redirect(url_for('.user', name = current_user.name))

    form.real_name.data = current_user.real_name
    form.location.data = current_user.location
    form.school.data = current_user.school
    form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', form=form)




# from flask import render_template, redirect, url_for, flash
#
# from app.auth.forms import NameForm
# from . import main
# from .. import db
# from ..email import send_email
# from ..models import User
#
#
# @main.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         user_finded_by_name = User.query.filter_by(name=form.name.data).first()
#         user_finded_by_email = User.query.filter_by(email=form.email.data).first()
#         if user_finded_by_name is None and user_finded_by_email is None:
#             name = form.name.data
#             # password = form.name.data
#             email = form.email.data
#             user = User(name = name, email = email)
#             db.session.add(user)
#             send_email(email, name)
#             return redirect(url_for('.welcome', name = name))
#         elif user_finded_by_name is not None:
#             flash('This name has already been used.')
#         elif user_finded_by_email is not None:
#             flash('This email has already been registed.')
#         return redirect(url_for('.index'))
#     return render_template('index.html', form = form)