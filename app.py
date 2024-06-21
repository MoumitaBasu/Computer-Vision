from flask import Flask, request, jsonify
from ocr import ocr_receipt, extract_tables_from_pdf, parse_ocr_text_to_dataframe
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)
    
    if file.filename.lower().endswith('.pdf'):
        tables = extract_tables_from_pdf(file_path)
        tables_json = [table.to_json() for table in tables]
        return jsonify({'tables': tables_json}), 200
    else:
        ocr_text = ocr_receipt(file_path)
        ocr_df = parse_ocr_text_to_dataframe(ocr_text)
        return jsonify({'ocr_text': ocr_text, 'ocr_df': ocr_df.to_json()}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
