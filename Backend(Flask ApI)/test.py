
from database import db ,ProcessedFile, User_Detail


def test_processed_files():
    user_email = "person@gmail.com"
    user = User_Detail.query.filter_by(email=user_email).first()

    if not user:
        print("❌ User not found!")
        return

    processed_files = ProcessedFile.query.filter_by(user_id=user.id).all()

    if processed_files:
        print(f"✅ Found {len(processed_files)} processed files for {user_email}.")
        for file in processed_files:
            print(f"- {file.filename} | {file.file_url}")
    else:
        print("⚠️ No processed files found!")


if __name__ == "__main__":
    test_processed_files()
