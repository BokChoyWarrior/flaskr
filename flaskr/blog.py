from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

####################
# helper functions #
####################

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, likes, deleted'
        ' FROM posts p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

##########
# routes #
##########

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT posts.id, title, body, created, author_id, username, likes, deleted'
        ' FROM posts'
        ' JOIN user u ON posts.author_id = u.id'
        ' WHERE posts.deleted = 0'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        errors = check_post_validity(title, body)
        if errors:
            for error in errors:
                flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO posts (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', edit_type="create")

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        errors = check_post_validity(title, body)
        if errors:
            for error in errors:
                flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE posts SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post, edit_type="update")

def check_post_validity(title, body):
    errors = []

    if not title:
        errors.append('Title is required.')

    if len(title) > 250:
        errors.append('Title must be 50 chars or less.')
    
    if len(body) > 8192:
        errors.append('Body text must be 4096 characters or less.')
    
    if not body:
        errors.append('Body is required.')

    if len(errors) > 0:
        return errors
    
    return False

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    print(f"Deleting post {id}")
    get_post(id)
    db = get_db()
    db.execute(
        'UPDATE posts'
        ' SET deleted = ?'
        ' WHERE id = ?',
        (1, id,)
    )
    db.commit()
    return redirect(url_for('blog.index'))