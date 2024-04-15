from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
# referencing an external py file
from descriptive_statistics import analyze_file  

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required to use flash messages

# Set the path for the uploads folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB upload limit

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data-upload', methods=['GET', 'POST'])
def data_upload():
    if request.method == 'POST':
        file = request.files['dataFile']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(f'😄 File {filename} uploaded successfully! Good on you!', 'success')
        else:
            flash('😵 File upload failed. I can only ingest .csv, .xlsx, .xls files, sorry!', 'danger')
        return redirect(url_for('data_upload'))
    return render_template('data_upload.html')

@app.route('/datasets')
def datasets():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        stats = os.stat(filepath)
        files.append({
            'name': filename,
            'size': f"{stats.st_size / 1024:.2f} KB",
            'upload_time': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        })
    return render_template('datasets.html', files=files)

@app.route('/descriptive-statistics')
def descriptive_statistics():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
    return render_template('descriptive_statistics.html', files=files)

@app.route('/analyze/<filename>')
def analyze(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        flash("File does not exist.", 'danger')
        return redirect(url_for('descriptive_statistics'))
    results = analyze_file(file_path)
    return render_template('view_statistics.html', filename=filename, results=results)

@app.route('/network-visualiser')
def network_visualiser():
    return render_template('network_visualiser.html')

@app.route('/report-generator')
def report_generator():
    return render_template('report_generator.html')

if __name__ == '__main__':
    app.run(debug=True)
