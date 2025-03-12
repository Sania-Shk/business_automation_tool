import streamlit as st
import pandas as pd
import requests

BASE_URL = "http://127.0.0.1:5000"

def show_upload_page():
    st.title("📤 Upload Your File")
    st.write("Upload a CSV, Excel, or JSON file to store in database and process.")

    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "json"])

    if uploaded_file is not None:
        st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")

        # ✅ Display File Preview
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith(".json"):
                df = pd.read_json(uploaded_file)
            else:
                st.error("Unsupported file format.")
                return

            st.write("📂 **File Preview:**")
            st.dataframe(df.head())  # ✅ Show first 5 rows of file

            # ✅ Upload File to Flask Backend
            if st.button("Save to Database"):
                token = st.session_state.get("auth_token")  # Fetch user token
                user_id = st.session_state.get("user_id")  # ✅ Get user_id from session

                if not token or not user_id:
                    st.error("⚠️ Please log in first!")
                    return

                files = {"file": uploaded_file}
                headers = {"Authorization": f"Bearer {token}"}  # ✅ JWT Token sent
                data = {"user_id": user_id}  # ✅ Pass user_id while uploading
                response = requests.post(f"{BASE_URL}/upload", files=files, headers=headers, data=data)

                if response.status_code == 201:
                    st.success("✅ File saved to database successfully!")
                else:
                    st.error(f"❌ Upload failed: {response.json().get('error', 'Unknown error')}")

        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

# ✅ Call function when script runs
if __name__ == "__main__":
    show_upload_page()
