import os
import pytest
from app import app, extract_table_from_pdf, allowed_file

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload_form(client):
    """Test that the upload form is displayed correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'PDF Table Extractor' in response.data
    assert b'Upload a PDF file containing tables' in response.data

def test_allowed_file():
    """Test the allowed_file function"""
    assert allowed_file('test.pdf') == True
    assert allowed_file('test.txt') == False
    assert allowed_file('test') == False

def test_upload_no_file(client):
    """Test uploading with no file"""
    response = client.post('/upload', data={})
    assert response.status_code == 302  # Redirect

def test_upload_invalid_file(client):
    """Test uploading an invalid file type"""
    data = {
        'file': (open(__file__, 'rb'), 'test.py')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b'Please upload a valid PDF file' in response.data

# Note: Testing with actual PDF files would require sample PDFs
# This would be a more comprehensive test but is omitted for simplicity 