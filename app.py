import os
import pandas as pd
import pdfplumber
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_tables_from_pdf(pdf_path):
    """Extract all tables from a PDF file using pdfplumber"""
    try:
        all_tables = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                tables = page.extract_tables()
                if tables:
                    for table_num, table in enumerate(tables, 1):
                        if table and any(any(cell for cell in row) for row in table):  # Check if table has content
                            all_tables.append({
                                'page': page_num,
                                'table_number': table_num,
                                'data': table
                            })
        return all_tables
    except Exception as e:
        print(f"Error extracting tables: {e}")
        return None

@app.route('/', methods=['GET'])
def upload_form():
    """Display the upload form"""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and table extraction"""
    # Check if a file was uploaded
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    # Check if the user selected a file
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('upload_form'))
    
    # Check if the file is a PDF
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract tables from the PDF
        tables = extract_tables_from_pdf(filepath)
        
        if not tables:
            return render_template('result.html', table_html="<p>No tables found in the PDF.</p>")
        
        # Convert all tables to HTML
        table_html = ""
        for table_info in tables:
            # Convert the table to a pandas DataFrame
            df = pd.DataFrame(table_info['data'][1:], columns=table_info['data'][0])
            
            # Add a header for each table showing its location
            table_html += f"<h3 class='text-lg font-semibold mt-6 mb-2'>Table {table_info['table_number']} from Page {table_info['page']}</h3>"
            
            # Convert DataFrame to HTML table with styling
            table_html += df.to_html(classes='table table-striped', index=False)
        
        # Clean up the uploaded file
        os.remove(filepath)
        
        return render_template('result.html', table_html=table_html)
    else:
        return render_template('result.html', table_html="<p>Please upload a valid PDF file.</p>")

if __name__ == '__main__':
    # Run the app on port 8000
    app.run(debug=True, host='0.0.0.0', port=8000) 