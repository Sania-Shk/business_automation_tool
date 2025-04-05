import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from flask_migrate import Migrate

from database import db, UploadedFile, User_Detail

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your_secret_key")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
csrf = CSRFProtect(app)
csrf.init_app(app)
migrate = Migrate(app, db)

# ------------------ USER AUTHENTICATION ------------------

@app.route('/signup', methods=['POST'])
@csrf.exempt
def signup():
    data = request.json
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')

    if not full_name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if User_Detail.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User_Detail(full_name=full_name, email=email, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/login', methods=['POST'])
@csrf.exempt
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = User_Detail.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=email)

    return jsonify({
        "message": "Login successful!",
        "token": access_token,
        "user": {"id": user.id, "full_name": user.full_name, "email": user.email}
    }), 200

# ------------------ FILE UPLOAD & HISTORY ------------------

@app.route('/upload', methods=['POST'])
@csrf.exempt
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    current_user = get_jwt_identity()
    user = User_Detail.query.filter_by(email=current_user).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    file_data = file.read()
    if not file_data:
        return jsonify({"error": "File upload failed, no data read."}), 500

    new_file = UploadedFile(user_id=user.id, filename=secure_filename(file.filename), file_data=file_data)

    try:
        db.session.add(new_file)
        db.session.commit()
        return jsonify({"message": "File uploaded successfully!", "filename": file.filename}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route("/history", methods=["GET"])
@jwt_required()
@csrf.exempt
def get_user_history():
    current_user = get_jwt_identity()
    user = User_Detail.query.filter_by(email=current_user).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    uploaded_files = UploadedFile.query.filter_by(user_id=user.id).all()
    files_data = [{"filename": file.filename, "upload_time": file.upload_time.strftime("%Y-%m-%d %H:%M:%S")} for file in uploaded_files]

    return jsonify({"uploaded_files": files_data}), 200

# ------------------ GET USER FILES LIST ------------------

@app.route('/files/<email>', methods=['GET'])
@jwt_required()
@csrf.exempt
def get_user_files(email):
    current_user = get_jwt_identity()

    if current_user != email:
        return jsonify({"error": "Unauthorized access"}), 403

    user = User_Detail.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    files = UploadedFile.query.filter_by(user_id=user.id).all()
    filenames = [file.filename for file in files]

    return jsonify({"files": filenames}), 200

# ------------------ DOWNLOAD FILE BY NAME ------------------

@app.route('/download/<filename>', methods=['GET'])
@jwt_required()
@csrf.exempt
def download_file(filename):
    current_user = get_jwt_identity()
    user = User_Detail.query.filter_by(email=current_user).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    file_entry = UploadedFile.query.filter_by(user_id=user.id, filename=filename).first()

    if not file_entry:
        return jsonify({"error": "File not found"}), 404

    return file_entry.file_data, 200, {
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': f'attachment; filename={filename}'
    }

# ------------------ GET FILE DATA (For Visualization Page) ------------------

@app.route('/get_file_data', methods=['GET'])
@jwt_required()
@csrf.exempt
def get_file_data():
    email = get_jwt_identity()
    filename = request.args.get("filename")

    user = User_Detail.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    file_entry = UploadedFile.query.filter_by(user_id=user.id, filename=filename).first()

    if not file_entry:
        return jsonify({"error": "File not found"}), 404

    return file_entry.file_data, 200, {
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': f'attachment; filename={filename}'
    }

# ------------------ RUN FLASK APP ------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
