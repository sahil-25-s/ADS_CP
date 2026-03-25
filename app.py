from flask import Flask, render_template, request, jsonify
from kdtree import KDTree

app = Flask(__name__)

STALLS = []
_next_id = 1
kd_tree = KDTree([])

def _rebuild_tree():
    global kd_tree
    kd_tree = KDTree(STALLS)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/map')
def map_view():
    return render_template('map.html')

@app.route('/stalls')
def stalls_list():
    stall_type = request.args.get('type', 'all')
    filtered = STALLS if stall_type == 'all' else [s for s in STALLS if s['type'] == stall_type]
    return render_template('stalls.html', stalls=filtered, selected_type=stall_type)

@app.route('/stall/<int:stall_id>')
def stall_detail(stall_id):
    stall = next((s for s in STALLS if s['id'] == stall_id), None)
    return render_template('stall_detail.html', stall=stall)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/api/stalls')
def api_stalls():
    return jsonify(STALLS)

@app.route('/api/stall/add', methods=['POST'])
def api_add_stall():
    global _next_id
    data = request.json
    stall = {
        'id': _next_id,
        'name': data['name'],
        'type': data['type'],
        'rating': float(data.get('rating', 0)),
        'lat': float(data['lat']),
        'lng': float(data['lng']),
    }
    _next_id += 1
    STALLS.append(stall)
    _rebuild_tree()
    return jsonify(stall), 201

@app.route('/api/stall/<int:stall_id>', methods=['DELETE'])
def api_delete_stall(stall_id):
    global STALLS
    STALLS = [s for s in STALLS if s['id'] != stall_id]
    _rebuild_tree()
    return jsonify({'ok': True})

@app.route('/api/search', methods=['POST'])
def api_search():
    query = request.json.get('query', '').lower()
    results = [s for s in STALLS if query in s['name'].lower() or query in s['type'].lower()]
    return jsonify(results)

@app.route('/api/nearest', methods=['POST'])
def api_nearest():
    data = request.json
    point = {'lat': float(data['lat']), 'lng': float(data['lng'])}
    k = int(data.get('k', 3))
    return jsonify(kd_tree.nearest(point, k))

@app.route('/api/range', methods=['POST'])
def api_range():
    data = request.json
    point = {'lat': float(data['lat']), 'lng': float(data['lng'])}
    radius = float(data.get('radius', 0.005))
    return jsonify(kd_tree.range_query(point, radius))

if __name__ == '__main__':
    app.run(debug=True)
