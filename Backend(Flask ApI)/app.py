# import os
# from datetime import datetime
#
# from flask import Flask, request, jsonify
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from flask_sqlalchemy import SQLAlchemy
# from flask_wtf.csrf import CSRFProtect
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sql-404@localhost/business_data_automation'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'your_secret_key'
# app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
# app.config['UPLOAD_FOLDER'] = 'uploads'  # ✅ File Upload Folder
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # ✅ Create folder if not exists
#
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# jwt = JWTManager(app)
# csrf = CSRFProtect()
# csrf.init_app(app)
# csrf._disable_on_blueprints = True  # Disable CSRF for API routes
#
#
# class User_detail(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     full_name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#
#
# class UploadedFile(db.Model):  # ✅ Table to store uploaded file details
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user_detail.id'), nullable=False)
#     filename = db.Column(db.String(255), nullable=False)
#     upload_time = db.Column(db.TIMESTAMP, default=datetime.utcnow)
#
#
# # Signup Route
# @app.route('/signup', methods=['POST'])
# @csrf.exempt
# def signup():
#     data = request.json
#     full_name = data.get('full_name')
#     email = data.get('email')
#     password = data.get('password')
#
#     if not full_name or not email or not password:
#         return jsonify({"error": "All fields are required"}), 400
#
#     if User_detail.query.filter_by(email=email).first():
#         return jsonify({"error": "Email already registered"}), 400
#
#     hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#     new_user = User_detail(full_name=full_name, email=email, password=hashed_password)
#
#     try:
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify({"message": "User registered successfully!"}), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": "Database error"}), 500
#
#
# # Login Route
# @app.route('/login', methods=['POST'])
# @csrf.exempt
# def login():
#     data = request.json
#     email = data.get('email')
#     password = data.get('password')
#
#     user = User_detail.query.filter_by(email=email).first()
#
#     # ✅ Debugging Statements
#     print(f"User fetched from DB: {user}")  # Check if user exists
#     if user:
#         print(f"Stored Hashed Password: {user.password}")
#         print(f"Entered Password: {password}")
#         print(f"Password Match: {bcrypt.check_password_hash(user.password, password)}")
#
#     if not user:
#         return jsonify({"error": "Invalid credentials"}), 401
#
#     if bcrypt.check_password_hash(user.password, password):
#         access_token = create_access_token(identity=email)
#
#         return jsonify({
#             "message": "Login successful!",
#             "token": access_token,
#             "user": {"id": user.id, "full_name": user.full_name, "email": user.email}
#         }), 200
#
#     return jsonify({"error": "Invalid credentials"}), 401
#
#
# # Upload File Route
# @app.route('/upload', methods=['POST'])
# @csrf.exempt
# @jwt_required()
# def upload_file():
#     try:
#         if 'file' not in request.files:
#             return jsonify({"error": "No file uploaded"}), 400
#
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({"error": "No selected file"}), 400
#
#         current_user = get_jwt_identity()
#         user = User_detail.query.filter_by(email=current_user).first()
#
#         if not user:
#             return jsonify({"error": "User not found"}), 404
#
#         # ✅ Debugging Statements
#         print(f"User ID: {user.id}")  # Check user_id
#         print(f"Uploading file: {file.filename}")  # Check filename
#
#         # ✅ Store File in DB
#         new_file = UploadedFile(user_id=user.id, filename=file.filename)
#         db.session.add(new_file)
#         db.session.commit()
#
#         return jsonify({"message": "File uploaded successfully!", "filename": file.filename}), 201
#
#     except Exception as e:
#         db.session.rollback()
#         print(f"Upload Error: {str(e)}")  # Print error in terminal
#         return jsonify({"error": f"Database error: {str(e)}"}), 500
#
#
# # Get Upload History
# @app.route('/history', methods=['GET'])
# @csrf.exempt
# @jwt_required()
# def get_upload_history():
#     current_user = get_jwt_identity()  # ✅ Get logged-in user email
#     user = User_detail.query.filter_by(email=current_user).first()
#
#     if not user:
#         return jsonify({"error": "User not found"}), 404
#
#     # ✅ Fetch uploaded files of the logged-in user
#     uploaded_files = UploadedFile.query.filter_by(user_id=user.id).all()
#
#     # ✅ Convert to JSON format
#     files_data = [
#         {"filename": file.filename, "upload_time": file.upload_time.strftime("%Y-%m-%d %H:%M:%S")}
#         for file in uploaded_files
#     ]
#
#     return jsonify({"files": files_data}), 200
#
#
# # Run Flask App
# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)


import os
from datetime import datetime
from dotenv import load_dotenv  # ✅ Load environment variables

from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# ✅ Load .env file
load_dotenv()

app = Flask(__name__)

print("Database URL:", os.getenv("DATABASE_URL"))
# ✅ Use Supabase Connection from .env
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your_secret_key")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
app.config['UPLOAD_FOLDER'] = 'uploads'  # ✅ File Upload Folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # ✅ Create folder if not exists

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
csrf = CSRFProtect()
csrf.init_app(app)
csrf._disable_on_blueprints = True  # Disable CSRF for API routes


class User_detail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class UploadedFile(db.Model):  # ✅ Table to store uploaded file details
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_detail.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    upload_time = db.Column(db.TIMESTAMP, default=datetime.utcnow)


# Signup Route
@app.route('/signup', methods=['POST'])
@csrf.exempt
def signup():
    data = request.json
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')

    if not full_name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if User_detail.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User_detail(full_name=full_name, email=email, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500


# Login Route
@app.route('/login', methods=['POST'])
@csrf.exempt
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User_detail.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=email)

    return jsonify({
        "message": "Login successful!",
        "token": access_token,
        "user": {"id": user.id, "full_name": user.full_name, "email": user.email}
    }), 200


# Upload File Route
@app.route('/upload', methods=['POST'])
@csrf.exempt
@jwt_required()
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        current_user = get_jwt_identity()
        user = User_detail.query.filter_by(email=current_user).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # ✅ Store File in DB
        new_file = UploadedFile(user_id=user.id, filename=file.filename)
        db.session.add(new_file)
        db.session.commit()

        return jsonify({"message": "File uploaded successfully!", "filename": file.filename}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500


# Get Upload History
@app.route('/history', methods=['GET'])
@csrf.exempt
@jwt_required()
def get_upload_history():
    current_user = get_jwt_identity()  # ✅ Get logged-in user email
    user = User_detail.query.filter_by(email=current_user).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    uploaded_files = UploadedFile.query.filter_by(user_id=user.id).all()

    files_data = [
        {"filename": file.filename, "upload_time": file.upload_time.strftime("%Y-%m-%d %H:%M:%S")}
        for file in uploaded_files
    ]

    return jsonify({"files": files_data}), 200


# Run Flask App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



