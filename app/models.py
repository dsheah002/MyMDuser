from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(200))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class EditHistory(db.Model):
    history_id = db.Column(db.Integer, primary_key=True)
    edit_type = db.Column(db.String(100))
    edit_material = db.Column(db.String(100))
    edit_page = db.Column(db.String(100))
    old_content = db.Column(db.String(200))
    new_content = db.Column(db.String(200))
    changed_by = db.Column(db.String(100))
    changed_time = db.Column(db.String(100))


db.create_all()
db.session.commit()
