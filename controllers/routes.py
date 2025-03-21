from main import app
from flask import render_template, request, session, flash, redirect, url_for
from controllers.models import *
from datetime import datetime

@app.route('/')
def home():
    if(session.get('is_admin') == True):
        subjects = Subject.query.all()
        return render_template('admin_dashboard.html', subjects=subjects)
    elif(session.get('user_email')):
        quizzes = Quiz.query.all()
        return render_template('user_dashboard.html', quizzes=quizzes)
    else:
        flash('You are not logged in!',"danger")
        return redirect(url_for('login'))

@app.route('/add_subject', methods=['GET','POST'])
def add_subject():

    if session.get('is_admin') == True:
        if request.method == 'GET':
            return render_template('add_subject.html')
        
        if request.method == 'POST':
            name = request.form.get('name',None)
            description = request.form.get('description',None)
            
            if not name or not description:
                flash('Subject Name and Description are Mandatory!',"danger")
                return redirect(url_for('add_subject'))
            
            sub = Subject.query.filter_by(sub_name=name).first()
            if sub:
                flash('Subject already exists, create a new one!',"danger")
                return redirect(url_for('add_subject'))
            else:
                new_sub = Subject(
                    sub_name = name,
                    sub_desc = description
                )
                db.session.add(new_sub)
                db.session.commit()
                flash('Subject added successfully!',"success")
            return redirect(url_for('home'))

    else:
        flash('You are not authorized to access this page!',"danger")
        return redirect(url_for('home'))
    
@app.route('/add_chapter/<int:subject_id>', methods=['GET','POST'])
def add_chapter(subject_id):

    if session.get('is_admin') == True:
        if request.method == 'GET':
            return render_template('add_chapter.html', subject_id=subject_id)
        
        if request.method == 'POST':
            name = request.form.get('name',None)
            description = request.form.get('description',None)

            if not name or not description:
                flash('Chapter Name and Description are Mandatory!',"danger")
                return redirect(url_for('add_chapter', subject_id=subject_id))
            
            chap = Chapter.query.filter_by(chap_name=name, sub_id=subject_id).first()
            if chap:
                flash('Chapter already exists, create a new one!',"danger")
                return redirect(url_for('add_chapter', subject_id=subject_id))
            else:
                new_chap = Chapter(
                    chap_name = name,
                    chap_desc = description,
                    sub_id = subject_id
                )
                db.session.add(new_chap)
                db.session.commit()
                flash('Chapter added successfully!',"success")
                chapters = Chapter.query.filter_by(sub_id=subject_id).all()
            return redirect(url_for('view_subject', subject_id=subject_id))
    else:
        flash('You are not authorized to access this page!',"danger")
        return redirect(url_for('home'))
        
@app.route('/view_subject/<int:subject_id>', methods=['GET'])
def view_subject(subject_id):
    if session.get('is_admin') == True:
        subject = Subject.query.filter_by(sub_id=subject_id).first()
        chapters = Chapter.query.filter_by(sub_id=subject_id).all()

        if not subject:
            flash('Subject not found!', 'danger')
            return redirect(url_for('home'))

        return render_template('view_subject.html', chapters=chapters, subject=subject)

    else:
        flash('You are not authorized to access this page!', "danger")
        return redirect(url_for('home'))

@app.route('/add_quiz/<int:chapter_id>', methods=['GET','POST'])
def add_quiz(chapter_id):
    if session.get('is_admin') == True:
        if request.method == 'GET':
            return render_template('add_quiz.html', chapter_id=chapter_id)
        
        if request.method == 'POST':
            name = request.form.get('name',None)

            if not name:
                flash('Quiz Name and Number of Questions are Mandatory!',"danger")
                return redirect(url_for('add_quiz', chapter_id=chapter_id))
            
            quiz = Quiz.query.filter_by(quiz_name=name, chap_id=chapter_id).first()
            if quiz:
                flash('Quiz already exists, create a new one!',"danger")
                return redirect(url_for('add_quiz', chapter_id=chapter_id))
            else:
                new_quiz = Quiz(
                    quiz_name = name,
                    chap_id = chapter_id,
                )
                db.session.add(new_quiz)
                db.session.commit()
                flash('Quiz added successfully!',"success")
            return redirect(url_for('view_chapter', chapter_id=chapter_id))
        
@app.route('/view_chapter/<int:chapter_id>', methods=['GET'])
def view_chapter(chapter_id):
    if session.get('is_admin') == True:
        if request.method == 'GET':
            chapter = Chapter.query.filter_by(chap_id=chapter_id).first()
            quizzes = Quiz.query.filter_by(chap_id=chapter_id).all()

            if not chapter:
                flash('Chapter not found!', 'danger')
                return redirect(url_for('home'))

            return render_template('view_chapter.html', quizzes=quizzes, chapter=chapter)

    else:
        flash('You are not authorized to access this page!', "danger")
        return redirect(url_for('home'))
    
