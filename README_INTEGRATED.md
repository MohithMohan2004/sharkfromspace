# 🦈 Sharks from Space - Integrated Frontend & Backend

A complete web application that combines a beautiful frontend with machine learning backend to track shark probabilities using NASA satellite data.

## 🌟 Features

- **Interactive Frontend**: Beautiful HTML pages with modern UI design
- **Machine Learning Backend**: Python ML scripts for shark probability prediction
- **Real-time API**: Flask server providing REST API endpoints
- **Interactive Maps**: Folium-based heatmaps showing shark probability hotspots
- **Synthetic Data Generation**: Generate ocean data for testing and demonstration

## 🚀 Quick Start

### Option 1: Easy Start (Recommended)
```bash
python start_server.py
```
This will:
- Check and install dependencies automatically
- Start the Flask server
- Open your browser to http://localhost:5000

### Option 2: Manual Start
```bash
# Install dependencies
pip install -r sharkfromspace/requirements.txt

# Start the server
python app.py
```

## 📁 Project Structure

```
├── app.py                    # Flask server (serves frontend + API)
├── start_server.py          # Easy startup script
├── tracker.html             # Interactive shark tracker page
├── index.html               # Home page
├── about.html               # About page
├── nasa.html                # NASA data page
├── tag.html                 # Next-gen tag page
├── why.html                 # Why sharks page
├── contact.html             # Contact page
├── habitat.html             # Shark habitat page
├── types.html               # Types of sharks page
├── migration.html           # Migration cycle page
├── aboutus.html             # About us page
└── sharkfromspace/          # Backend ML scripts
    ├── ml-trainer.py        # ML model training & heatmap generation
    ├── ultim-gen-syn.py     # Synthetic data generation
    ├── requirements.txt     # Python dependencies
    └── README.md            # Backend documentation
```

## 🌐 Web Interface

Once the server is running, visit:

- **Home**: http://localhost:5000/
- **Shark Tracker**: http://localhost:5000/tracker.html (Interactive ML interface)
- **About**: http://localhost:5000/about
- **NASA Data**: http://localhost:5000/nasa
- **Next-Gen Tag**: http://localhost:5000/tag
- **Why Sharks**: http://localhost:5000/why
- **Contact**: http://localhost:5000/contact

## 🔧 API Endpoints

The Flask server provides these API endpoints:

- `POST /api/generate-synthetic-data` - Generate synthetic ocean data
- `POST /api/generate-heatmap` - Generate shark probability heatmap
- `GET /api/list-heatmaps` - List available heatmap files
- `GET /api/data-info` - Get current dataset information
- `GET /api/heatmap/<filename>` - Serve generated heatmap files

## 🦈 How to Use the Shark Tracker

1. **Generate Synthetic Data**: Click "Generate Synthetic Data" to create ocean data
2. **Configure Parameters**: Adjust grid resolution, probability threshold, etc.
3. **Generate Heatmap**: Click "Generate Heatmap" to create the ML model and map
4. **View Results**: Click "View Map" on any generated heatmap to see interactive results
5. **Load Data Info**: Click "Load Data Info" to see statistics about your dataset

## 🛠️ Technical Details

### Frontend
- Pure HTML/CSS/JavaScript
- Responsive design with modern UI
- Real-time API integration
- Interactive controls for ML parameters

### Backend
- Flask web server
- Machine Learning with scikit-learn
- Interactive maps with Folium
- Synthetic data generation
- RESTful API design

### Dependencies
- Flask (web server)
- pandas, numpy (data processing)
- scikit-learn (machine learning)
- folium (interactive maps)
- cartopy, shapely (geospatial processing)

## 🎯 Use Cases

- **Research**: Study shark behavior and ocean ecology
- **Conservation**: Identify shark hotspots for protection
- **Education**: Learn about marine biology and ML
- **Demonstration**: Showcase NASA data applications

## 👥 Team

**The Commit Crew** 🔥

## 📄 License

This project is part of the NASA Space Apps Challenge.

---

**Ready to track sharks from space? Run `python start_server.py` and start exploring!** 🚀
