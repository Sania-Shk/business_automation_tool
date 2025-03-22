# import pandas as pd
# import os
# from sklearn.preprocessing import MinMaxScaler
#
# def process_data(file_path):
#     """
#     Process dataset by handling missing values, duplicates, outliers,
#     converting data types, and normalizing data.
#     """
#     changes = {}  # Dictionary to track modifications
#     try:
#         # Read the file
#         if file_path.endswith('.csv'):
#             df = pd.read_csv(file_path)
#         else:
#             df = pd.read_excel(file_path)
#
#         numeric_cols = df.select_dtypes(include=['number']).columns  # Numeric columns only
#
#         # 1. Handle Missing Values
#         missing_before = df[numeric_cols].isnull().sum().to_dict()
#         df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
#         missing_after = df[numeric_cols].isnull().sum().to_dict()
#         changes["missing_values"] = {"before": missing_before, "after": missing_after}
#
#         # 2. Handle Outliers using IQR method
#         outlier_count = {}
#         for col in numeric_cols:
#             Q1 = df[col].quantile(0.25)
#             Q3 = df[col].quantile(0.75)
#             IQR = Q3 - Q1
#             before_count = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
#             df[col] = df[col].clip(lower=Q1 - 1.5 * IQR, upper=Q3 + 1.5 * IQR)
#             after_count = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
#             outlier_count[col] = {"before": before_count, "after": after_count}
#         changes["outlier_handling"] = outlier_count
#
#         # 3. Remove Duplicates
#         duplicate_before = df.duplicated().sum()
#         df.drop_duplicates(inplace=True)
#         duplicate_after = df.duplicated().sum()
#         changes["duplicates"] = {"before": duplicate_before, "after": duplicate_after}
#
#         # 4. Convert Data Types (Only for numeric conversions)
#         converted_cols = {}
#         for col in df.select_dtypes(include=['object']).columns:
#             df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert non-numeric to NaN
#             converted_cols[col] = df[col].dtype.name  # Track conversion
#         changes["data_type_conversion"] = converted_cols
#
#         # 5. Standardize and Normalize Data using MinMaxScaler
#         scaler = MinMaxScaler()
#         df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
#         changes["scaling"] = "Applied MinMax Scaling on numerical columns"
#
#         # Save the processed file for download
#         processed_file_path = file_path.replace(".csv", "_processed.csv").replace(".xlsx", "_processed.xlsx")
#         if file_path.endswith(".csv"):
#             df.to_csv(processed_file_path, index=False)
#         else:
#             df.to_excel(processed_file_path, index=False)
#
#         # Delete the original file after processing
#         os.remove(file_path)
#
#         return df, changes, processed_file_path
#     except Exception as e:
#         return None, {"error": str(e)}, None
