from main import app
from flask import render_template, request, session, flash, redirect, url_for
from controllers.models import *
from datetime import datetime

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'GET':
        if 'user_id' in session:
            # yet to write the redirect part
            return redirect(url_for('home'))
        return render_template('login.html')

    if request.method == 'POST':
        email = request.form.get('email',None)
        password = request.form.get('password',None)

        #data validation
        if not email or not password:
            flash('Enter Email and Password!',"danger")
            return redirect(url_for('login'))
        if '@' and '.' not in email or len(email) < 7 or ' ' in email:
            flash('Enter a valid Email!',"danger")
            return redirect(url_for('login'))
        if len(password) < 8 or len(password) > 20:
            flash('Password must be 8-20 characters long!',"danger")
            return redirect(url_for('login'))
        
        #check if user exists
        user = User.query.filter_by(user_email=email).first()
        if not user:
            flash('User does not exists! Try Again!', "danger")
            return redirect(url_for('login'))
        
        if user.user_password != password:
            flash('Invalid Password! Try Again!', "danger")
            return redirect(url_for('login'))
        
        session['user_id'] = user.user_id
        session['user_email'] = user.user_email
        session['full_name'] = user.full_name
        session['is_admin'] = user.is_admin
        
        #return url to home page (yet to do)
        flash('You are logged in successfully!', "success")
        return redirect(url_for('home'))


@app.route('/logout')
def logout():
    if 'user_email' not in session:
        flash('You are not logged in!',"danger")
        return redirect(url_for('login'))
    
    session.pop('user_id')
    session.pop('user_email')
    session.pop('full_name')
    session.pop('is_admin')
    session.clear()
    flash('You are logged out successfully!', "success")
    return redirect(url_for('login'))


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        email = request.form.get('email',None)
        password = request.form.get('password',None)
        name = request.form.get('name',None)
        qual = request.form.get('qual',None)
        dateofbirth = request.form.get('dateofbirth')

        if dateofbirth:
            try:
                dateofbirth = datetime.strptime(dateofbirth, '%Y-%m-%d').date()  # Format based on your input
            except ValueError:
                return "Invalid date format. Please use YYYY-MM-DD.", 400
        else:
            dateofbirth = None

        #data validation
        if not email or not password or not name:
            flash('Email, Password and Full Name are Mandatory!', "danger")
            return redirect(url_for('register'))
        if '@' and '.' not in email or len(email) < 7 or ' ' in email:
            flash('Enter a valid Email!',"danger")
            return redirect(url_for('register'))
        if len(password) < 8 or len(password) > 20:
            flash('Password must be 8-20 characters long!', "danger")
            return redirect(url_for('register'))
        
        #check if user exists
        user = User.query.filter_by(user_email=email).first()
        if user:
            flash('User already exists\n Please login or use a different Email!', "danger")
            return redirect(url_for('register'))
        
        user = User(
            user_email = email,
            user_password = password,
            full_name = name,
            qualification = qual,
            dob = dateofbirth
        )
        db.session.add(user)
        db.session.commit()
        flash('User Registered Successfully!',"success")

        return redirect(url_for('login'))    
        