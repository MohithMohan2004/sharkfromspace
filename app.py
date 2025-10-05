<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shark Tracker - Sharks from Space</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
<style>
/* Same styles as other pages for consistency */
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; height: 100%; overflow-x: hidden; }
body { font-family: 'Poppins', sans-serif; color: #fff; min-height: 100vh; background: url('https://imgsonica.s3.amazonaws.com/wp-content/uploads/2025/05/77355.jpg') no-repeat center center fixed; background-size: cover; position: relative; padding-top:70px; }
body::before { content: ""; position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.4); z-index:-1; }

/* Transparent scrollbar */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.4); }

/* Navigation bar */
nav { position: fixed; top:0; left:0; width:100%; background: transparent; display:flex; justify-content:flex-end; align-items:center; padding:1rem 2rem; z-index:100; }
nav a { color: #00eaff; text-decoration: none; font-weight: 600; margin-left: 1.5rem; transition: color 0.3s ease; }
nav a:hover { color: #fff; text-decoration: underline; }

/* Hamburger menu button */
#menu-toggle { display:flex; align-items:center; gap:10px; background:none; border:none; cursor:pointer; z-index:101; margin-right:auto; }
#menu-toggle .hamburger { display:flex; flex-direction:column; justify-content:space-between; width:25px; height:20px; }
#menu-toggle .hamburger span { display:block; height:3px; width:100%; background:#00eaff; border-radius:2px; transition: all 0.3s ease; }
#menu-toggle.active .hamburger span:nth-child(1) { transform: rotate(45deg) translate(5px,5px); }
#menu-toggle.active .hamburger span:nth-child(2) { opacity: 0; }
#menu-toggle.active .hamburger span:nth-child(3) { transform: rotate(-45deg) translate(6px,-6px); }
#menu-toggle .menu-text { font-weight:600; color:#00eaff; font-size:1rem; }

/* Sidebar menu content */
.sidebar-menu {
    position: fixed;
    top: 0; left: -250px;
    width: 220px;
    height: 100%;
    background: rgba(0,50,100,0.6);
    backdrop-filter: blur(10px);
    padding: 3rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    border-radius: 0 20px 20px 0;
    transition: left 0.3s ease;
    z-index: 99;
}
.sidebar-menu.show { left: 0; }
.sidebar-menu a {
    padding: 0.8rem 1rem;
    text-align: center;
    border-radius: 15px;
    color: #fff;
    font-weight: 600;
    background: linear-gradient(135deg, #0072ff, #00c6ff);
    text-decoration: none;
    transition: all 0.3s ease;
    box-shadow: 0 5px 10px rgba(0,0,0,0.3);
}
.sidebar-menu a:hover { transform: translateY(-3px); background: linear-gradient(135deg, #00c6ff, #0072ff); box-shadow: 0 8px 15px rgba(0,0,0,0.5); }

/* Main content */
.main-content { flex:1; padding:6rem 2rem 3rem 2rem; z-index:1; position:relative; max-width:1200px; margin:auto; }

/* Control panel */
.control-panel { 
    background: rgba(0,0,0,0.6); 
    backdrop-filter: blur(10px); 
    padding:2rem; 
    border-radius:20px; 
    margin-bottom:2rem; 
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
}

.control-group { margin-bottom: 1rem; }
.control-group label { display: block; margin-bottom: 0.5rem; color: #00eaff; font-weight: 600; }
.control-group input, .control-group select { 
    width: 100%; 
    padding: 0.5rem; 
    border: 1px solid #00eaff; 
    border-radius: 8px; 
    background: rgba(255,255,255,0.1); 
    color: #fff; 
    font-size: 1rem;
}
.control-group input::placeholder { color: rgba(255,255,255,0.6); }

/* Buttons */
.btn { 
    padding: 0.8rem 1.5rem; 
    border: none; 
    border-radius: 10px; 
    font-weight: 600; 
    cursor: pointer; 
    transition: all 0.3s ease; 
    font-size: 1rem;
    margin: 0.5rem;
}
.btn-primary { 
    background: linear-gradient(135deg, #0072ff, #00c6ff); 
    color: white; 
    box-shadow: 0 5px 10px rgba(0,0,0,0.3);
}
.btn-primary:hover { 
    transform: translateY(-2px); 
    box-shadow: 0 8px 15px rgba(0,0,0,0.5); 
}
.btn-secondary { 
    background: linear-gradient(135deg, #6c757d, #495057); 
    color: white; 
    box-shadow: 0 5px 10px rgba(0,0,0,0.3);
}
.btn-secondary:hover { 
    transform: translateY(-2px); 
    box-shadow: 0 8px 15px rgba(0,0,0,0.5); 
}

/* Status and loading */
.status { 
    padding: 1rem; 
    border-radius: 10px; 
    margin: 1rem 0; 
    font-weight: 600;
}
.status.success { background: rgba(40, 167, 69, 0.3); border: 1px solid #28a745; color: #d4edda; }
.status.error { background: rgba(220, 53, 69, 0.3); border: 1px solid #dc3545; color: #f8d7da; }
.status.info { background: rgba(23, 162, 184, 0.3); border: 1px solid #17a2b8; color: #d1ecf1; }
.status.loading { background: rgba(255, 193, 7, 0.3); border: 1px solid #ffc107; color: #fff3cd; }

.loading-spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255,255,255,.3);
    border-radius: 50%;
    border-top-color: #00eaff;
    animation: spin 1s ease-in-out infinite;
    margin-right: 10px;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Map container */
.map-container { 
    background: rgba(0,0,0,0.6); 
    backdrop-filter: blur(10px); 
    padding:2rem; 
    border-radius:20px; 
    margin-bottom:2rem; 
    min-height: 500px;
}

.map-container h2 { color: #00eaff; margin-bottom: 1rem; }

/* Heatmap list */
.heatmap-list { 
    background: rgba(0,0,0,0.6); 
    backdrop-filter: blur(10px); 
    padding:2rem; 
    border-radius:20px; 
    margin-bottom:2rem; 
}

.heatmap-item { 
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
    padding: 1rem; 
    margin: 0.5rem 0; 
    background: rgba(255,255,255,0.1); 
    border-radius: 10px; 
    border: 1px solid rgba(0,234,255,0.3);
}

.heatmap-item a { 
    color: #00eaff; 
    text-decoration: none; 
    font-weight: 600; 
}
.heatmap-item a:hover { color: #fff; text-decoration: underline; }

footer { margin-top:2rem; padding:1.2rem; text-align:center; font-size:0.9rem; color:#cceeff; }
</style>
</head>
<body>

<nav>
    <button id="menu-toggle">
        <div class="hamburger"><span></span><span></span><span></span></div>
        <span class="menu-text">Menu</span>
    </button>
    <a href="index.html">Home</a>
    <a href="about.html">About</a>
    <a href="why.html">Why Sharks</a>
    <a href="nasa.html">NASA Data</a>
    <a href="tag.html">Next-Gen Tag</a>
    <a href="tracker.html">Shark Tracker</a>
    <a href="contact.html">Contact</a>
</nav>

<div class="sidebar-menu" id="sidebarMenu">
    <a href="habitat.html">Shark Habitat</a>
    <a href="types.html">Types of Sharks</a>
    <a href="migration.html">Migration Cycle</a>
    <a href="aboutus.html">About Us</a>
</div>

<div class="main-content">
    <div class="content-container">
        <h1>🦈 Shark Probability Tracker</h1>
        <p>Generate interactive shark probability heatmaps using NASA satellite data and machine learning algorithms.</p>
    </div>

    <!-- Control Panel -->
    <div class="control-panel">
        <div class="control-group">
            <label for="gridRes">Grid Resolution (degrees)</label>
            <input type="number" id="gridRes" value="0.25" step="0.05" min="0.1" max="1.0">
        </div>
        <div class="control-group">
            <label for="probThreshold">Probability Threshold</label>
            <input type="number" id="probThreshold" value="0.4" step="0.05" min="0.1" max="1.0">
        </div>
        <div class="control-group">
            <label for="testSize">Test Size</label>
            <input type="number" id="testSize" value="0.2" step="0.05" min="0.1" max="0.5">
        </div>
        <div class="control-group">
            <label for="nEst">Random Forest Trees</label>
            <input type="number" id="nEst" value="200" step="50" min="50" max="500">
        </div>
    </div>

    <!-- Action Buttons -->
    <div style="text-align: center; margin-bottom: 2rem;">
        <button class="btn btn-primary" onclick="generateSyntheticData()">
            <span id="syntheticSpinner" class="loading-spinner" style="display: none;"></span>
            Generate Synthetic Data
        </button>
        <button class="btn btn-primary" onclick="generateHeatmap()">
            <span id="heatmapSpinner" class="loading-spinner" style="display: none;"></span>
            Generate Heatmap
        </button>
        <button class="btn btn-secondary" onclick="loadDataInfo()">
            <span id="infoSpinner" class="loading-spinner" style="display: none;"></span>
            Load Data Info
        </button>
        <button class="btn btn-secondary" onclick="refreshHeatmapList()">
            <span id="listSpinner" class="loading-spinner" style="display: none;"></span>
            Refresh Heatmaps
        </button>
    </div>

    <!-- Status Messages -->
    <div id="statusContainer"></div>

    <!-- Data Information -->
    <div id="dataInfoContainer" style="display: none;">
        <div class="content-container">
            <h2>📊 Current Dataset Information</h2>
            <div id="dataInfoContent"></div>
        </div>
    </div>

    <!-- Heatmap List -->
    <div class="heatmap-list">
        <h2>🗺️ Generated Heatmaps</h2>
        <div id="heatmapListContent">
            <p>Click "Refresh Heatmaps" to see available heatmaps.</p>
        </div>
    </div>

    <!-- Map Display -->
    <div class="map-container">
        <h2>🌍 Interactive Shark Probability Map</h2>
        <div id="mapDisplay">
            <p>Generate a heatmap to see the interactive map here.</p>
        </div>
    </div>

    <footer>
        &copy; 2025 Shark from Space | <strong>The Commit Crew</strong>
    </footer>
</div>

<script>
// API Base URL
const API_BASE = window.location.origin;

// Utility functions
function showStatus(message, type = 'info') {
    const container = document.getElementById('statusContainer');
    const statusDiv = document.createElement('div');
    statusDiv.className = `status ${type}`;
    statusDiv.innerHTML = message;
    container.appendChild(statusDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (statusDiv.parentNode) {
            statusDiv.parentNode.removeChild(statusDiv);
        }
    }, 5000);
}

function showSpinner(elementId) {
    document.getElementById(elementId).style.display = 'inline-block';
}

function hideSpinner(elementId) {
    document.getElementById(elementId).style.display = 'none';
}

// API Functions
async function generateSyntheticData() {
    showSpinner('syntheticSpinner');
    showStatus('Generating synthetic ocean data...', 'loading');
    
    try {
        const response = await fetch(`${API_BASE}/api/generate-synthetic-data`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            showStatus(`✅ ${result.message}`, 'success');
        } else {
            showStatus(`❌ Error: ${result.error}`, 'error');
        }
    } catch (error) {
        showStatus(`❌ Network error: ${error.message}`, 'error');
    } finally {
        hideSpinner('syntheticSpinner');
    }
}

async function generateHeatmap() {
    showSpinner('heatmapSpinner');
    showStatus('Generating shark probability heatmap...', 'loading');
    
    const params = {
        grid_res: parseFloat(document.getElementById('gridRes').value),
        prob_threshold: parseFloat(document.getElementById('probThreshold').value),
        test_size: parseFloat(document.getElementById('testSize').value),
        n_est: parseInt(document.getElementById('nEst').value)
    };
    
    try {
        const response = await fetch(`${API_BASE}/api/generate-heatmap`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showStatus(`✅ ${result.message}`, 'success');
            // Refresh the heatmap list
            setTimeout(refreshHeatmapList, 1000);
        } else {
            showStatus(`❌ Error: ${result.error}`, 'error');
        }
    } catch (error) {
        showStatus(`❌ Network error: ${error.message}`, 'error');
    } finally {
        hideSpinner('heatmapSpinner');
    }
}

async function loadDataInfo() {
    showSpinner('infoSpinner');
    
    try {
        const response = await fetch(`${API_BASE}/api/data-info`);
        const result = await response.json();
        
        if (result.success) {
            const container = document.getElementById('dataInfoContainer');
            const content = document.getElementById('dataInfoContent');
            
            content.innerHTML = `
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div><strong>Data Points:</strong> ${result.rows.toLocaleString()}</div>
                    <div><strong>Latitude Range:</strong> ${result.bounds.lat_min.toFixed(2)}° to ${result.bounds.lat_max.toFixed(2)}°</div>
                    <div><strong>Longitude Range:</strong> ${result.bounds.lon_min.toFixed(2)}° to ${result.bounds.lon_max.toFixed(2)}°</div>
                    <div><strong>Avg Sea Surface Temp:</strong> ${result.stats.sst_mean.toFixed(2)}°C</div>
                    <div><strong>Avg Chlorophyll:</strong> ${result.stats.chlor_mean.toFixed(2)} mg/m³</div>
                    <div><strong>Avg Ocean Depth:</strong> ${Math.abs(result.stats.depth_mean).toFixed(0)}m</div>
                </div>
                <div style="margin-top: 1rem;">
                    <strong>Available Parameters:</strong> ${result.columns.join(', ')}
                </div>
            `;
            
            container.style.display = 'block';
            showStatus('✅ Data information loaded', 'success');
        } else {
            showStatus(`❌ Error: ${result.error}`, 'error');
        }
    } catch (error) {
        showStatus(`❌ Network error: ${error.message}`, 'error');
    } finally {
        hideSpinner('infoSpinner');
    }
}

async function refreshHeatmapList() {
    showSpinner('listSpinner');
    
    try {
        const response = await fetch(`${API_BASE}/api/list-heatmaps`);
        const result = await response.json();
        
        if (result.success) {
            const content = document.getElementById('heatmapListContent');
            
            if (result.heatmaps.length === 0) {
                content.innerHTML = '<p>No heatmaps generated yet. Generate one to see it here!</p>';
            } else {
                content.innerHTML = result.heatmaps.map(filename => `
                    <div class="heatmap-item">
                        <span>${filename}</span>
                        <a href="${API_BASE}/api/heatmap/${filename}" target="_blank">View Map</a>
                    </div>
                `).join('');
            }
            
            showStatus('✅ Heatmap list refreshed', 'success');
        } else {
            showStatus(`❌ Error: ${result.error}`, 'error');
        }
    } catch (error) {
        showStatus(`❌ Network error: ${error.message}`, 'error');
    } finally {
        hideSpinner('listSpinner');
    }
}

async function displayFirstHeatmap() {
    try {
        const response = await fetch(`${API_BASE}/api/list-heatmaps`);
        const result = await response.json();

        const mapContainer = document.getElementById('mapDisplay');

        if (result.success && result.heatmaps.length > 0) {
            // Get the first heatmap
            const firstHeatmap = result.heatmaps[0];

            // Embed the heatmap using iframe
            mapContainer.innerHTML = `
                <iframe 
                    src="${API_BASE}/api/heatmap/${firstHeatmap}" 
                    width="100%" 
                    height="500px" 
                    style="border:none; border-radius:15px;">
                </iframe>
            `;
        } else {
            mapContainer.innerHTML = '<p>Generate a heatmap to see the interactive map here.</p>';
        }
    } catch (error) {
        console.error('Error loading first heatmap:', error);
        mapContainer.innerHTML = '<p>Unable to load heatmap.</p>';
    }
}

// Call this on page load
document.addEventListener('DOMContentLoaded', () => {
    showStatus('🦈 Shark Tracker loaded! Generate synthetic data and heatmaps to get started.', 'info');
    displayFirstHeatmap(); // <-- Display the first map automatically
});


// Menu functionality
const menuBtn = document.getElementById('menu-toggle');
const sidebarMenu = document.getElementById('sidebarMenu');
menuBtn.addEventListener('click', () => {
    menuBtn.classList.toggle('active');
    sidebarMenu.classList.toggle('show');
});

// Load initial data
document.addEventListener('DOMContentLoaded', () => {
    showStatus('🦈 Shark Tracker loaded! Generate synthetic data and heatmaps to get started.', 'info');
});
</script>

</body>
</html>
