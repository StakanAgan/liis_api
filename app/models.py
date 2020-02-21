from app import db

ROLE_USER = 0
ROLE_ADMIN = 1


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)

    __table_args__ = (db.UniqueConstraint(user_id, question_id, answer_id),)
    user = db.relationship('User', back_populates='result')
    question = db.relationship('Question', back_populates='result')
    answer = db.relationship('Answer', back_populates='result')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    result = db.relationship('Result', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}> '


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    describe = db.Column(db.String(256))
    result = db.relationship('Result', back_populates='question')

    def __repr__(self):
        return f'<{self.describe}>'


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.String(128))
    result = db.relationship('Result', back_populates='answer')

    def __repr__(self):
        return f'<{self.response}>'
