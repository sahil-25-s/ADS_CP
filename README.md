# Campus Stall Finder System

Advanced Data Structures project - Flask-based web application for finding campus stalls.

## Features
- 🏠 Home page with feature overview
- 🗺️ Interactive map view with visual stall markers
- 📋 Stalls listing with category filtering
- 🔍 Live search functionality
- 📍 Individual stall detail pages

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open browser and navigate to:
```
http://127.0.0.1:5000
```

## Project Structure
```
ADS_CP/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── home.html         # Home page
│   ├── map.html          # Interactive map view
│   ├── stalls.html       # Stalls listing
│   ├── stall_detail.html # Individual stall details
│   └── search.html       # Search page
└── static/               # Static files (currently empty)
```

## Routes
- `/` - Home page
- `/map` - Interactive map view
- `/stalls` - Browse all stalls (with filtering)
- `/stall/<id>` - Individual stall details
- `/search` - Search stalls
- `/api/search` - Search API endpoint

## Note
This is a UI-focused implementation using dummy data. Spatial data structures (KD-Tree, QuadTree) will be integrated later for nearest neighbor and range queries.
