from flask import jsonify

from flaskr.api import bp
from flaskr.api.errors import error_response
from flaskr.db import get_db

@bp.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    db = get_db()
    post = db.execute(
        "SELECT created, title, body, likes, deleted, users.username"
        " FROM posts"
        " JOIN users ON users.id = posts.author_id"
        " WHERE posts.id = ? AND posts.deleted = 0",
        (id,)
    ).fetchone()

    if not post or post['deleted'] == 1:
        return error_response(404, "Post does not exist or was deleted")

    post_dict = dict(post)
    post_dict.pop('deleted')

    return jsonify(post_dict)

@bp.route('/posts', methods=['GET'])
def get_posts():
    pass

@bp.route('/posts', methods=['POST'])
def create_post():
    pass

@bp.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    pass