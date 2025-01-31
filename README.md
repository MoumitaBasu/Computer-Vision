# OCRApp

This project demonstrates Optical Character Recognition (OCR) capabilities using Flask for backend processing and Streamlit for frontend visualization.

## Project Structure

```bash
ocr_project/
│
├── app.py                 # Flask backend application
├── ocr.py                 # OCR functionality module
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (optional)
├── sample_images/         # Directory containing sample images and PDFs
└── frontend/              # Directory containing Streamlit frontend
    └── streamlit_app.py   # Streamlit web application for frontend
```

## Components
### Backend (Flask - app.py)
The backend of the project utilizes Flask to provide a RESTful API for OCR operations. It includes endpoints to upload images/PDFs, perform OCR, extract tables from PDFs, and parse OCR text into structured data.

### OCR Functionality (ocr.py)
This module contains functions for OCR processing:

- `ocr_receipt(file_path)`: Performs OCR on receipt images.
- `extract_tables_from_pdf(file_path)`: Extracts tables from PDF files.
- `parse_ocr_text_to_dataframe(ocr_text)`: Parses OCR text into a structured DataFrame.

### Frontend (Streamlit - frontend/streamlit_app.py)
The frontend is implemented using Streamlit, providing a user-friendly interface to interact with the OCR functionalities. Users can upload images or PDFs, visualize OCR results, and explore extracted tables.

## Getting Started
1. Clone the repository
```bash
git clone https://github.com/your-username/ocrapp.git
cd ocrapp
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```
3. Install Tesseract
- Linux
```bash
sudo apt-get install tesseract-ocr
```
- MacOS
```bash
brew install tesseract
```
4. Run the backend (Flask):

```bash
python app.py
```
The backend will start running on http://localhost:5000.

5. Run the frontend (Streamlit)
```bash
streamlit run frontend/streamlit_app.py
```

## Sample Images and PDFs
The sample_images/ directory contains example files that can be used to test the OCR functionalities. These include:

- 1.jpg
- 2.jpg
- 3.pdf
