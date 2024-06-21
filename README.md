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

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
