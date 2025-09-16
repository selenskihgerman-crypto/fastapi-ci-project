from flask import Flask
from app.models import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Импортируем и инициализируем роуты после создания app
    from app.routes import init_routes
    init_routes(app)

    with app.app_context():
        db.create_all()

    return app