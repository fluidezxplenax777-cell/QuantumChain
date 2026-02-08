import hashlib
import time
import json

# --- QuantumChain Block Definition ---
class Block:
    """
    Represents a single block in the QuantumChain blockchain.
    Each block contains a unique index, timestamp, transactional data,
    the hash of the previous block, a nonce (for potential PoW/tuning),
    and a PoI score reflecting the creator's importance.
    """
    def __init__(self, index, timestamp, data, previous_hash, nonce=0, poi_score=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data # Can be a dictionary of transactions or other relevant data
        self.previous_hash = previous_hash
        self.nonce = nonce # Can be used for PoW-like elements or as an identifier
        self.poi_score = poi_score # The Proof of Importance score of the block creator
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calculates the SHA256 hash of the block by concatenating its key attributes.
        The `sort_keys=True` ensures consistent hash generation.
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "poi_score": self.poi_score
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def update_poi_score_and_rehash(self, new_poi_score):
        """
        Updates the PoI score of the block and recalculates its hash.
        This might be used if a block is proposed, and its importance needs
        to be adjusted before finalization, though typically PoI is set at creation.
        """
        self.poi_score = new_poi_score
        self.hash = self.calculate_hash()

    def __repr__(self):
        """Provides a string representation for debugging and logging."""
        return (f"Block(Index: {self.index}, Timestamp: {self.timestamp:.2f}, "
                f"Data: {self.data}, Prev_Hash: {self.previous_hash[:10]}..., "
                f"PoI_Score: {self.poi_score}, Hash: {self.hash[:10]}...)")

# --- QuantumChain PoI Validation Module ---
class PoIValidator:
    """
    Handles the validation logic for Proof of Importance within the QuantumChain network.
    It simulates how a node's importance is calculated and verified.
    """
    def __init__(self, network_context=None):
        """
        Initializes the PoI validator with relevant network context.
        The network_context would contain access to ledger state,
        node reputation, transaction history, etc.
        """
        self.network_context = network_context # Placeholder for global chain state

    def _get_node_metrics(self, node_identifier, block_time):
        """
        Internal method to fetch critical metrics for a node at a given time.
        In a real system, this would query the blockchain state.
        Metrics could include:
        - Stake/Balance
        - Transaction Volume/Frequency
        - Network participation (e.g., successful block proposals, validations)
        - Uptime/Reliability
        - Reputation score (derived from historical behavior)
        """
        # --- SIMULATED METRICS ---
        # For demonstration, we use fixed or slightly varied values.
        # In production, these would come from the live network state.
        if node_identifier == "miner_node_A":
            return {
                "stake": 10000, # Tokens held
                "tx_volume_24h": 50, # Number of transactions processed
                "reputation": 0.85, # Historical reliability score (0-1)
                "online_duration_24h": 20 # Hours online
            }
        elif node_identifier == "miner_node_B":
            return {
                "stake": 500,
                "tx_volume_24h": 5,
                "reputation": 0.50,
                "online_duration_24h": 10
            }
        else: # Default for unknown nodes
            return {
                "stake": 100,
                "tx_volume_24h": 1,
                "reputation": 0.20,
                "online_duration_24h": 5
            }

    def calculate_importance(self, node_identifier, block_time):
        """
        Calculates the Importance Score for a given node based on its metrics.
        QuantumChain's PoI algorithm emphasizes network contribution,
        reliable participation, and economic stake.
        """
        metrics = self._get_node_metrics(node_identifier, block_time)

        # QuantumChain's Importance Formula (simplified for this prototype):
        # Importance = (Stake_Weight * Stake) + (TxVolume_Weight * TxVolume) +
        #              (Reputation_Weight * Reputation) + (Uptime_Weight * Uptime)
        # Weights would be dynamically adjusted by governance in a real system.
        stake_weight = 0.4
        tx_volume_weight = 0.25
        reputation_weight = 0.25
        uptime_weight = 0.1

        importance_score = (
            (stake_weight * metrics["stake"]) +
            (tx_volume_weight * metrics["tx_volume_24h"]) +
            (reputation_weight * (metrics["reputation"] * 100)) + # Scale reputation
            (uptime_weight * metrics["online_duration_24h"])
        )
        return importance_score

    def validate_poi(self, block, network_state_at_block_time, proposer_node_identifier):
        """
        Validates if the PoI score embedded in a block is legitimate and sufficient.
        This involves:
        1. Recalculating the importance of the block's proposer using historical data.
        2. Comparing the recalculated score against the block's `poi_score`.
        3. Ensuring the score meets the dynamic minimum threshold for block creation.
        """
        print(f"\n--- Validating PoI for Block {block.index} ---")
        print(f"Proposed PoI Score in Block: {block.poi_score}")

        recalculated_importance = self.calculate_importance(proposer_node_identifier, block.timestamp)
        print(f"Recalculated PoI for {proposer_node_identifier}: {recalculated_importance}")

        # Define a dynamic minimum PoI threshold
        # In a real QuantumChain, this might adjust based on network congestion,
        # overall importance distribution, or a governance model.
        MINIMUM_POI_THRESHOLD = 500 # Example threshold

        # Check 1: Does the block's score match the recalculated score (within a tolerance)?
        # A small tolerance accounts for floating point arithmetic or minor network sync delays.
        score_match_tolerance = 0.01 # 1% tolerance
        score_matches = abs(block.poi_score - recalculated_importance) / recalculated_importance <= score_match_tolerance
        if not score_matches:
            print(f"Validation Failed: Block's PoI score ({block.poi_score}) does not match "
                  f"recalculated importance ({recalculated_importance}) for {proposer_node_identifier}.")
            return False

        # Check 2: Does the importance score meet the minimum threshold?
        if recalculated_importance < MINIMUM_POI_THRESHOLD:
            print(f"Validation Failed: Node's importance ({recalculated_importance}) is below "
                  f"the minimum threshold ({MINIMUM_POI_THRESHOLD}).")
            return False

        print(f"Validation Passed: PoI score {block.poi_score} for {proposer_node_identifier} is valid and sufficient.")
        return True

# --- Example Usage (for demonstrating the Block and PoIValidator classes) ---
if __name__ == "__main__":
    print("Initializing QuantumChain Core Components...")

    # 1. Create a Genesis Block
    genesis_block = Block(
        index=0,
        timestamp=time.time(),
        data={"message": "QuantumChain Genesis Block", "validator": "QuantumCore"},
        previous_hash="0" * 64 # Standard genesis hash
    )
    print("\n--- Genesis Block Created ---")
    print(genesis_block)

    # 2. Simulate Node Importance Calculation
    poi_validator = PoIValidator()

    # Node A is a high-importance node
    node_a_id = "miner_node_A"
    node_a_importance = poi_validator.calculate_importance(node_a_id, time.time())
    print(f"\nCalculated Importance for {node_a_id}: {node_a_importance:.2f}")

    # Node B is a lower-importance node
    node_b_id = "miner_node_B"
    node_b_importance = poi_validator.calculate_importance(node_b_id, time.time())
    print(f"Calculated Importance for {node_b_id}: {node_b_importance:.2f}")

    # 3. Create a New Block proposed by Node A
    # Node A proposes a block and includes its calculated PoI score.
    second_block_data = {"transactions": ["Tx1_A->B_10QC", "Tx2_C->D_5QC"], "validator": node_a_id}
    second_block_timestamp = time.time()
    second_block = Block(
        index=1,
        timestamp=second_block_timestamp,
        data=second_block_data,
        previous_hash=genesis_block.hash,
        poi_score=node_a_importance # Node A's self-reported PoI
    )
    print("\n--- Second Block Proposed by Node A ---")
    print(second_block)

    # 4. Validate the Second Block's PoI
    is_second_block_poi_valid = poi_validator.validate_poi(second_block, "current_state_snapshot", node_a_id)
    print(f"Result for Second Block PoI Validation: {is_second_block_poi_valid}")

    # 5. Create another Block proposed by Node B (with insufficient importance)
    third_block_data = {"transactions": ["Tx3_E->F_20QC"], "validator": node_b_id}
    third_block_timestamp = time.time()
    third_block = Block(
        index=2,
        timestamp=third_block_timestamp,
        data=third_block_data,
        previous_hash=second_block.hash,
        poi_score=node_b_importance # Node B's self-reported PoI
    )
    print("\n--- Third Block Proposed by Node B ---")
    print(third_block)

    # 6. Validate the Third Block's PoI
    is_third_block_poi_valid = poi_validator.validate_poi(third_block, "current_state_snapshot", node_b_id)
    print(f"Result for Third Block PoI Validation: {is_third_block_poi_valid}")

    # 7. Demonstrate a block with a tampered PoI score
    # Let's say Node B tries to fake its importance
    fake_poi_score = 1500 # A high, but incorrect score for Node B
    fourth_block_data = {"transactions": ["Tx4_G->H_1QC"], "validator": node_b_id}
    fourth_block_timestamp = time.time()
    fourth_block = Block(
        index=3,
        timestamp=fourth_block_timestamp,
        data=fourth_block_data,
        previous_hash=third_block.hash,
        poi_score=fake_poi_score # Node B tries to report a fake high PoI
    )
    print("\n--- Fourth Block Proposed by Node B (with Faked PoI) ---")
    print(fourth_block)

    # 8. Validate the Fourth Block's PoI (should fail due to mismatch)
    is_fourth_block_poi_valid = poi_validator.validate_poi(fourth_block, "current_state_snapshot", node_b_id)
    print(f"Result for Fourth Block PoI Validation: {is_fourth_block_poi_valid}")
