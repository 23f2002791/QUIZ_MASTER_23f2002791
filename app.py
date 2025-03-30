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
            user_email = 'admin@gmail.com',
            user_password = 'admin@1234',
            full_name = 'QuizMaster Admin',
            is_admin = True
        )
        db.session.add(admin)
    db.session.commit()

from controllers.auth_routes import *
from controllers.routes import *

if __name__ == '__main__':
    app.run(debug=True)