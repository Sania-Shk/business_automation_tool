import os
from datetime import datetime

from dotenv import load_dotenv  # Load environment variables
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# from utils.processing import process_data

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from utils.processing import process_data

#  Load .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your_secret_key")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure upload folder exists

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
csrf = CSRFProtect(app)
csrf.init_app(app)
csrf._disable_on_blueprints = True


# Database Models
class User_detail(db.Model):
    __tablename__ = "user_detail"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class UploadedFile(db.Model):
    __tablename__ = "uploaded_file"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_detail.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    upload_time = db.Column(db.TIMESTAMP, default=datetime.utcnow)


class ProcessedData(db.Model):
    __tablename__ = "processed_data"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_detail.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    processed_json = db.Column(db.JSON, nullable=False)
    changes = db.Column(db.JSON, nullable=False)
    processed_time = db.Column(db.TIMESTAMP, default=datetime.utcnow)


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

        #  Store File in DB
        new_file = UploadedFile(user_id=user.id, filename=file.filename)
        db.session.add(new_file)
        db.session.commit()

        return jsonify({"message": "File uploaded successfully!", "filename": file.filename}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500


# # Process Data Route
# @app.route('/process-data', methods=['POST'])
# @jwt_required()
# def process_data_api():
#     try:
#         if 'file' not in request.files:
#             return jsonify({"error": "No file uploaded"}), 400
#
#         file = request.files['file']
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(file_path)
#
#         processed_df, changes = process_data(file_path)
#         if processed_df is None:
#             return jsonify({"error": "Processing failed", "details": changes}), 500
#
#         processed_json = processed_df.to_dict(orient='records')
#         current_user = get_jwt_identity()
#         user = User_detail.query.filter_by(email=current_user).first()
#
#         if not user:
#             return jsonify({"error": "User not found"}), 404
#
#         new_processed = ProcessedData(user_id=user.id, filename=file.filename, processed_json=processed_json,
#                                       changes=changes)
#         db.session.add(new_processed)
#         db.session.commit()
#
#         return jsonify({"processed_data": processed_json, "changes": changes}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500
#
#
# # Get Processed Data Route
# @app.route('/get-processed-data', methods=['GET'])
# @jwt_required()
# def get_processed_data():
#     current_user = get_jwt_identity()
#     user = User_detail.query.filter_by(email=current_user).first()
#     if not user:
#         return jsonify({"error": "User not found"}), 404
#
#     processed_data = ProcessedData.query.filter_by(user_id=user.id).order_by(
#         ProcessedData.processed_time.desc()).first()
#     if not processed_data:
#         return jsonify({"error": "No processed data found"}), 404
#
#     return jsonify({"processed_data": processed_data.processed_json, "changes": processed_data.changes}), 200


# Get User History Route
@app.route('/history', methods=['GET'])
@csrf.exempt
@jwt_required()
def get_upload_history():
    current_user = get_jwt_identity()  # Get logged-in user email
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
