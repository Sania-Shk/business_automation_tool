# import sys
# import streamlit as st
# import os
# import pandas as pd
#
# # Backend directory ka path dynamically resolve karo
# backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Backend (Flask API)"))
# sys.path.insert(0, backend_dir)
#
# print("Backend Path Added:", backend_dir)  # Debugging ke liye
#
# #   Import
# try:
#     from utils.processing import process_data
# except ModuleNotFoundError as e:
#     print("Error Importing processing.py:", e)
#
#
# # Streamlit UI
# st.title("Upload & Process Data")
#
# uploaded_file = st.file_uploader("Upload your dataset (.csv or .xlsx)", type=["csv", "xlsx"])
#
# if uploaded_file is not None:
#     file_path = os.path.join("uploads", uploaded_file.name)
#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())
#
#     st.success(f"File saved at: {file_path}")
#
#     # 🛠 Processing Call
#     df, changes, processed_file_path = process_data(file_path)
#
#     if df is not None:
#         st.success("Processing Completed!")
#
#         # Show Changes
#         st.write("### Changes Made:")
#         st.json(changes)
#
#         # Show Processed Data
#         st.write("### Processed Data Preview:")
#         st.dataframe(df.head())
#
#         # Download Processed File
#         with open(processed_file_path, "rb") as file:
#             st.download_button("Download Processed File", file, file_name="processed_data.csv", mime="text/csv")
#     else:
#         st.error("Error in processing! Please check the file format.")
