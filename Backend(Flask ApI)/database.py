from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

# ✅ User Table
class User_Detail(db.Model, UserMixin):
    __tablename__ = "user_detail"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)

    # ✅ Relationships
    uploaded_files = db.relationship("UploadedFile", backref="user", cascade="all, delete-orphan")
    processed_files = db.relationship("ProcessedFile", backref="user", cascade="all, delete-orphan")


# ✅ Uploaded Files Table
class UploadedFile(db.Model):
    __tablename__ = "uploaded_file"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_detail.id", ondelete="CASCADE"), nullable=False)
    filename = db.Column(db.String(255), nullable=False, index=True)
    file_data = db.Column(db.LargeBinary, nullable=True)  # ✅ Nullable in case of URL storage
    upload_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    # ✅ Relationship with ProcessedFile
    processed_files = db.relationship("ProcessedFile", backref="uploaded_file", cascade="all, delete-orphan")


# ✅ Processed Files Table (Improved)
class ProcessedFile(db.Model):
    __tablename__ = "processed_file"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_detail.id", ondelete="CASCADE"), nullable=False)
    uploaded_file_id = db.Column(db.Integer, db.ForeignKey("uploaded_file.id", ondelete="CASCADE"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(500), nullable=False)  # ✅ Store File URL Instead of Binary
    processed_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)


# ✅ Function to Initialize Database
def init_db(app):
    """Initializes the database schema."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
