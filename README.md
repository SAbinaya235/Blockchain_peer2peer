# Blockchain P2P Network

This project is a simplified implementation of a blockchain system with peer-to-peer (P2P) networking capabilities and a web-based dashboard interface. It is intended for educational purposes to demonstrate key blockchain concepts, including transactions, mining, and consensus.

See it live at : https://blockchain-peer2peer.onrender.com/
## Features

* **Blockchain Core**: Implements blocks, transactions, proof-of-work mining, and chain validation.
* **P2P Node Communication**: Multiple nodes that register with one another and maintain synchronized blockchains.
* **Transaction Creation**: Users can create and broadcast transactions through the web interface.
* **Block Mining**: Nodes can mine pending transactions into blocks using a basic proof-of-work algorithm.
* **Blockchain Viewer**: View the current state of the blockchain from any participating node.
* **Web Interface**: A simple frontend for managing nodes, transactions, mining, and viewing blockchain data.

## Project Structure

```
├── blockchain.py          # Core blockchain logic
├── node_server.py         # Flask server for each node
├── simple_dashboard.py    # Web dashboard interface
├── templates/simple.html  # HTML template for the dashboard
├── requirements.txt       # Python dependencies
└── README.md              # Project overview
```

## Installation

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the dashboard:

   ```bash
   python simple_dashboard.py
   ```

3. Open the application in a web browser at:

   ```
   http://localhost:8080
   ```

## Usage

### Starting the Network

* Start all nodes from the dashboard. Nodes automatically register with each other and form a P2P network.

### Creating a Transaction

* Provide sender, receiver, and amount through the form.
* Choose a node to broadcast the transaction.

### Mining a Block

* Select a node and trigger the mining process.
* The node performs proof-of-work and appends a new block to its blockchain containing pending transactions.
* Other nodes sync the chain based on the longest valid chain rule.

### Viewing the Blockchain

* Select any node to display its blockchain.
* Each block contains its index, timestamp, transactions, nonce, and previous hash.

### Shutting Down

* All nodes can be stopped cleanly from the dashboard interface.

## Technical Details

* **Hashing Algorithm**: SHA-256
* **Consensus Mechanism**: Longest valid chain
* **Mining Difficulty**: Configured to allow easy demonstration (e.g., 4 leading zeros)
* **Synchronization Interval**: Nodes auto-sync periodically to maintain consistency
* **Interface Polling**: Real-time UI updates to reflect network status and blockchain state

## Output Screenshot

<img width="1757" height="860" alt="image" src="https://github.com/user-attachments/assets/ff0144b1-14e6-4a4c-80b3-ea805cc92c50" />
<img width="1642" height="672" alt="image" src="https://github.com/user-attachments/assets/821b3d7e-4e24-40e4-852b-a4b767b724ff" />

## Purpose

This project provides a foundational understanding of:

* How transactions are recorded in a distributed ledger
* How blocks are mined and linked cryptographically
* How P2P networks maintain consensus
* How basic blockchain synchronization and validation mechanisms operate

---
