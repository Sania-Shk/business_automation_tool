import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"  # Change this if using a deployed backend


def show_processed_data_page():
    """Streamlit page to view & download processed files."""
    st.title("📂 Processed Data")

    # ✅ Ensure user is logged in
    auth_token = st.session_state.get("auth_token")
    if not auth_token:
        st.warning("⚠️ Please log in first!")
        return

    headers = {"Authorization": f"Bearer {auth_token}"}

    # ✅ Fetch Processed Files from API
    st.write("📡 Fetching processed files from API...")

    try:
        response = requests.get(f"{API_URL}/processed_files", headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            files = response_data.get("processed_files", [])

            if files:
                selected_file = st.selectbox("📁 Select a processed file:", [file["filename"] for file in files])

                # ✅ Get selected file's download URL
                file_url = next(file["download_url"] for file in files if file["filename"] == selected_file)

                # ✅ Display File Information
                st.success(f"✅ File `{selected_file}` is available for download.")

                # ✅ Download Button
                st.markdown(f"[⬇️ Download Processed File]({file_url})", unsafe_allow_html=True)

            else:
                st.warning("⚠️ No processed files available.")

        elif response.status_code == 401:
            st.warning("⚠️ Session expired. Please log in again.")

        else:
            try:
                error_message = response.json().get("error", "Unknown error")
            except requests.exceptions.JSONDecodeError:
                error_message = f"Unexpected response: {response.text}"  # Debugging info

            st.error(f"❌ Failed to fetch processed files: {error_message}")

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Network error: {str(e)}")


# ✅ Run function
if __name__ == "__main__":
    show_processed_data_page()
