from flask import Flask, request, jsonify
from blockchain import Blockchain
import json
import uuid
import threading
import time

app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid.uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    """Mine a new block"""
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.get_last_block()
    nonce = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.add_transaction(
        sender="0",
        recipient=node_identifier,
        amount=10.0,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = last_block.hash
    block = blockchain.mine_block(node_identifier)

    response = {
        'message': "New Block Forged",
        'index': block.index,
        'transactions': [tx.to_dict() for tx in block.transactions],
        'nonce': block.nonce,
        'previous_hash': block.previous_hash,
        'hash': block.hash,
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """Create a new transaction"""
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.add_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    """Return the full blockchain"""
    response = blockchain.to_dict()
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    """Register a list of new nodes"""
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    """Resolve conflicts between blockchain nodes"""
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.to_dict()
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.to_dict()
        }

    return jsonify(response), 200

@app.route('/nodes/sync', methods=['GET'])
def sync_chain():
    """Sync the blockchain with other nodes"""
    replaced = blockchain.resolve_conflicts()
    
    response = {
        'message': 'Chain synced' if replaced else 'Chain already up to date',
        'chain_length': len(blockchain.chain),
        'nodes': list(blockchain.nodes)
    }
    return jsonify(response), 200

@app.route('/status', methods=['GET'])
def status():
    """Get the current status of the node"""
    response = {
        'node_id': node_identifier,
        'chain_length': len(blockchain.chain),
        'pending_transactions': len(blockchain.current_transactions),
        'connected_nodes': list(blockchain.nodes),
        'last_block': blockchain.get_last_block().to_dict() if blockchain.chain else None
    }
    return jsonify(response), 200

@app.route('/transactions/pending', methods=['GET'])
def pending_transactions():
    """Get all pending transactions"""
    response = {
        'transactions': [tx.to_dict() for tx in blockchain.current_transactions],
        'count': len(blockchain.current_transactions)
    }
    return jsonify(response), 200

def auto_sync():
    """Automatically sync with other nodes every 30 seconds"""
    while True:
        time.sleep(30)
        try:
            blockchain.resolve_conflicts()
            print(f"Node {node_identifier[:8]}... auto-synced")
        except Exception as e:
            print(f"Auto-sync error: {e}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python node_server.py <port>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    
    # Start auto-sync thread
    sync_thread = threading.Thread(target=auto_sync, daemon=True)
    sync_thread.start()
    
    print(f"Starting blockchain node on port {port}")
    print(f"Node ID: {node_identifier}")
    print(f"API endpoints:")
    print(f"  GET  /mine - Mine a new block")
    print(f"  POST /transactions/new - Create a new transaction")
    print(f"  GET  /chain - Get the full blockchain")
    print(f"  POST /nodes/register - Register new nodes")
    print(f"  GET  /nodes/resolve - Resolve conflicts")
    print(f"  GET  /nodes/sync - Sync with other nodes")
    print(f"  GET  /status - Get node status")
    print(f"  GET  /transactions/pending - Get pending transactions")
    
    app.run(host='0.0.0.0', port=port, debug=False) 