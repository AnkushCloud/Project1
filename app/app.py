from flask import Flask, jsonify, send_file
import random
import math
import os
import json
from pathlib import Path

app = Flask(__name__)

# Load configuration from ConfigMap
def load_config():
    config_path = Path('/app/config/environment.properties')
    config = {}
    if config_path.exists():
        with open(config_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key] = value
    return config

app_config = load_config()

@app.route('/')
def hello_world():
    welcome_path = Path('/app/config/welcome-message.txt')
    welcome_message = "Hello, World!"
    
    if welcome_path.exists():
        with open(welcome_path, 'r') as f:
            welcome_message = f.read().strip()
    
    return jsonify({
        "message": welcome_message,
        "version": app_config.get('APP_VERSION', '1.0'),
        "environment": app_config.get('DEPLOYMENT_ENVIRONMENT', 'development'),
        "pod": os.environ.get('HOSTNAME', 'unknown')
    })

@app.route('/config')
def show_config():
    """Endpoint to display current configuration"""
    config_path = Path('/app/config/app-config.json')
    config_data = {}
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            config_data = json.load(f)
    
    return jsonify({
        "config": config_data,
        "environment_vars": {
            "APP_NAME": os.environ.get('APP_NAME'),
            "DEPLOYMENT_ENVIRONMENT": os.environ.get('DEPLOYMENT_ENVIRONMENT')
        },
        "pod": os.environ.get('HOSTNAME', 'unknown')
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/cpu-intensive')
def cpu_intensive():
    # Check if CPU intensive route is enabled
    if app_config.get('ENABLE_CPU_INTENSIVE_ROUTE', 'true').lower() == 'false':
        return jsonify({"error": "CPU intensive route is disabled"}), 503
    
    # Simulate CPU-intensive work
    n = 100000
    result = 0
    for i in range(n):
        result += math.sqrt(i) * math.sin(i)
    
    return jsonify({
        "result": result,
        "message": "CPU intensive task completed",
        "iterations": n,
        "pod": os.environ.get('HOSTNAME', 'unknown')
    })

@app.route('/memory-intensive')
def memory_intensive():
    # Check if memory intensive route is enabled
    if app_config.get('ENABLE_MEMORY_INTENSIVE_ROUTE', 'true').lower() == 'false':
        return jsonify({"error": "Memory intensive route is disabled"}), 503
    
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