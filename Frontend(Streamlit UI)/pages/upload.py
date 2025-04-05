import streamlit as st
import requests
import pandas as pd
import io

# ⬇ Load CSS
def load_css():
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:5000"

def show_upload_page():
    """Streamlit page to upload files."""
    st.title("📤 Upload File")

    # ✅ Ensure user is logged in
    auth_token = st.session_state.get("auth_token")
    user_email = st.session_state.get("user_email")

    if not auth_token or not user_email:
        st.error("⚠️ Please log in first!")
        st.stop()

    uploaded_file = st.file_uploader("📂 Choose a file:", type=["csv", "xlsx", "json"])

    if uploaded_file:
        st.success(f"✅ File `{uploaded_file.name}` selected!")

        try:
            # ✅ Load file based on extension
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith(".json"):
                df = pd.read_json(uploaded_file)
            else:
                st.warning("⚠️ Unsupported file type.")
                return

            # ✅ Save preview and columns in session
            st.session_state["uploaded_df"] = df
            st.session_state["uploaded_columns"] = list(df.columns)

            # ✅ Show file preview
            with st.expander("🔍 Preview File"):
                st.dataframe(df.head())

        except Exception as e:
            st.error(f"❌ Failed to preview file: {e}")
            return

        # ✅ Upload button
        if st.button("🚀 Upload File"):
            with st.spinner("📡 Uploading file..."):
                try:
                    file_data = uploaded_file.getvalue()
                    if not file_data:
                        st.error("❌ File is empty. Please upload a valid file.")
                        return

                    files = {"file": (uploaded_file.name, file_data)}
                    headers = {"Authorization": f"Bearer {auth_token}"}
                    data = {"email": user_email}

                    response = requests.post(f"{API_URL}/upload", files=files, data=data, headers=headers)

                    if response.status_code == 201:
                        st.success("✅ File uploaded successfully!")

                        # ✅ Show stored column names
                        if "uploaded_columns" in st.session_state:
                            st.subheader("🧾 Columns in Uploaded File:")
                            st.write(st.session_state["uploaded_columns"])

                    elif response.status_code == 401:
                        st.warning("⚠️ Session expired. Please log in again.")
                        st.session_state.clear()
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
