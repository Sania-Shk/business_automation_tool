from flask_bcrypt import Bcrypt  # (Password hashing, so It won't store raw data)
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()


#  User Table
class UserDetail(db.Model, UserMixin):
    __tablename__ = "user_detail"  # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)  # ✅ FIXED: Changed full_name → firstname
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Hashed password

    # Flask-Login required methods
    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)  # return user-ID, that flask uses to recognize


#  Uploaded Files Table
class UploadedFile(db.Model):
    __tablename__ = "uploaded_file"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_detail.id'), nullable=False)  # ✅ Changed user_email → user_id
    filename = db.Column(db.String(255), nullable=False)
    upload_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())


#  Function to initialize database
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
