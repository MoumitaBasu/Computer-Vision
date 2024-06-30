import streamlit as st
import requests
import pandas as pd
from PIL import Image
import io

# Function to upload files and interact with backend
def upload_files_to_backend(files):
    uploaded_files_data = []
    for file in files:
        files = {'file': file.getvalue()}
        response = requests.post("http://localhost:5005/upload", files=files)
        if response.status_code == 200:
            result = response.json()
            if 'ocr_text' in result and 'ocr_df' in result:
                ocr_text = result['ocr_text']
                ocr_df = pd.read_json(result['ocr_df'])
                uploaded_files_data.append({'ocr_text': ocr_text, 'ocr_df': ocr_df, 'file_type': file.type, 'file_name': file.name})
    return uploaded_files_data

# Function to display image preview
def display_image_preview(file):
    img = Image.open(io.BytesIO(file.read()))
    st.image(img, caption=file.name, use_column_width=True)

# Page 1: Upload files and show basic information
def page1():
    st.markdown(
        """
        <style>
        .main {
            background-color: #e6e6fa;
            padding: 20px;
            border-radius: 10px;
        }
        .header {
            font-size: 36px;
            text-align: center;
            margin-top: -50px;
            margin-bottom: 50px;
        }
        .upload-section, .convert-section {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
        }
        .convert-button {
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='main'>", unsafe_allow_html=True)
    st.markdown("<div class='header'>Upload Receipt Images or PDFs</div>", unsafe_allow_html=True)

    uploaded_files = st.file_uploader("Upload files", type=["jpeg", "jpg", "png", "pdf"], accept_multiple_files=True)

    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        st.success("Files uploaded successfully!")

        # Display image preview for uploaded images
        for file in uploaded_files:
            if file.type.startswith('image'):
                display_image_preview(file)

        st.markdown("<div class='convert-section'>", unsafe_allow_html=True)
        if st.button('Convert Files'):
            st.session_state.uploaded_files_data = upload_files_to_backend(uploaded_files)
            st.session_state.page = 'Page 2'
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Page 2: Display converted data for each file and allow download
def page2():
    st.markdown(
        """
        <style>
        .main {
            background-color: #e6e6fa;
            padding: 20px;
            border-radius: 10px;
        }
        .header {
            font-size: 36px;
            text-align: center;
            margin-top: -50px;
            margin-bottom: 50px;
        }
        .download-section {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
        }
        .download-button {
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='main'>", unsafe_allow_html=True)
    st.markdown("<div class='header'>Converted Data</div>", unsafe_allow_html=True)

    if 'uploaded_files_data' in st.session_state:
        for idx, file_data in enumerate(st.session_state.uploaded_files_data):
            st.markdown(f"<h3>File {idx + 1}</h3>", unsafe_allow_html=True)
            ocr_text = file_data['ocr_text']
            ocr_df = file_data['ocr_df']

            st.subheader("Parsed OCR DataFrame")
            st.dataframe(ocr_df)

            st.markdown("<div class='download-section'>", unsafe_allow_html=True)
            file_format = st.selectbox(
                f"Select file format for File {idx + 1}",
                (".xlsx", ".pdf")
            )

            if st.button(f'Download table for File {idx + 1}'):
                if file_format == ".xlsx":
                    @st.cache_data
                    def convert_df_to_excel(df):
                        from io import BytesIO
                        with BytesIO() as output:
                            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                                df.to_excel(writer, index=False, sheet_name='Sheet1')
                            return output.getvalue()

                    excel = convert_df_to_excel(ocr_df)

                    st.download_button(
                        label=f"Download data as Excel for File {idx + 1}",
                        data=excel,
                        file_name=f'converted_data_file_{idx + 1}.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    )

                elif file_format == ".pdf":
                    @st.cache_data
                    def convert_df_to_pdf(df):
                        from io import BytesIO
                        from reportlab.lib.pagesizes import letter
                        from reportlab.pdfgen import canvas

                        output = BytesIO()
                        c = canvas.Canvas(output, pagesize=letter)
                        width, height = letter

                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(30, height - 40, f"Converted Data for File {idx + 1}")

                        c.setFont("Helvetica", 10)
                        x_offset = 30
                        y_offset = height - 60
                        for i, col in enumerate(df.columns):
                            c.drawString(x_offset + i * 150, y_offset, col)

                        for row in df.itertuples():
                            y_offset -= 20
                            for i, val in enumerate(row[1:]):
                                c.drawString(x_offset + i * 150, y_offset, str(val))

                        c.save()
                        output.seek(0)
                        return output

                    pdf = convert_df_to_pdf(ocr_df)

                    st.download_button(
                        label=f"Download data as PDF for File {idx + 1}",
                        data=pdf,
                        file_name=f'converted_data_file_{idx + 1}.pdf',
                        mime='application/pdf',
                    )

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Initialize Streamlit app
st.set_page_config(layout="centered")

# Initialize session state for navigation and uploaded files
if 'page' not in st.session_state:
    st.session_state.page = 'Page 1'
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = None

# Function to switch pages
def switch_page(page_name):
    st.session_state.page = page_name

# Page selection based on session state
if st.session_state.page == 'Page 1':
    page1()
elif st.session_state.page == 'Page 2':
    page2()