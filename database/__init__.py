from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database():
    from database.models import Humidity, Pressure, Temperature, User
    db.drop_all()
    db.create_all()
