from flask import Flask, render_template, request, jsonify, send_file
import os
import subprocess
import json
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure necessary directories exist
os.makedirs('maps', exist_ok=True)
os.makedirs('uploads', exist_ok=True)

@app.route('/')
def index():
    """Serve the main index page"""
    return send_file('index.html')

@app.route('/about')
def about():
    """Serve the about page"""
    return send_file('about.html')

@app.route('/nasa')
def nasa():
    """Serve the NASA data page"""
    return send_file('nasa.html')

@app.route('/tag')
def tag():
    """Serve the tag page"""
    return send_file('tag.html')

@app.route('/why')
def why():
    """Serve the why sharks page"""
    return send_file('why.html')

@app.route('/contact')
def contact():
    """Serve the contact page"""
    return send_file('contact.html')

@app.route('/habitat')
def habitat():
    """Serve the habitat page"""
    return send_file('habitat.html')

@app.route('/types')
def types():
    """Serve the types page"""
    return send_file('types.html')

@app.route('/migration')
def migration():
    """Serve the migration page"""
    return send_file('migration.html')

@app.route('/aboutus')
def aboutus():
    """Serve the about us page"""
    return send_file('aboutus.html')

@app.route('/tracker')
def tracker():
    """Serve the tracker page"""
    return send_file('tracker.html')

@app.route('/tracker.html')
def tracker_html():
    """Serve the tracker page (HTML suffix)"""
    return send_file('tracker.html')

@app.route('/api/generate-synthetic-data', methods=['POST'])
def generate_synthetic_data():
    """Generate synthetic ocean data"""
    try:
        # Run the synthetic data generator
        result = subprocess.run([
            'python', 'sharkfromspace/ultim-gen-syn.py'
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Synthetic data generated successfully',
                'filename': 'synthetic_ocean_data_ocean_only.csv'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Error generating data: {result.stderr}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Exception: {str(e)}'
        }), 500

@app.route('/api/generate-heatmap', methods=['POST'])
def generate_heatmap():
    """Generate shark probability heatmap"""
    try:
        data = request.get_json()
        
        # Default parameters
        grid_res = data.get('grid_res', 0.25)
        prob_threshold = data.get('prob_threshold', 0.4)
        test_size = data.get('test_size', 0.2)
        n_est = data.get('n_est', 200)
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"shark_heatmap_{timestamp}.html"
        
        # Run the ML trainer
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
            return jsonify({
                'success': False,
                'error': f'Error generating heatmap: {result.stderr}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Exception: {str(e)}'
        }), 500

@app.route('/api/heatmap/<filename>')
def serve_heatmap(filename):
    """Serve generated heatmap files"""
    try:
        filepath = os.path.join('maps', secure_filename(filename))
        if os.path.exists(filepath):
            return send_file(filepath)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/list-heatmaps')
def list_heatmaps():
    """List all available heatmap files"""
    try:
        maps_dir = 'maps'
        if not os.path.exists(maps_dir):
            return jsonify({'heatmaps': []})
        
        files = [f for f in os.listdir(maps_dir) if f.endswith('.html')]
        files.sort(key=lambda x: os.path.getmtime(os.path.join(maps_dir, x)), reverse=True)
        
        return jsonify({
            'success': True,
            'heatmaps': files
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/data-info')
def data_info():
    """Get information about the current dataset"""
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
                    'sst_std': float(df['SST_C'].std()),
                    'chlor_mean': float(df['chlor_a_mg_m3'].mean()),
                    'depth_mean': float(df['ocean_depth_m'].mean())
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No data file found. Generate synthetic data first.'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    try:
        print("🦈 Starting Sharks from Space Flask Server...")
        print("📊 Backend API endpoints available at:")
        print("   - POST /api/generate-synthetic-data")
        print("   - POST /api/generate-heatmap")
        print("   - GET /api/list-heatmaps")
        print("   - GET /api/data-info")
        print("   - GET /api/heatmap/<filename>")
        print("\n🌐 Frontend pages available at:")
        print("   - / (home)")
        print("   - /about, /nasa, /tag, /why, /contact")
        print("   - /habitat, /types, /migration, /aboutus")
        print("   - /tracker (shark tracking interface)")
        print("\n🚀 Server starting on http://localhost:5000")
    except UnicodeEncodeError:
        # Fallback for Windows console encoding issues
        print("Starting Sharks from Space Flask Server...")
        print("Backend API endpoints available at:")
        print("   - POST /api/generate-synthetic-data")
        print("   - POST /api/generate-heatmap")
        print("   - GET /api/list-heatmaps")
        print("   - GET /api/data-info")
        print("   - GET /api/heatmap/<filename>")
        print("\nFrontend pages available at:")
        print("   - / (home)")
        print("   - /about, /nasa, /tag, /why, /contact")
        print("   - /habitat, /types, /migration, /aboutus")
        print("   - /tracker (shark tracking interface)")
        print("\nServer starting on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
