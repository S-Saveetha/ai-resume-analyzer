import streamlit as st

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])

if uploaded_file is not None:
    st.write("File uploaded successfully!")