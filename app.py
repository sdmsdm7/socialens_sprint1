from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import pandas as pd
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
    breadcrumbs = [("Home", "/")]
    return render_template('index.html', breadcrumbs=breadcrumbs)

@app.route('/data-upload', methods=['GET', 'POST'])
def data_upload():
    breadcrumbs = [("Home", "/"), ("Data Upload", "/data-upload")]
    if request.method == 'POST':
        file = request.files['dataFile']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(f'😄 File {filename} uploaded successfully! Good on you!', 'success')
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    files_info = [{
        'name': file,
        'size': f"{os.stat(os.path.join(app.config['UPLOAD_FOLDER'], file)).st_size / 1024:.2f} KB",
        'upload_time': datetime.fromtimestamp(os.stat(os.path.join(app.config['UPLOAD_FOLDER'], file)).st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    } for file in files]
    return render_template('data_upload.html', breadcrumbs=breadcrumbs, files=files_info)

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

@app.route('/explore-data')
def explore_data():
    breadcrumbs = [("Home", "/"), ("Explore Data", "/explore-data")]
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
    if not files:
        flash("No uploaded files found. Please upload a file first.", 'danger')
        return render_template('explore_data.html', files=files, breadcrumbs=breadcrumbs, error_message="No uploaded files found.")
    return render_template('explore_data.html', files=files, breadcrumbs=breadcrumbs)

@app.route('/analyze-data', methods=['POST'])
def analyze_data():
    selected_file = request.form.get('selectedFile')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], selected_file)
    if not os.path.exists(file_path):
        flash("File does not exist.", 'danger')
        return redirect(url_for('explore_data'))

    breadcrumbs = [("Home", "/"), ("Explore Data", "/explore-data"), ("Analyze Data", "/analyze-data")]

    try:
        # Check the file extension and read accordingly
        if selected_file.endswith(('.xlsx', '.xls')):
            # Read all sheets; each sheet's DataFrame is stored in a dictionary
            xls = pd.ExcelFile(file_path)
            sheets = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
        elif selected_file.endswith('.csv'):
            df = pd.read_csv(file_path)
            sheets = {'CSV': df}
        else:
            flash("Unsupported file format.", 'danger')
            return redirect(url_for('explore_data'))

        # Convert each DataFrame to HTML table
        tables_html = {sheet_name: df.to_html(classes='table table-striped', index=False) for sheet_name, df in sheets.items()}
    except Exception as e:
        flash(f"Failed to read the file: {str(e)}", 'danger')
        return redirect(url_for('explore_data'))

    return render_template('analysis_results.html', tables_html=tables_html, filename=selected_file, sheet_names=list(tables_html.keys()), breadcrumbs=breadcrumbs)

@app.route('/descriptive-statistics')
def descriptive_statistics():
    breadcrumbs = [("Home", "/"), ("Descriptive Statistics", "/descriptive-statistics")]
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
    if not files:
        flash("No uploaded files found. Please upload a file first.", 'danger')
        return render_template('descriptive_statistics.html', files=files, breadcrumbs=breadcrumbs, error_message="No uploaded files found.")
    return render_template('descriptive_statistics.html', files=files, breadcrumbs=breadcrumbs)

@app.route('/descriptive-statistics-viewer')
def descriptive_statistics_viewer():
    breadcrumbs = [("Home", "/"), ("Descriptive Statistics Viewer", "/descriptive-statistics-viewer")]
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith(('.xlsx', '.xls', '.csv'))]  # Filter to include only relevant file types
    return render_template('descriptive_statistics_viewer.html', files=files, breadcrumbs=breadcrumbs)

@app.route('/analyze/<filename>')
def analyze(filename):
    breadcrumbs = [("Home", "/"), ("Descriptive Statistics", "/descriptive-statistics"), ("View Statistics", "/")]
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        flash("File does not exist.", 'danger')
        return redirect(url_for('descriptive_statistics'))
    results = analyze_file(file_path)
    return render_template('view_statistics.html', filename=filename, results=results, breadcrumbs=breadcrumbs)

@app.route('/network-visualiser')
def network_visualiser():
    breadcrumbs = [("Home", "/"), ("Network Visualiser", "/network-visualiser")]
    return render_template('network_visualiser.html', breadcrumbs=breadcrumbs)

@app.route('/report-generator')
def report_generator():
    breadcrumbs = [("Home", "/"), ("Report Generator", "/report-generator")]
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        stats = os.stat(filepath)
        files.append({
            'name': filename,
        })
    return render_template('report_generator.html', breadcrumbs=breadcrumbs)

@app.route('/login')
def user_profile():
    breadcrumbs = [("Home", "/"), ("Login", "/login")]
    return render_template('login.html', breadcrumbs=breadcrumbs)

@app.route('/settings')
def settings():
    breadcrumbs = [("Home", "/"), ("Settings", "/settings")]
    return render_template('settings.html', breadcrumbs=breadcrumbs)

@app.route('/support')
def support():
    breadcrumbs = [("Home", "/"), ("Support", "/support")]
    return render_template('support.html', breadcrumbs=breadcrumbs)

@app.route('/feedback')
def feedback():
    breadcrumbs = [("Home", "/"), ("Feedback", "/feedback")]
    return render_template('feedback.html', breadcrumbs=breadcrumbs)

if __name__ == '__main__':
    app.run(debug=True)
