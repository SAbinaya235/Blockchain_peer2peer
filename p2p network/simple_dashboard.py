from flask import Flask, render_template, request, jsonify
import requests
import subprocess
import sys
import time
import os

app = Flask(__name__)

# Simple configuration
NODES = [5000, 5001, 5002, 5003]
processes = []

@app.route('/')
def index():
    return render_template('simple.html')

@app.route('/api/start', methods=['POST'])
def start_nodes():
    """Start all blockchain nodes"""
    global processes
    
    if processes:
        return jsonify({"message": "Nodes already running"})
    
    try:
        for port in NODES:
            process = subprocess.Popen([
                sys.executable, 'node_server.py', str(port)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            processes.append(process)
        
        time.sleep(3)  # Wait for nodes to start
        
        # Register nodes with each other
        for i, port in enumerate(NODES):
            for j, other_port in enumerate(NODES):
                if i != j:
                    try:
                        requests.post(f'http://localhost:{port}/nodes/register', 
                                    json={'nodes': [f'http://localhost:{other_port}']})
                    except:
                        pass
        
        return jsonify({"message": "All nodes started successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/stop', methods=['POST'])
def stop_nodes():
    """Stop all blockchain nodes"""
    global processes
    
    for process in processes:
        process.terminate()
        process.wait()
    
    processes.clear()
    return jsonify({"message": "All nodes stopped!"})

@app.route('/api/status')
def get_status():
    """Get status of all nodes"""
    status = []
    
    for port in NODES:
        try:
            response = requests.get(f'http://localhost:{port}/status', timeout=2)
            if response.status_code == 200:
                data = response.json()
                status.append({
                    'port': port,
                    'online': True,
                    'blocks': data['chain_length'],
                    'pending': data['pending_transactions']
                })
            else:
                status.append({
                    'port': port,
                    'online': False,
                    'blocks': 0,
                    'pending': 0
                })
        except:
            status.append({
                'port': port,
                'online': False,
                'blocks': 0,
                'pending': 0
            })
    
    return jsonify(status)

@app.route('/api/mine/<int:port>', methods=['POST'])
def mine_block(port):
    """Mine a block on specific node"""
    try:
        response = requests.get(f'http://localhost:{port}/mine', timeout=30)
        if response.status_code == 200:
            result = response.json()
            return jsonify({"message": f"Block mined! Block #{result['index']}"})
        else:
            return jsonify({"error": "Mining failed"})
    except Exception as e:
        return jsonify({"error": f"Mining failed: {str(e)}"})

@app.route('/api/transaction', methods=['POST'])
def create_transaction():
    """Create a transaction"""
    data = request.get_json()
    sender = data.get('sender', '')
    recipient = data.get('recipient', '')
    amount = data.get('amount', 0)
    port = data.get('port', 5000)
    
    if not all([sender, recipient, amount]):
        return jsonify({"error": "Please fill all fields"})
    
    # First check if the node is online
    try:
        status_response = requests.get(f'http://localhost:{port}/status', timeout=2)
        if status_response.status_code != 200:
            return jsonify({"error": f"Node on port {port} is not running. Please start the network first."})
    except:
        return jsonify({"error": f"Node on port {port} is not accessible. Please start the network first."})
    
    try:
        response = requests.post(
            f'http://localhost:{port}/transactions/new',
            json={'sender': sender, 'recipient': recipient, 'amount': float(amount)},
            timeout=5
        )
        if response.status_code == 201:
            return jsonify({"message": "Transaction created!"})
        else:
            return jsonify({"error": "Transaction failed"})
    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"Node on port {port} is not running. Please start the network first."})
    except Exception as e:
        return jsonify({"error": f"Transaction failed: {str(e)}"})

@app.route('/api/chain/<int:port>')
def get_chain(port):
    """Get blockchain from specific node"""
    try:
        response = requests.get(f'http://localhost:{port}/chain', timeout=2)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to get blockchain"})
    except:
        return jsonify({"error": "Node not accessible"})

if __name__ == '__main__':
    print("🚀 Simple Blockchain Dashboard")
    print("Open your browser and go to: http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=False) 