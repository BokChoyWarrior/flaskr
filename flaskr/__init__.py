import os

from flask import Flask, redirect, url_for


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialise modules inside app
    from . import db
    db.init_app(app)
    
    # register blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return redirect(url_for("index"))

    @app.route('/test')
    def test():
        return "Hello, World!"

    @app.route('/cats')
    def cats():
        return 'Insert cat pictures here!'

    @app.route('/api')
    def api():
        return {
            "name": "cat",
            "id": 591212,
            "message": "Thanks for using cat API!",
        }

    return app
