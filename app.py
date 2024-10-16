import os
from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

# Ensure the uploaded_files directory exists
os.makedirs('uploaded_files', exist_ok=True)

# SQLite database setup
DATABASE_URL = 'sqlite:///data.db'
engine = create_engine(DATABASE_URL)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for uploading the CSV file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and file.filename.endswith('.csv'):
        file_path = os.path.join('uploaded_files', file.filename)
        file.save(file_path)

        # Read the CSV file
        df = pd.read_csv(file_path)

        # Store the data in SQLite database
        df.to_sql('data_table', con=engine, if_exists='replace', index=False)

        return "CSV file uploaded and data stored in the database!"

    return "Invalid file type. Please upload a CSV file."

if __name__ == '__main__':
    app.run(debug=True)
