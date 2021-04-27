from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
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
        ' FROM posts p JOIN users u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None or post['deleted'] == 1:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

def get_comment(id, check_author=True):
    comment = get_db().execute(
        'SELECT c.id, content, created, author_id, username, likes, deleted, post_id'
        ' FROM comments c JOIN users u ON c.author_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()

    if comment is None or comment['deleted'] == 1:
        abort(404, f"Comment id {id} doesn't exist.")

    if check_author and comment['author_id'] != g.user['id']:
        abort(403)

    return comment

##########
# routes #
##########

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT posts.id, title, body, created, author_id, username, likes, deleted'
        ' FROM posts'
        ' JOIN users u ON posts.author_id = u.id'
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

@bp.route('/<int:id>/comment', methods=('POST',))
@login_required
def comment(id):
    text = request.form['comment-box']
    errors = check_comment_validity(text)
    if errors:
        for error in errors:
            flash(error)
    else:
        db = get_db()
        db.execute(
            'INSERT INTO comments (author_id, post_id, content)'
            ' VALUES (?, ?, ?)',
            (g.user['id'], id, text)
        )
        db.commit()
        return redirect(url_for('blog.view', id=id))

    return redirect(url_for('blog.view', id=id))

def check_comment_validity(text):
    errors = []
    if not text:
        errors.append('Comment body is required.')

    if len(text) > 2048:
        errors.append('Comment too long!')

    if len(errors) > 0:
        return errors

    return False

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
        ' SET deleted = 1'
        ' WHERE id = ?',
        (id,)
    )
    db.commit()
    flash(message="Post deleted successfully")
    return redirect(url_for('blog.index'))

@bp.route('/<int:id>/delete_comment')
@login_required
def delete_comment(id):
    comment = get_comment(id)
    post_id = comment['post_id']
    print(f"Deleting comment {id}")
    db = get_db()
    db.execute(
        'UPDATE comments'
        ' SET deleted = 1'
        ' WHERE id = ?',
        (id,)
    )
    db.commit()
    flash(message="Comment deleted successfully")
    return redirect(url_for('blog.view', id=post_id))

@bp.route('/<int:id>/view')
def view(id):
    db = get_db()
    post = db.execute(
        "SELECT posts.id, created, author_id, title, body, likes, deleted, users.username"
        " FROM posts"
        " JOIN users ON users.id = posts.author_id"
        " WHERE posts.id = ? AND posts.deleted = 0",
        (id,)
    ).fetchone()

    comments = db.execute(
        "SELECT c.id, author_id, content, likes, created, username, c.post_id"
        " FROM comments c"
        " JOIN users u ON c.author_id = u.id"
        " WHERE c.post_id = ? AND c.deleted = 0"
        " ORDER BY created DESC",
        (id,)
    ).fetchall()
    
    if not post:
        flash(message="That post does not exist!")
        return redirect(url_for('blog.index'))

    return render_template('blog/post.html', post=post, comments=comments)