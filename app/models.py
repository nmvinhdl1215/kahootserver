from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # avatar_url = db.Column(db.String(256), nullable=True)
    # bio = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        # self.password_hash = generate_password_hash(password)
        self.password_hash = password

    def check_password(self, password):
        # return check_password_hash(self.password_hash, password)
        return self.password_hash == password
    
    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash
        }
        return data
    
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])
    
# class Quiz(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     title = db.Column(db.String(128), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
#     category = db.relationship('Category', back_populates='quizzes')
#     questions = db.relationship('Question', back_populates='quiz', cascade='all, delete-orphan')

# class Question(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
#     text = db.Column(db.Text, nullable=False)
#     type = db.Column(db.String(32), nullable=False, default='multiple_choice')
#     quiz = db.relationship('Quiz', back_populates='questions')
#     options = db.relationship('Option', back_populates='question', cascade='all, delete-orphan')

# class Option(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
#     text = db.Column(db.Text, nullable=False)
#     is_correct = db.Column(db.Boolean, default=False, nullable=False)
#     question = db.relationship('Question', back_populates='options')

# class Session(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
#     host_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     end_time = db.Column(db.DateTime)
#     quiz = db.relationship('Quiz')
#     host = db.relationship('User')
#     participants = db.relationship('Participant', back_populates='session', cascade='all, delete-orphan')

# class Participant(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     join_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     session = db.relationship('Session', back_populates='participants')
#     user = db.relationship('User')

# class Score(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
#     participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
#     score = db.Column(db.Integer, nullable=False)
#     session = db.relationship('Session')
#     participant = db.relationship('Participant')

# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True, nullable=False)
#     quizzes = db.relationship('Quiz', back_populates='category')

# class Leaderboard(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
#     total_score = db.Column(db.Integer, nullable=False, default=0)
#     user = db.relationship('User')
#     quiz = db.relationship('Quiz')

# class Response(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
#     participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
#     question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
#     option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=True)
#     response_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     session = db.relationship('Session')
#     participant = db.relationship('Participant')
#     question = db.relationship('Question')
#     option = db.relationship('Option')

# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))