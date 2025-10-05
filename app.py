from flask import Flask, render_template, jsonify, request, send_file
import os
import subprocess
import pandas as pd
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates')

# Ensure directories exist
os.makedirs('maps', exist_ok=True)
os.makedirs('uploads', exist_ok=True)

# -------------------- FRONTEND ROUTES -------------------- #
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/why')
def why():
    return render_template('why.html')

@app.route('/nasa')
def nasa():
    return render_template('nasa.html')

@app.route('/tag')
def tag():
    return render_template('tag.html')

@app.route('/tracker')
def tracker():
    return render_template('tracker.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/habitat')
def habitat():
    return render_template('habitat.html')

@app.route('/types')
def types():
    return render_template('types.html')

@app.route('/migration')
def migration():
    return render_template('migration.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

# -------------------- API ROUTES -------------------- #
@app.route('/api/generate-synthetic-data', methods=['POST'])
def generate_synthetic_data():
    try:
        result = subprocess.run(
            ['python', 'sharkfromspace/ultim-gen-syn.py'],
            capture_output=True, text=True, cwd='.'
        )
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Synthetic data generated successfully',
                'filename': 'synthetic_ocean_data_ocean_only.csv'
            })
        else:
            return jsonify({'success': False, 'error': result.stderr}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate-heatmap', methods=['POST'])
def generate_heatmap():
    try:
        data = request.get_json()
        grid_res = data.get('grid_res', 0.25)
        prob_threshold = data.get('prob_threshold', 0.4)
        test_size = data.get('test_size', 0.2)
        n_est = data.get('n_est', 200)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"shark_heatmap_{timestamp}.html"

        result = subprocess.run([
            'python', 'sharkfromspace/ml-trainer.py',
            '--input', 'synthetic_ocean_data_ocean_only.csv',
            '--out', output_filename,
            '--grid_res', str(grid_res),
            '--prob_threshold', str(prob_threshold),
            '--test_size', str(test_size),
            '--n_est', str(n_est)
        ], capture_output=True, text=True, cwd='.')

        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Heatmap generated successfully',
                'filename': output_filename,
                'path': f'maps/{output_filename}'
            })
        else:
            return jsonify({'success': False, 'error': result.stderr}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/heatmap/<filename>')
def serve_heatmap(filename):
    filepath = os.path.join('maps', secure_filename(filename))
    if os.path.exists(filepath):
        return send_file(filepath)
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/list-heatmaps')
def list_heatmaps():
    try:
        files = [f for f in os.listdir('maps') if f.endswith('.html')]
        files.sort(key=lambda x: os.path.getmtime(os.path.join('maps', x)), reverse=True)
        return jsonify({'success': True, 'heatmaps': files})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/data-info')
def data_info():
    try:
        csv_file = 'synthetic_ocean_data_ocean_only.csv'
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            return jsonify({
                'success': True,
                'rows': len(df),
                'columns': list(df.columns),
                'bounds': {
                    'lat_min': float(df['lat'].min()),
                    'lat_max': float(df['lat'].max()),
                    'lon_min': float(df['lon'].min()),
                    'lon_max': float(df['lon'].max())
                },
                'stats': {
                    'sst_mean': float(df['SST_C'].mean()),
                    'chlor_mean': float(df['chlor_a_mg_m3'].mean()),
                    'depth_mean': float(df['ocean_depth_m'].mean())
                }
            })
        else:
            return jsonify({'success': False, 'error': 'No data file found. Generate synthetic data first.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# -------------------- MAIN -------------------- #
if __name__ == '__main__':
    print("🚀 Server running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
