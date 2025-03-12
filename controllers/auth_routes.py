from main import app
from flask import render_template, request, session, flash, redirect, url_for
from controllers.models import *

@app.route('/login', methods=['POST'])
def login():

    if request.method == 'GET':
        # if 'user_id' in session:
            #yet to write the redirect part
            # return redirect(url_for('home'))
        return render_template('login.html')

    if request.method == 'POST':
        email = request.form.get['email',None]
        password = request.form.get['password',None]

        #data validation
        if not email or not password:
            flash('Enter Email and Password!')
            return render_template('login.html')
        if '@' and '.' not in email or len(email) < 7 or ' ' in email:
            flash('Enter a valid Email!')
            return render_template('login.html')
        if len(password) < 8 or len(password) > 20:
            flash('Password must be 8-20 characters long!')
            return render_template('login.html')
        
        #check if user exists
        user = User.query.filter_by(user_email=email, user_password=password).first()
        if not user:
            flash('User does not exists! Try Again!')
            return render_template('login.html')
        if user.password != password:
            flash('Invalid Password! Try Again!')
            return render_template('login.html')
        
        session['user_id'] = user.user_id
        session['user_email'] = user.user_email
        session['full_name'] = user.full_name
        session['is_admin'] = user.is_admin
        
        #return url to home page (yet to do)


        user = User.query.filter_by(user_email=email, user_password=password).first()
        