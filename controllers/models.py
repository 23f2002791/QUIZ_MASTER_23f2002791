from controllers.database import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(50), unique=True, nullable=False)
    user_password = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    qualification = db.Column(db.String(50))
    dob = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, default=False)

class Subject(db.Model):
    sub_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sub_name = db.Column(db.String(50), unique=True, nullable=False)
    sub_desc = db.Column(db.String(100), nullable=False)

class Chapter(db.Model):
    chap_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chap_name = db.Column(db.String(50), nullable=False)
    chap_desc = db.Column(db.String(100), nullable=False)
    sub_id = db.Column(db.Integer, db.ForeignKey('subject.sub_id'), nullable=False)

class Quiz(db.Model):
    quiz_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_name = db.Column(db.String(50), nullable=False)
    quiz_desc = db.Column(db.String(100), nullable=False)
    chap_id = db.Column(db.Integer, db.ForeignKey('chapter.chap_id'), nullable=False)

class Question(db.Model):
    ques_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    ques = db.Column(db.String(100), nullable=False)
    option1 = db.Column(db.String(50), nullable=False)
    option2 = db.Column(db.String(50), nullable=False)
    option3 = db.Column(db.String(50), nullable=False)
    option4 = db.Column(db.String(50), nullable=False)
    ans = db.Column(db.String(50), nullable=False)

class Scores(db.Model):
    score_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    score_total = db.Column(db.Integer, nullable=False)
    date_attempted = db.Column(db.Date, nullable=False)
    