@app.route('/add_ques/<int:q_id>', methods=['GET','POST'])
def add_ques(q_id):
    if session.get('is_admin') == True:
        if request.method == 'GET':
            return render_template('add_ques.html', q_id=q_id)
        
        if request.method == 'POST':
            ques = request.form.get('ques',None)
            opt1 = request.form.get('opt1',None)
            opt2 = request.form.get('opt2',None)
            opt3 = request.form.get('opt3',None)
            opt4 = request.form.get('opt4',None)
            ans = request.form.get('ans',None)

            if not ques or not opt1 or not opt2 or not opt3 or not opt4 or not ans:
                flash('All fields are Mandatory!',"danger")
                return redirect(url_for('add_ques', q_id=q_id))
            
            new_ques = Question(
                quiz_id = q_id,
                ques = ques,
                option1 = opt1,
                option2 = opt2,
                option3 = opt3,
                option4 = opt4,
                ans = ans
            )
            quiz = Quiz.query.filter_by(quiz_id=q_id).first()
            quiz.num_ques += 1
            db.session.add(new_ques)
            db.session.commit()
            flash('Question added successfully!',"success")
            return redirect(url_for('view_quiz', q_id=q_id))
        
@app.route('/view_quiz/<int:q_id>', methods=['GET'])
def view_quiz(q_id):
    if session.get('is_admin') == True:
        if request.method == 'GET':
            quiz = Quiz.query.filter_by(quiz_id=q_id).first()
            questions = Question.query.filter_by(quiz_id=q_id).all()

            if not quiz:
                flash('Quiz not found!', 'danger')
                return redirect(url_for('home'))

            return render_template('view_quiz.html', questions=questions, quiz=quiz)
        
@app.route('/edit_subject/<int:subject_id>', methods=['GET','POST'])
def edit_subject(subject_id):
    if session.get('is_admin') == True:
        if request.method == 'GET':
            subject = Subject.query.filter_by(sub_id=subject_id).first()
            return render_template('edit_subject.html', subject_id=subject_id, subject=subject)
        
        if request.method == 'POST':
            name = request.form.get('name',None)
            description = request.form.get('description',None)
            
            if not name or not description:
                flash('Subject Name and Description are Mandatory!',"danger")
                return redirect(url_for('edit_subject', subject_id=subject_id))
            
            sub = Subject.query.filter_by(sub_id=subject_id).first()
            sub.sub_name = name
            sub.sub_desc = description
            db.session.commit()
            flash('Subject updated successfully!',"success")
            return redirect(url_for('home'))
        
@app.route('/edit_chapter/<int:chapter_id>', methods=['GET','POST'])
def edit_chapter(chapter_id):
    if session.get('is_admin') == True:
        if request.method == 'GET':
            chapter = Chapter.query.filter_by(chap_id=chapter_id).first()
            return render_template('edit_chapter.html', chapter_id=chapter_id, chapter=chapter)
        
        if request.method == 'POST':
            name = request.form.get('name',None)
            description = request.form.get('description',None)
            
            if not name or not description:
                flash('Chapter Name and Description are Mandatory!',"danger")
                return redirect(url_for('edit_chapter', chapter_id=chapter_id))
            
            chap = Chapter.query.filter_by(chap_id=chapter_id).first()
            chap.chap_name = name
            chap.chap_desc = description
            db.session.commit()
            flash('Chapter updated successfully!',"success")
            return redirect(url_for('view_subject', subject_id=chap.sub_id))
        
@app.route('/edit_quiz/<int:quiz_id>', methods=['GET','POST'])
def edit_quiz(quiz_id):
    if session.get('is_admin') == True:
        if request.method == 'GET':
            quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
            return render_template('edit_quiz.html', quiz_id=quiz_id, quiz=quiz)
        
        if request.method == 'POST':
            name = request.form.get('name',None)
            
            if not name:
                flash('Quiz Name is Mandatory!',"danger")
                return redirect(url_for('edit_quiz', quiz_id=quiz_id))
            
            q = Quiz.query.filter_by(quiz_id=quiz_id).first()
            q.quiz_name = name
            db.session.commit()
            flash('Quiz updated successfully!',"success")
            return redirect(url_for('view_chapter', chapter_id=q.chap_id))
        
