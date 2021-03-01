from solstice import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(25), unique=False, nullable=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    pfp = db.Column(db.String(32), nullable=False, default="default.jpg")
    verified = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(60), nullable=False)
    projects = db.relationship("Project", backref="project_uploader", lazy=True)
    forums = db.relationship("Forum", backref="forum_uploader", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.name}', '{self.email}', '{self.pfp}')"

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    score = db.Column(db.Integer, nullable=False, default=0)
    total_comments = db.Column(db.Integer, nullable=False, default=0)
    survey = db.Column(db.String(128), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"User('{self.content}', '{self.date_posted}', '{self.score}', '{self.total_comments}', '{self.survey}')"

class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(600), nullable=False)
    category = db.Column(db.String(32), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    score = db.Column(db.Integer, nullable=False, default=0)
    total_comments = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"User('{self.content}', '{self.date_posted}', '{self.score}', '{self.total_comments}')"
