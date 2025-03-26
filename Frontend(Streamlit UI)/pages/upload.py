import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

def show_upload_page():
    """Streamlit page to upload files."""
    st.title("📤 Upload File")

    # ✅ Ensure user is logged in
    auth_token = st.session_state.get("auth_token")
    user_email = st.session_state.get("user_email")

    if not auth_token or not user_email:
        st.error("⚠️ Please log in first!")
        st.stop()  # ✅ Stops execution if not logged in

    uploaded_file = st.file_uploader("📂 Choose a file:", type=["csv", "xlsx", "json"])

    if uploaded_file:
        st.success(f"✅ File `{uploaded_file.name}` selected!")

        if st.button("🚀 Upload File"):
            with st.spinner("📡 Uploading file..."):
                try:
                    # ✅ Ensure file data is read before sending
                    file_data = uploaded_file.getvalue()
                    if not file_data:
                        st.error("❌ File is empty. Please upload a valid file.")
                        return

                    files = {"file": (uploaded_file.name, file_data)}
                    headers = {"Authorization": f"Bearer {auth_token}"}
                    data = {"email": user_email}  # ✅ Ensure user email is sent

                    response = requests.post(f"{API_URL}/upload", files=files, data=data, headers=headers)

                    if response.status_code == 201:
                        st.success("✅ File uploaded successfully!")
                    elif response.status_code == 401:
                        st.warning("⚠️ Session expired. Please log in again.")
                        st.session_state.clear()  # ✅ Clears session on token expiry
                        st.rerun()
                    else:
                        try:
                            error_message = response.json().get("error", "Unknown error")
                        except requests.exceptions.JSONDecodeError:
                            error_message = f"Unexpected response: {response.text}"

                        st.error(f"❌ Upload failed: {error_message}")

                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Network error: {str(e)}")

# ✅ Run function
if __name__ == "__main__":
    show_upload_page()
