from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import base64
from datetime import datetime, timedelta
import os

ROLE_USER = 0
ROLE_ADMIN = 1


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False, index=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)

    __table_args__ = (db.UniqueConstraint(user_id, question_id, answer_id),)
    user = db.relationship('User', back_populates='result')
    question = db.relationship('Question', back_populates='result')
    answer = db.relationship('Answer', back_populates='result')

    def from_dict(self, data):
        for field in ['user_id', 'question_id', 'answer_id']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.user.username,
            'question': self.question.describe,
            'answer': self.answer.response,
        }
        return data

    def __repr__(self):
        return f'<User {self.user.username} answer {self.answer.response} to {self.question.describe}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    result = db.relationship('Result', back_populates='user')
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return User

    def __repr__(self):
        return f'<User {self.username}> '

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
        }
        if include_email:
            data['email'] = self.email
        return data

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    describe = db.Column(db.String(256))
    answers = db.relationship('Answer', backref='question', lazy=True,
                              cascade='all, save-update, merge, delete')
    result = db.relationship('Result', back_populates='question')

    def __repr__(self):
        return f'<{self.describe}>'

    def from_dict(self, data):
        for field in ['name', 'describe']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'describe': self.describe
        }
        return data


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.String(128))
    result = db.relationship('Result', back_populates='answer')
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'),
                            nullable=False)

    def __repr__(self):
        return f'<{self.response}>'
