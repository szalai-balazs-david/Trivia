from app.main import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    questions = db.relationship('Question', backref='cat', lazy=True)


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False, unique=True)
    answer = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    answer_attempt_count = db.Column(db.Integer, nullable=False)
    answer_success_count = db.Column(db.Integer, nullable=False)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    questions_total = db.Column(db.Integer, nullable=False)
    questions_won = db.Column(db.Integer, nullable=False)
