import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit.components.v1 import html
import tempfile
import os

# Set the correct password
PASSWORD = "Camelot2025!"

# Initialize authentication state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "password_entered" not in st.session_state:
    st.session_state["password_entered"] = False

# Prompt for password if not authenticated
if not st.session_state["authenticated"]:
    with st.form("login_form"):
        password = st.text_input("Enter password:", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if password == PASSWORD:
                st.session_state["authenticated"] = True
                st.success("Password correct! Access granted.")
            else:
                st.error("Incorrect password. Please try again.")

# Main app content after successful authentication
if st.session_state["authenticated"]:
    st.title("📊 Data Profiler - CSV & Excel Files")

    # File uploader
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

    # Process the uploaded file
    if uploaded_file is not None:
        try:
            # Check the file extension to determine whether it's a CSV or Excel file
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file type. Please upload a CSV or Excel file.")
                df = None

            # If the dataframe is loaded, proceed with profiling
            if df is not None:
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
