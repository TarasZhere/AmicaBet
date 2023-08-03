import os
from flask import Flask, render_template


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'amica.sqlite'),
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

    from . import db
    db.init_app(app)

    @app.route('/')
    def landing():
        return render_template('landing/landing.html')

    @app.route('/offers')
    def offers():
        return render_template('landing/offers.html')

    @app.route('/developer')
    def developer():
        return render_template('landing/developer.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    from . import auth, user, bet, friend, vote, notification
    app.register_blueprint(auth.bp)

    app.register_blueprint(user.bp)

    app.register_blueprint(bet.bp)

    app.register_blueprint(friend.bp)

    app.register_blueprint(vote.bp)

    app.register_blueprint(notification.bp)

    return app