@app.route('/edit_ques/<int:ques_id>', methods=['GET','POST'])
def edit_ques(ques_id):
    if session.get('is_admin') == True:
        if request.method == 'GET':
            ques = Question.query.filter_by(ques_id=ques_id).first()
            return render_template('edit_ques.html', ques_id=ques_id, ques=ques)
        
        if request.method == 'POST':
            ques = request.form.get('ques',None)
            opt1 = request.form.get('opt1',None)
            opt2 = request.form.get('opt2',None)
            opt3 = request.form.get('opt3',None)
            opt4 = request.form.get('opt4',None)
            ans = request.form.get('ans',None)

            if not ques or not opt1 or not opt2 or not opt3 or not opt4 or not ans:
                flash('All fields are Mandatory!',"danger")
                return redirect(url_for('edit_ques', ques_id=ques_id))
            
            q = Question.query.filter_by(ques_id=ques_id).first()
            q.ques = ques
            q.option1 = opt1
            q.option2 = opt2
            q.option3 = opt3
            q.option4 = opt4
            q.ans = ans
            db.session.commit()
            flash('Question updated successfully!',"success")
            return redirect(url_for('view_quiz', q_id=q.quiz_id))

@app.route('/delete_subject/<int:subject_id>', methods=['GET'])
def delete_subject(subject_id):
    if session.get('is_admin') == True:
        subject = Subject.query.filter_by(sub_id=subject_id).first()
        if not subject:
            flash('Subject not found!', 'danger')
            return redirect(url_for('home'))
        
        db.session.delete(subject)
        db.session.commit()
        flash('Subject deleted successfully!', 'success')
        return redirect(url_for('home'))
    
    else:
        flash('You are not authorized to access this page!', "danger")
        return redirect(url_for('home'))

@app.route('/delete_chapter/<int:chapter_id>', methods=['GET'])
def delete_chapter(chapter_id):
    if session.get('is_admin') == True:
        chapter = Chapter.query.filter_by(chap_id=chapter_id).first()
        subject_id = chapter.sub_id
        if not chapter:
            flash('Chapter not found!', 'danger')
            return redirect(url_for('home'))
        
        db.session.delete(chapter)
        db.session.commit()
        flash('Chapter deleted successfully!', 'success')
        return redirect(url_for('view_subject', subject_id=subject_id))
    
    else:
        flash('You are not authorized to access this page!', "danger")
        return redirect(url_for('home'))
    
@app.route('/delete_quiz/<int:quiz_id>', methods=['GET'])
def delete_quiz(quiz_id):
    if session.get('is_admin') == True:
        quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
        chapter_id = quiz.chap_id
        if not quiz:
            flash('Quiz not found!', 'danger')
            return redirect(url_for('home'))
        
        db.session.delete(quiz)
        db.session.commit()
        flash('Quiz deleted successfully!', 'success')
        return redirect(url_for('view_chapter', chapter_id=chapter_id))
    
    else:
        flash('You are not authorized to access this page!', "danger")
        return redirect(url_for('home'))

@app.route('/delete_ques/<int:ques_id>', methods=['GET'])
def delete_ques(ques_id):
    if session.get('is_admin') == True:
        ques = Question.query.filter_by(ques_id=ques_id).first()
        quiz_id = ques.quiz_id
        if not ques:
            flash('Question not found!', 'danger')
            return redirect(url_for('home'))
        quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
        quiz.num_ques -= 1
        db.session.delete(ques)
        db.session.commit()
        flash('Question deleted successfully!', 'success')
        return redirect(url_for('view_quiz', q_id=quiz_id))
    
    else:
        flash('You are not authorized to access this page!', "danger")
        return redirect(url_for('home'))
    
@app.route('/submit_quiz/<int:quiz_id>', methods=['GET','POST'])
def submit_quiz(quiz_id):
    if session.get('user_email'):
        if request.method == 'GET':
            quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
            questions = Question.query.filter_by(quiz_id=quiz_id).all()

            if not quiz:
                flash('Quiz not found!', 'danger')
                return redirect(url_for('home'))

            return render_template('submit_quiz.html', questions=questions, quiz=quiz)
        
        if request.method == 'POST':
            score = 0
            quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
            questions = Question.query.filter_by(quiz_id=quiz_id).all()
            for ques in questions:
                ans = request.form.get(str(ques.ques_id),None)
                if ans == ques.ans:
                    score += 1
            new_score = Scores(
                user_id = session.get('user_id'),
                quiz_id = quiz_id,
                score_total = score,
                time_attempted = datetime.now()
            )
            db.session.add(new_score)
            db.session.commit()
            flash('Quiz submitted successfully!',"success")
            quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
            return redirect(url_for('user_result',quiz_id=quiz_id, score=new_score, quiz=quiz))
    else:
        flash('You are not authorized to access this page!', "danger")
        return redirect(url_for('home'))

@app.route('/user_result/<int:quiz_id>', methods=['GET'])
def user_result(quiz_id):
    if session.get('user_email'):
        if request.method == 'GET':
            score = Scores.query.filter_by(user_id=session.get('user_id'),quiz_id=quiz_id).first()
            quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
            return render_template('user_result.html', score=score, quiz=quiz)
    else:
        flash('You are not authorized to access this page!', "danger")
        return redirect(url_for('home'))