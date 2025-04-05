from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

class User_Detail(db.Model, UserMixin):
    __tablename__ = "user_detail"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    uploaded_files = db.relationship("UploadedFile", backref="user", cascade="all, delete-orphan")

class UploadedFile(db.Model):
    __tablename__ = "uploaded_file"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_detail.id", ondelete="CASCADE"), nullable=False)
    filename = db.Column(db.String(255), nullable=False, index=True)
    file_data = db.Column(db.LargeBinary, nullable=True)
    upload_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)


# ✅ Function to Initialize Database
def init_db(app):
    """Initializes the database schema."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
