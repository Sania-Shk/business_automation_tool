import streamlit as st
import requests
import plotly.express as px
import pandas as pd
from io import BytesIO

API_URL = "http://127.0.0.1:5000"  # Change this if using a deployed backend

def show_visualization_page():
    """Streamlit page for visualizing processed files."""
    st.title("📊 Data Visualization")

    # ✅ Ensure user is logged in
    auth_token = st.session_state.get("auth_token")
    if not auth_token:
        st.warning("⚠️ Please log in first!")
        return

    headers = {"Authorization": f"Bearer {auth_token}"}

    # ✅ Fetch processed files from API
    try:
        response = requests.get(f"{API_URL}/processed_files", headers=headers)
        if response.status_code == 200:
            processed_files = response.json().get("processed_files", [])
        elif response.status_code == 401:
            st.warning("⚠️ Session expired. Please log in again.")
            return
        else:
            st.error(f"❌ Failed to fetch processed files: {response.json().get('error', 'Unknown error')}")
            return
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Network error: {str(e)}")
        return

    # ✅ File selection dropdown
    if processed_files:
        selected_file = st.selectbox("📂 Select a processed file:", [file["filename"] for file in processed_files])
        file_url = next(file["download_url"] for file in processed_files if file["filename"] == selected_file)

        # ✅ Fetch selected file's data
        try:
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                file_content = file_response.content
                df = pd.read_csv(BytesIO(file_content))

                # ✅ Display Data Preview
                st.write("📋 **Processed Data Preview:**")
                st.dataframe(df.head())

                # ✅ Select columns for visualization
                numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
                if not numeric_columns:
                    st.warning("⚠️ No numeric columns available for visualization.")
                    return

                x_axis = st.selectbox("📈 Select X-axis:", numeric_columns)
                y_axis = st.selectbox("📊 Select Y-axis:", numeric_columns)

                # ✅ Create Plotly visualization
                fig = px.scatter(df, x=x_axis, y=y_axis, title="📊 Data Visualization", size_max=15)
                st.plotly_chart(fig)

            else:
                st.error(f"❌ Error fetching file: {file_response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Network error: {str(e)}")
    else:
        st.warning("⚠️ No processed files available for visualization.")


# ✅ Run function
if __name__ == "__main__":
    show_visualization_page()
