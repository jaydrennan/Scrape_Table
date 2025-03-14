# PDF Table Extractor

A simple web application that allows users to upload a PDF file containing tables and extracts the first table found, displaying it as an HTML table.

## Features

- Upload PDF files through a web interface
- Extract tables from PDF files using pdfplumber
- Display extracted tables as formatted HTML
- Modern UI with Tailwind CSS and Alpine.js

## Requirements

- Python 3.8+
- Flask
- pdfplumber
- pandas
- Werkzeug

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/pdf-table-extractor.git
   cd pdf-table-extractor
   ```

2. Install dependencies using uv:
   ```
   uv pip install -r requirements.txt
   ```

## Usage

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

3. Upload a PDF file containing tables using the web form.

4. The application will extract the first table found in the PDF and display it as an HTML table.

## Testing

Run tests using pytest:
```
pytest
```

## Limitations

- Currently only extracts the first table found in the PDF
- May not work with all PDF formats or complex table structures
- No OCR capability for scanned documents

## Future Improvements

- Add support for extracting multiple tables
- Implement OCR for scanned documents
- Add options for exporting tables to CSV, Excel, etc.
- Improve table detection and extraction accuracy
