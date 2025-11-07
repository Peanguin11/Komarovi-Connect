
from flask_login import UserMixin, LoginManager
from datetime import datetime
from uuid import uuid4

from werkzeug.security import generate_password_hash

from config import db, app


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, )
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    def __init__(self, username, password, role="guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    registration_link = db.Column(db.String(500))
    location = db.Column(db.String(500))
    image = db.Column(db.String(200))
    event_date = db.Column(db.DateTime)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.id

class AlumniBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    title = db.Column(db.String(200))
    class_year = db.Column(db.String(10))
    position = db.Column(db.String(100))
    photo_path = db.Column(db.String(200))

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    funding_goal = db.Column(db.Integer, nullable=False, default=0)
    current_amount = db.Column(db.Integer, nullable=False, default=0)
    image = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Project %r>' % self.id

# class AdminUser(UserMixin):
#     id = "admin"

def make_unique(string):
    ident = uuid4().__str__()
    return f"{ident}-{string}"

class News(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80), unique= False, nullable= False)
    img = db.Column(db.String(80), unique= False, nullable= False)
    description = db.Column(db.String(80), unique= False, nullable= False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.id}: {self.name}'



if __name__ == '__main__' :

    with app.app_context():
        db.create_all()
        admin = User(username='admin', password='password', role='admin')
        user = User(username='user', password='123')
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()