from datetime import datetime
from datetime import datetime
from io import BytesIO

import numpy as np
import pandas as pd

from database import db, User_Detail, ProcessedFile


# ✅ Function to Process Data
def process_data(file_data, file_type):
    """Processes a user-uploaded file and applies data cleaning steps."""
    try:
        if file_data is None:
            print("❌ ERROR: `file_data` is None! Check file read operation.")
            return None, "Error: No file data found!"

        # ✅ Convert binary file data into a DataFrame
        if file_type == "csv":
            df = pd.read_csv(BytesIO(file_data))
        elif file_type == "xlsx":
            df = pd.read_excel(BytesIO(file_data))
        elif file_type == "json":
            df = pd.read_json(BytesIO(file_data))
        else:
            return None, "Unsupported file format"

        print(f"✅ DEBUG: Processing `{file_type}` file with shape {df.shape}")

        # ✅ Step 1: Handle Missing Values
        df.fillna(method='ffill', inplace=True)  # Forward fill missing values

        # ✅ Step 2: Remove Duplicates
        df.drop_duplicates(inplace=True)

        # ✅ Step 3: Normalize Numeric Columns
        for col in df.select_dtypes(include=[np.number]):
            if df[col].std() != 0:
                df[col] = (df[col] - df[col].mean()) / df[col].std()

        print("✅ DEBUG: File Processing Completed Successfully")
        return df, "✅ File Processed Successfully"

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return None, str(e)


# ✅ Function to Save Processed File
def save_processed_file(user_email, filename, df, file_type):
    """Saves the processed file and stores metadata in the database."""
    try:
        output = BytesIO()
        if file_type == "csv":
            df.to_csv(output, index=False)
        elif file_type == "xlsx":
            df.to_excel(output, index=False)
        elif file_type == "json":
            output.write(df.to_json().encode())

        output.seek(0)

        # ✅ Generate Unique Processed Filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"processed_{timestamp}_{filename}"
        file_url = f"/storage/{user_email}/{unique_filename}"  # ✅ Modify if using cloud storage

        # ✅ Find the user in the database
        user = User_Detail.query.filter_by(email=user_email).first()
        if not user:
            print(f"❌ DEBUG: User `{user_email}` not found in database.")
            return False, "User not found"

        # ✅ Save Processed File Entry in Database
        processed_file = ProcessedFile(
            user_id=user.id,
            filename=unique_filename,
            file_url=file_url
        )

        db.session.add(processed_file)
        db.session.commit()

        print(f"✅ DEBUG: Processed file saved for `{user_email}` - {file_url}")
        return True, file_url

    except Exception as e:
        db.session.rollback()
        print(f"❌ DEBUG: Error saving processed file - {e}")
        return False, str(e)
