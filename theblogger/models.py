from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

from theblogger import db, login_manager


@login_manager.user_loader  # checking if the user is authenicated
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):  # Setting up the class responsible for creating users instances
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    # each user will have a default profile image
    profile_image = db.Column(
        db.String(64), nullable=False, default="default_profile.png")
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # setting up the relationship between users and blogpost models
    posts = db.relationship("BlogPost", backref="author", lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f"Username is {self.username}"

    # checking the password when the user logs in
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class BlogPost(db.Model):  # this class is used to create post instances linked to the user

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    # linking the blogpost with user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(150), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} -- {self.title}"
