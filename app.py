from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from core.cpu import CPUScheduler, Process
from core.memory import fifo, lru, optimal
from core.disk import fcfs as disk_fcfs, sstf
from core.deadlock import is_safe_detailed
from ml.model import MLModel

app = Flask(__name__, static_folder='static')
CORS(app)

ml_model = MLModel()
print("Training initial ML model...")
ml_model.train()
print("ML Model trained.")

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def send_static(path):
    return app.send_static_file(path)

@app.route('/api/cpu', methods=['POST'])
def api_cpu():
    data = request.json
    processes_data = data.get('processes', [])
    if not processes_data:
        return jsonify({"error": "No processes provided"}), 400
        
    processes = [
        Process(pid=p['pid'], arrival=p['arrival'], burst=p['burst'], priority=p.get('priority', 0))
        for p in processes_data
    ]
    
    scheduler = CPUScheduler()
    results = scheduler.run_all(processes)
    
    # Predict best using ML
    ml_pred = ml_model.predict(processes)
    
    return jsonify({
        "results": results,
        "ml_prediction": ml_pred
    })

@app.route('/api/memory', methods=['POST'])
def api_memory():
    data = request.json
    pages = data.get('pages', [])
    frames = data.get('frames', 3)
    
    f = fifo(pages, frames)
    l = lru(pages, frames)
    o = optimal(pages, frames)
    
    return jsonify({
        "fifo": f,
        "lru": l,
        "optimal": o
    })

@app.route('/api/disk', methods=['POST'])
def api_disk():
    data = request.json
    requests = data.get('requests', [])
    head = data.get('head', 0)
    
    f = disk_fcfs(requests, head)
    s = sstf(requests, head)
    
    return jsonify({
        "fcfs": f,
        "sstf": s
    })

@app.route('/api/deadlock', methods=['POST'])
def api_deadlock():
    data = request.json
    allocation = data.get('allocation', [])
    max_need = data.get('max_need', [])
    available = data.get('available', [])
    
    result = is_safe_detailed(allocation, max_need, available)
    
    return jsonify(result)

@app.route('/api/ml/metrics', methods=['GET'])
def api_ml_metrics():
    return jsonify(ml_model.metrics)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
