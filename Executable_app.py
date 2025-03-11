import streamlit as st

# Set the correct password
PASSWORD = "your_secure_password"

# Prompt for password
password = st.text_input("Enter password:", type="password")

# Check if the password is correct
if password == Camelot2025!:
    # Your app's main content here
    st.write("Welcome to the app!")
    
    # Your app code goes here (e.g., data profiling, etc.)
    # Example:
    # df = pd.read_csv('file.csv')
    # st.write(df)
else:
    st.write("Incorrect password. Please try again.")


import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit.components.v1 import html
import tempfile
import os

# Title of the app
st.title("📊 Data Profiler - CSV & Excel Files")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

# Process the uploaded file
if uploaded_file is not None:
    try:
        # Check the file extension to determine whether it's a CSV or Excel file
        if uploaded_file.name.endswith(".csv"):
            # Load CSV file
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            # Load Excel file
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a CSV or Excel file.")
            df = None

        # If the dataframe is loaded, proceed with profiling
        if df is not None:
            # Display the dataframe preview
            st.write("### Preview of Uploaded Data", df.head())

            # Generate the profiling report
            profile = ProfileReport(df, title="Data Profiling Report", minimal=True)

            # Use a temporary file to save the report
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
                profile.to_file(tmp_file.name)
                tmp_file_path = tmp_file.name

            # Display the report in the app
            with open(tmp_file_path, "r", encoding='utf-8') as report_file:
                report_html = report_file.read()
                html(report_html, height=800, scrolling=True)

            # Provide a download button
            with open(tmp_file_path, "rb") as f:
                st.download_button("📥 Download Report", f, file_name="Data_Profile_Report.html", mime="text/html")
            
            # Clean up the temporary file
            os.remove(tmp_file_path)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a CSV or Excel file to generate the report.")
