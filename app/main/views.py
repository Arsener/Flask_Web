from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required, current_app
from . import main
from .forms import PostForm, EditProfileForm, CommentForm
from .. import db
from ..models import Post, User, Comment


@main.route('/', methods=['GET', 'POST'])
def index():
    posts, pagination = get_posts_in_one_page(Post.query)
    return render_template('index.html', posts=posts, pagination=pagination)

@main.route('/user/<name>')
def user(name):
    user = User.query.filter_by(name=name).first_or_404()
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


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        try:
            current_user._get_current_object()._sa_instance_state
        except:
            flash('You must login first.')
            return redirect(url_for('auth.login'))
        else:
            comment = Comment(body=form.body.data,
                              post=post,
                              author=current_user._get_current_object())
            db.session.add(comment)
            flash('Your comment has been published.')
            return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
               current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', post=post, form=form, post_author=User.query.filter_by(id=post.author_id).first(),
                        comments=comments, pagination=pagination, User=User)


@main.route('/write-post', methods=['GET', 'POST'])
@login_required
def write_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        if len(title) > 48:
            flash('The length of the title must be less than 48 characters')
            return render_template('write_post.html', form=form)
        post = Post(title=title, body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    return render_template('write_post.html', form=form)


@main.route('/delete/<int:id>')
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    flash('Your blog has been deleted.')
    return redirect(url_for('.user', name=current_user.name))


@main.route('/edit-post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if current_user.id != post.author_id:
        abort(403)
    form = PostForm()

    if form.validate_on_submit():
        if len(form.title.data) > 48:
            flash('The length of the title must be less than 48 characters')
            return render_template('edit_post.html', form=form)
        post.title = form.title.data
        post.body = form.body.data
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))

    form.title.data = post.title
    form.body.data = post.body

    return render_template('edit_post.html', form=form)


@main.route('/delete-comment/<int:id>')
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    post = Post.query.filter_by(id=comment.post_id).first()
    db.session.delete(comment)
    flash('The comment has been deleted.')
    return redirect(url_for('.post', id=post.id))


def get_posts_in_one_page(source):
    page = request.args.get('page', 1, type=int)
    pagination = source.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return posts, pagination
