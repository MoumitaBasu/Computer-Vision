import streamlit as st
import requests
import pandas as pd

st.title("Receipt OCR Application")

uploaded_file = st.file_uploader("Upload a receipt image or PDF", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    files = {'file': uploaded_file.getvalue()}
    response = requests.post("http://localhost:5005/upload", files=files)
    
    if response.status_code == 200:
        result = response.json()
        if 'ocr_text' in result:
            st.subheader("Parsed OCR DataFrame")
            ocr_df = pd.read_json(result['ocr_df'])
            st.dataframe(ocr_df)
        if 'tables' in result:
            st.subheader("Extracted Tables from PDF")
            for table_json in result['tables']:
                table_df = pd.read_json(table_json)
                st.dataframe(table_df)
    else:
        st.error("Failed to process the file.")
