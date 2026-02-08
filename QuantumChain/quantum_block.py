"""
QuantumChain Core Module: Block Definition and PoI Integration

This module defines the fundamental Block structure for the QuantumChain blockchain.
It integrates preliminary fields and methods essential for PoI (Proof of Importance)
consensus mechanism validation, laying the groundwork for secure and relevant block
creation and appending.
"""

import hashlib
import json
from datetime import datetime

class Block:
    """
    Represents a single block in the QuantumChain blockchain.
    Each block contains a set of transactions, links to the previous block,
    and includes data relevant for Proof of Importance (PoI) validation.
    """
    def __init__(self, index, timestamp, transactions, previous_hash, nonce=0, importance_data=None):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions # Could be a list of transaction objects
        self.previous_hash = previous_hash
        self.nonce = nonce # Can be adapted for PoI "mining" variations or randomness
        self.importance_data = importance_data if importance_data is not None else {}
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calculates the SHA-256 hash of the block's contents.
        Ensures consistency and integrity of block data.
        """
        # Ensure transactions are serialized consistently
        serialized_transactions = [
            tx.to_dict() if hasattr(tx, 'to_dict') else tx for tx in self.transactions
        ]
        
        block_string = json.dumps({
            "index": self.index,
            "timestamp": str(self.timestamp),
            "transactions": serialized_transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "importance_data": self.importance_data,
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def __repr__(self):
        return (f"Block(index={self.index}, timestamp='{self.timestamp}', "
                f"previous_hash='{self.previous_hash[:10]}...', hash='{self.hash[:10]}...', "
                f"transactions_count={len(self.transactions)}, "
                f"poi_factor={self.importance_data.get('score', 'N/A')})")

    @staticmethod
    def validate_poi(block, network_state):
        """
        Placeholder for Proof of Importance (PoI) validation logic.
        This method will determine if a block was created by an 'important' node
        based on various network metrics (e.g., transaction volume, staking, activity).

        Args:
            block (Block): The block to be validated.
            network_state (dict): Current state of the network, including node importance scores.

        Returns:
            bool: True if the block passes PoI validation, False otherwise.
        """
        # --- PoI Logic Definition (To be elaborated in 'poi_engine.py' or similar) ---
        # This is a preliminary implementation. A robust PoI requires deeper analysis
        # of network activity, transaction history, and potentially a reputation system.

        creator_id = block.importance_data.get("creator_id")
        claimed_score = block.importance_data.get("score")

        if not creator_id or not isinstance(claimed_score, (int, float)):
            # Block is missing critical PoI data
            return False

        # Retrieve the node's actual importance score from the network state
        # A more sophisticated system would verify the score at the block's timestamp.
        actual_score = network_state.get('node_importance_scores', {}).get(creator_id, 0)
        min_threshold = network_state.get('min_poi_threshold', 100) # Example threshold

        if actual_score < min_threshold:
            # Creator does not meet the minimum importance threshold
            return False
        
        # Verify that the claimed score is consistent with the actual score (e.g., within a valid range)
        # A block creator cannot claim an arbitrarily high score.
        # For simplicity, we assume claimed_score should not exceed the actual_score significantly.
        if claimed_score > actual_score:
            # Creator is claiming more importance than they possess
            return False

        # Further PoI checks could include:
        # - Validation of recent transaction activity by `creator_id`.
        # - Checking stake amount or network presence time.
        # - Verifying that the block adheres to network-defined PoI difficulty/complexity.

        # If all preliminary checks pass, consider it valid for now.
        return True

# --- End of Block Definition ---
# Further PoI logic and blockchain assembly will be developed in separate modules.
# This file provides the core data structure.
