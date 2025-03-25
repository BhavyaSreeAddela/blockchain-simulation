import hashlib
import time
import json

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_content).hexdigest()

    def mine_block(self, difficulty):
        """Proof-of-Work: Adjust nonce until hash meets difficulty target."""
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Adjust for Proof-of-Work complexity

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def add_block(self, transactions):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), transactions, last_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        """Check if hashes are correctly linked and unchanged."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash() or current.previous_hash != previous.hash:
                return False
        return True

    def print_blockchain(self):
        for block in self.chain:
            print(vars(block), "\n")

# --- Demonstration ---
bc = Blockchain()
bc.add_block(["Transaction 1"])
bc.add_block(["Transaction 2"])
bc.print_blockchain()

# Tampering Check
print("\nTampering with Blockchain...")
bc.chain[1].transactions = ["Hacked Transaction"]
print("Is blockchain valid?", bc.is_chain_valid())
