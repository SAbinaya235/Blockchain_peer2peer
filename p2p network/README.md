# 🔗 Blockchain P2P Network

A beautiful, simplified blockchain implementation with peer-to-peer networking and a stunning dark theme interface.

## ✨ Features

- **Dark Theme**: Beautiful gradient design with dark pink, yellow, blue, and green accents
- **Simple Interface**: Clean, easy-to-use web dashboard
- **Blockchain Core**: Complete blockchain with blocks, transactions, and mining
- **P2P Network**: 4 nodes that communicate and sync automatically
- **Real-time Updates**: Live status monitoring and automatic refresh

## 📁 Project Structure

```
├── blockchain.py          # Core blockchain logic
├── node_server.py         # Individual node server
├── simple_dashboard.py    # Web interface server
├── templates/simple.html  # Beautiful dark theme UI
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Dashboard
```bash
python simple_dashboard.py
```

### 3. Open Your Browser
Go to: **http://localhost:8080**

## 🎨 Beautiful Dark Theme

The interface features:
- **Black gradient background** with subtle depth
- **Dark pink** (#ff6b9d) for primary actions
- **Dark yellow** (#ffd93d) for highlights and stats
- **Dark blue** (#45b7d1) for info elements
- **Dark green** (#4ecdc4) for success states
- **Smooth animations** and hover effects
- **Custom scrollbars** with gradient colors

## 🎯 How to Use

### Start the Network
1. Click **"Start All Nodes"** button
2. Watch all 4 nodes turn green (online)
3. Nodes automatically register with each other

### Create Transactions
1. Fill in the transaction form:
   - **From**: Who is sending money
   - **To**: Who is receiving money
   - **Amount**: How much money
   - **Node**: Which node to use
2. Click **"Send Transaction"**

### Mine Blocks
1. Click **"Mine"** on any online node
2. Watch the mining process (takes a few seconds)
3. New block is created with pending transactions

### View Blockchain
1. Select a node from the dropdown
2. Click **"View Blockchain"**
3. See all blocks and transactions in beautiful cards

### Stop Everything
1. Click **"Stop All Nodes"**
2. All nodes shut down cleanly

## 🎨 Color Palette

| Element | Color | Hex Code |
|---------|-------|----------|
| Primary Actions | Dark Pink | #ff6b9d |
| Success States | Dark Green | #4ecdc4 |
| Warning/Info | Dark Yellow | #ffd93d |
| Info Elements | Dark Blue | #45b7d1 |
| Background | Black Gradient | #0a0a0a → #1a1a1a |
| Cards | Dark Gray | #1e1e1e → #2d2d2d |

## 🔧 Technical Details

- **Mining Difficulty**: 4 leading zeros (easy for demo)
- **Hash Algorithm**: SHA-256
- **Consensus**: Longest chain wins
- **Auto-sync**: Every 30 seconds
- **Real-time Updates**: Every 5 seconds

## 📱 Responsive Design

The interface works perfectly on:
- Desktop computers
- Tablets
- Mobile phones
- All screen sizes

## 🎉 Perfect for Learning

This simplified version focuses on the **core blockchain concepts**:
- How blocks are created and linked
- How transactions work
- How mining secures the network
- How nodes communicate
- How consensus works

**No overwhelming complexity** - just the essential blockchain concepts in a beautiful, easy-to-use interface!

## 🚀 Ready to Explore?

1. Start the dashboard: `python simple_dashboard.py`
2. Open http://localhost:8080
3. Click "Start All Nodes"
4. Create some transactions
5. Mine some blocks
6. Explore the blockchain!

The beautiful dark theme makes learning blockchain technology both educational and visually stunning! ✨ 