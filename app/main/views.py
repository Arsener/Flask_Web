from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, current_app
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
    # page = request.args.get('page', 1, type=int)
    # pagination = Post.query.order_by(Post.id.desc()).paginate(
    #     page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    # posts = pagination.items
    posts, pagination = get_posts_in_one_page(Post.query)
    return render_template('index.html', form=form, posts=posts, pagination=pagination)

@main.route('/user/<name>')
def user(name):
    user = User.query.filter_by(name=name).first_or_404()
    # page = request.args.get('page', 1, type=int)
    # pagination = Post.query.order_by(Post.id.desc()).paginate(
    #     page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    # posts = pagination.items
    posts, pagination = get_posts_in_one_page(user.posts)
    return render_template('user.html', user=user, posts = posts, pagination=pagination)


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

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])

def get_posts_in_one_page(source):
    page = request.args.get('page', 1, type=int)
    pagination = source.order_by(Post.id.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return posts, pagination
