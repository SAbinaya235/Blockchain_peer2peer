import hashlib
import json
import time
from typing import List, Dict, Any
from urllib.parse import urlparse
import requests


class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        return cls(data['sender'], data['recipient'], data['amount'])


class Block:
    def __init__(self, index: int, transactions: List[Transaction], timestamp: float, previous_hash: str, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate the hash of the block"""
        block_string = json.dumps({
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Block':
        transactions = [Transaction.from_dict(tx) for tx in data['transactions']]
        block = cls(
            data['index'],
            transactions,
            data['timestamp'],
            data['previous_hash'],
            data['nonce']
        )
        block.hash = data['hash']
        return block


class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.current_transactions: List[Transaction] = []
        self.nodes = set()
        self.difficulty = 4  # Number of leading zeros required for proof-of-work
        
        # Create the genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(0, [], time.time(), "0")
        self.chain.append(genesis_block)
    
    def get_last_block(self) -> Block:
        """Get the last block in the chain"""
        return self.chain[-1]
    
    def add_transaction(self, sender: str, recipient: str, amount: float) -> int:
        """Add a new transaction to the list of pending transactions"""
        transaction = Transaction(sender, recipient, amount)
        self.current_transactions.append(transaction)
        return self.get_last_block().index + 1
    
    def proof_of_work(self, last_block: Block) -> int:
        """Simple proof of work algorithm"""
        nonce = 0
        while True:
            block = Block(
                last_block.index + 1,
                self.current_transactions,
                time.time(),
                last_block.hash,
                nonce
            )
            
            if block.hash.startswith('0' * self.difficulty):
                return nonce
            nonce += 1
    
    def mine_block(self, miner_address: str) -> Block:
        """Mine a new block"""
        last_block = self.get_last_block()
        
        # Add mining reward transaction
        self.add_transaction("0", miner_address, 10.0)  # Mining reward
        
        # Find the proof of work
        nonce = self.proof_of_work(last_block)
        
        # Create the new block
        new_block = Block(
            last_block.index + 1,
            self.current_transactions,
            time.time(),
            last_block.hash,
            nonce
        )
        
        # Add the block to the chain
        self.chain.append(new_block)
        
        # Reset the current list of transactions
        self.current_transactions = []
        
        return new_block
    
    def is_chain_valid(self, chain: List[Block] = None) -> bool:
        """Check if the blockchain is valid"""
        if chain is None:
            chain = self.chain
        
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]
            
            # Check that the hash of the block is correct
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check that the previous hash reference is correct
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def register_node(self, address: str):
        """Add a new node to the list of nodes"""
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    def resolve_conflicts(self) -> bool:
        """Consensus algorithm: replace our chain with the longest valid chain"""
        neighbours = self.nodes
        new_chain = None
        
        # We're only looking for chains longer than ours
        max_length = len(self.chain)
        
        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            try:
                response = requests.get(f'http://{node}/chain')
                if response.status_code == 200:
                    chain_data = response.json()
                    chain = [Block.from_dict(block) for block in chain_data['chain']]
                    length = chain_data['length']
                    
                    # Check if the length is longer and the chain is valid
                    if length > max_length and self.is_chain_valid(chain):
                        max_length = length
                        new_chain = chain
            except requests.RequestException:
                continue
        
        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True
        
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'chain': [block.to_dict() for block in self.chain],
            'length': len(self.chain),
            'current_transactions': [tx.to_dict() for tx in self.current_transactions],
            'nodes': list(self.nodes)
        } 