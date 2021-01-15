import hashlib
import json
import requests
from time import time
from urllib.parse import urlparse

from .Block import Block
from .Proof import Proof

class Blockchain(object):
  def __init__(self):
    self.chain = []
    self.current_transactions = []
    self.nodes = set()

    # Create the genesis block
    self.new_block(previous_hash=1, proof=100)
  

  @staticmethod
  def hash(block):
    """
    Hashes a block using SHA-256 hash
    """
    # Dictionary must be ordered to have consistent hashes
    # representing 
    block_string = json.dumps(dict(block), sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

  @property
  def last_block(self):
    return self.chain[-1]

  def get_chain(self):
    return [dict(obj) for obj in self.chain]

  def new_block(self, proof, previous_hash=None):
    """
    Creates a new Block and adds it to the chain
    """

    # Build the block
    block = Block(
      index=len(self.chain) + 1,
      timestamp=time(),
      transactions=self.current_transactions,
      proof=proof,
      previous_hash=previous_hash or self.hash(self.chain[-1])
    )

    # Reset current list of transactions
    self.current_transactions = []

    self.chain.append(block)
    return block

  def new_transaction(self, sender, recipient, data):
    """
    Adds a new transaction to the list of transactions
    """

    self.current_transactions.append({
      'sender': sender,
      'recipient': recipient,
      'data': data,
    })
  
    return self.last_block.index + 1 # This could be an issue

  def register_node(self, addr):
    """
    Add a new node to the list of nodes
    """
    parsed_url = urlparse(addr)
    self.nodes.add(parsed_url.netloc)

  def resolve_conflicts(self):
    """
    Consensus algorithm. Resolves conflicts by replacing chain
    with the largest in the network
    """

    neighbors = self.nodes
    new_chain = None

    # Look for chains longer than ours 
    max_length = len(self.chain)

    # Verify chains from all nodes in the network
    for node in neighbors:
      response = requests.get(f'http://{node}/chain')

      if response.status_code == 200:
        length = response.json()['length']
        chain = response.json()['chain']

        if length > max_length and self.valid_chain(chain):
          max_length = length
          new_chain = chain

      # Replace the chain if there's a new, valid chain that's longer
      if new_chain:
        self.chain = new_chain
        return True

      return False

  def valid_chain(self, chain):
    """
    Determine if a given blockchain is valid
    """

    last_block = chain[0]
    current_index = 1

    while current_index < len(chain):
      block = chain[current_index]
      print(f'{last_block}')
      print(f'{block}')
      print('\n-----------\n')

      # Check if the hash of the block is correct
      if block['previous_hash'] != self.hash(last_block):
        return False

      last_block = block
      current_index += 1

    return True
    
  def proof_of_work(self, last_proof):
    return Proof.proof_of_work(last_proof)

  def valid_proof(self, last_proof, proof):
    return Proof.is_valid_proof(last_proof, proof)
