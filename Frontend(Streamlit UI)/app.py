import streamlit as st
from pages.login import show_login_page
from pages.signup import show_signup_page
from pages.upload import show_upload_page
from pages.history import show_history_page
from pages.process_visual import show_process_visual_page  # 🆕


# ⬇️ Load CSS
def load_css():
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.set_page_config(page_title="Business Data Entry Automation", layout="wide")
load_css()  # Apply the custom CSS

# Sidebar Navigation
st.sidebar.title("📁 Business Automation")
page = st.sidebar.radio("Navigate", [
    "Home", "Login", "Signup", "Upload File",
    "Recent Files", "Process & Visualize"  # 🆕
])

# Page Routing
if page == "Home":
    st.markdown("## 🏠 Welcome to **Business Data Entry Automation**")

    st.markdown("""
    <div style='font-size:17px; line-height:1.7'>
        <span title='Our system helps users save time by automatically analyzing and cleaning messy business data.'>
        📌 This project automates the process of uploading, cleaning, and visualizing business datasets
        </span><br><br>
        <span title='Upload formats include CSV, Excel, and JSON. Cleaned data can be downloaded or visualized directly.'>
        💡 You can upload `.csv`, `.xlsx`, or `.json` files, and our system will handle null values, outliers, and duplicates.
        </span><br><br>
        <span title='Visualize key metrics using pie charts, bar graphs, groupby insights and more.'>
        📊 After cleaning, the system also generates interactive charts and summaries for analysis.
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 3-Step Walkthrough Section
    st.markdown("### 🔄 How It Works (3 Easy Steps)")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📤 Upload")
        st.markdown("Upload your business dataset in `.csv`, `.xlsx`, or `.json` format.")

    with col2:
        st.markdown("#### 🛠️ Auto Clean")
        st.markdown("The system automatically cleans your data: handles missing values, removes outliers & duplicates.")

    with col3:
        st.markdown("#### 📊 Visualize")
        st.markdown("Generate beautiful charts and key insights for fast and effective decision-making.")

    st.markdown("---")
    st.info("✨ Use the sidebar to login or get started right away by uploading your first file!")

elif page == "Login":
    show_login_page()

elif page == "Signup":
    show_signup_page()

elif page == "Upload File":
    st.header("📤 Upload File")
    show_upload_page()

elif page == "Recent Files":
    st.header("🕘 Recent Uploaded Files")
    show_history_page()

elif page == "Process & Visualize":
    st.header("📊 Process & Visualize Your Dataset")
    show_process_visual_page()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("🔒 Secure • 🚀 Fast • 💡 Smart")
st.sidebar.markdown("Developed by San & Team")
