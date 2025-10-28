from flask import Flask, jsonify
import random
import math
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({
        "message": "Hello, World!",
        "version": "1.0",
        "pod": os.environ.get('HOSTNAME', 'unknown')
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/cpu-intensive')
def cpu_intensive():
    # Simulate CPU-intensive work
    n = 100000
    result = 0
    for i in range(n):
        result += math.sqrt(i) * math.sin(i)
    
    return jsonify({
        "result": result,
        "message": "CPU intensive task completed",
        "pod": os.environ.get('HOSTNAME', 'unknown')
    })

@app.route('/memory-intensive')
def memory_intensive():
    # Simulate memory-intensive work
    large_list = [random.random() for _ in range(1000000)]
    sorted_list = sorted(large_list)
    
    return jsonify({
        "message": "Memory intensive task completed",
        "list_length": len(sorted_list),
        "pod": os.environ.get('HOSTNAME', 'unknown')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)