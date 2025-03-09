from flask import Flask,render_template
from controllers.database import db
from controllers.config import Config
from controllers.models import *

app = Flask(__name__)
app.config.from_object(Config)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db.init_app(app)

with app.app_context():
    db.create_all()

    admin_user = User.query.filter_by(is_admin=True).first()
    if not admin_user:
        admin = User(
            user_email = 'QuizMaster Admin',
            password = 'admin@1234',
            full_name = 'QuizMaster Admin',
            is_admin = True
        )
        db.session.add(admin)
    db.session.commit()

@app.route('/')
def index():
    return render_template('hello.html')

@app.route('/about')
def about():
    return 'About page'

if __name__ == '__main__':
    app.run()