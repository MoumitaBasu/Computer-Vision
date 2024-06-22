import cv2
import pytesseract
import tabula
import pandas as pd
import re
from datetime import datetime

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary_image

def ocr_receipt(image_path):
    processed_image = preprocess_image(image_path)
    # Set Tesseract configuration
    custom_config = r'--oem 3 --psm 6'

    ocr_text = pytesseract.image_to_string(processed_image, config=custom_config)
    return ocr_text

def extract_tables_from_pdf(pdf_path):
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    return [pd.DataFrame(table) for table in tables]

def extract_store_name(ocr_text):
    lines = ocr_text.split('\n')
    store_name = ''
    for line in lines:
        # Check if line is in uppercase and contains alphabets
        if line.strip() and line.strip().isupper() and any(char.isalpha() for char in line):
            store_name = line.strip()
            break
    return store_name

def extract_purchase_date(ocr_text):
    date_patterns = [
        re.compile(r'\b(\d{2}/\d{2}/\d{4})\b'),
        re.compile(r'\b(\d{2}-\d{2}-\d{4})\b'),
        re.compile(r'\b(\d{2}\.\d{2}\.\d{4})\b')
    ]
    lines = ocr_text.split('\n')
    for line in lines:
        for pattern in date_patterns:
            match = pattern.search(line)
            if match:
                # Normalize date format to YYYY-MM-DD
                try:
                    return datetime.strptime(match.group(1), '%m/%d/%Y').strftime('%Y-%m-%d')
                except ValueError:
                    pass
                try:
                    return datetime.strptime(match.group(1), '%m-%d-%Y').strftime('%Y-%m-%d')
                except ValueError:
                    pass
                try:
                    return datetime.strptime(match.group(1), '%m.%d.%Y').strftime('%Y-%m-%d')
                except ValueError:
                    pass
    return None


def normalize_price(price):
    currency_match = re.search(r'(\$|USD|EUR|€|£|GBP)', price)
    currency = currency_match.group(1) if currency_match else 'USD'
    price = re.sub(r'[^\d.]+', '', price)
    try:
        return float(price), currency
    except ValueError:
        return None, currency
    

def parse_ocr_text_to_dataframe(ocr_text):
    # Split the OCR text into lines with lower case
    lines = ocr_text.lower().split('\n')
    item_lines = []
    buffer_line = ''

    # Extract store name and purchase date
    store_name = extract_store_name(ocr_text)
    purchase_date = extract_purchase_date(ocr_text)

    # Define a regex pattern to identify lines with item, sku, and price, in any order. SKU is optional, can be defined as alphanumeric, atleast 1 character.
    pattern = re.compile(r'(?:(.*?)(?:\s+)(\d+\.\d+))')
    for line in lines:
        if pattern.match(line):
            #item_lines.append(line)
            if buffer_line:
                item_lines.append(buffer_line.strip())
                buffer_line = ''
            item_lines.append(line.strip())
        else:
            buffer_line += ' ' + line.strip()
    
    if buffer_line:
        item_lines.append(buffer_line.strip())

    # Common quantity patterns
    quantity_patterns = re.compile(r'\b(\d+)\s?(lb|oz|kg|g|ea|each|bag|doz|ct)\b')
    # SKU is something that is alphanumeric,must start with a number, atleast 1 character long.
    sku_pattern = re.compile(r'\b(\d{1,})\b')
    # Parsing item lines into structured data
    data = []
    for line in item_lines:
        match = pattern.match(line)
        if match:
            item = match.group(1).strip()
            #price = match.group(2).strip()
            price, currency = normalize_price(match.group(2).strip())  # Normalize the price and extract currency
            if price is None:
                continue  # Skip items with invalid prices
            quantity = 1  # Default quantity to 1
            unit = None  # Default unit to None
            sku = None
            # Check for quantity pattern in the item description
            quantity_match = quantity_patterns.search(item)
            if quantity_match:
                quantity = quantity_match.group(1).strip()
                unit = quantity_match.group(2).strip()
                # Remove the quantity part from the item description
                item = quantity_patterns.sub('', item).strip()
            if sku_pattern.search(item):
                sku = sku_pattern.search(item).group(1).strip()
                # Remove the sku part from the item description
                item = sku_pattern.sub('', item).strip()

            # Clean up the item description
            item = re.sub(r'\s+', ' ', item).strip()
            # Remove extra characters from the item description
            item = re.sub(r'[^a-zA-Z0-9\s]', '', item)
            # Skip words like 'total', 'subtotal', 'tax', etc.
            if item.lower() in ['total', 'subtotal', 'tax', 'cash', 'change', 'credit', 'debit', 'visa', 'mastercard', 'american express', 'discover']:
                continue
            
            data.append([item, quantity, unit, price, currency, sku])

    # Create a DataFrame from the parsed data
    df = pd.DataFrame(data, columns=['Item', 'Quantity', 'Unit', 'Price', 'Currency', 'SKU'])
    # Add a row for the total amount
    total_amount = df['Price'].astype(float).sum()
    # Add a row for the total amount
    df = pd.concat([df, pd.DataFrame([['Total', '', '', total_amount, 'USD', '']], columns=['Item', 'Quantity', 'Unit', 'Price', 'Currency', 'SKU'])], ignore_index=True)

    df['Store Name'] = store_name
    df['Purchase Date'] = purchase_date

    return df


