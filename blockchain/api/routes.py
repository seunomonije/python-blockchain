import json

from uuid import uuid4
from flask import Flask, jsonify, request

import sys
sys.path.append('..')
from src.Blockchain import Blockchain

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
  # Run proof algo to get the next proof
  last_block = blockchain.last_block
  last_proof = last_block.proof
  proof = blockchain.proof_of_work(last_proof)

  # Give a reward for finding proof. New coin comes form 0 sender
  blockchain.new_transaction(
    sender='0',
    recipient=node_identifier,
    data=1,
  )

  # Add new block to the chain
  previous_hash = blockchain.hash(last_block)
  block = blockchain.new_block(proof, previous_hash)

  response = {
    'message': 'New Block Forged',
    'index': block.index,
    'transactions': block.transactions,
    'proof': block.proof,
    'previous_hash': block.previous_hash,
  }

  return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
  # If there's a problem with json, set force=True in get_json()
  values = request.get_json()

  # Check that the required fields are in the POST data
  required = ['sender', 'recipient', 'data']
  print(values)
  if not all(k in values for k in required):
    return 'Missing values', 400

  index = blockchain.new_transaction(values['sender'], 
    values['recipient'], values['data'])

  response = {'message': f'Transaction will be added to Block {index}'}
  return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
  chain = blockchain.get_chain()
  response = {
    'chain': chain,
    'length': len(chain),
  }
  return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
  values = request.get_json()

  nodes = values.get('nodes')
  if nodes is None:
    return 'Error: Please supply a valid list of nodes', 400

  for node in nodes:
    blockchain.register_node(node)

  response = {
    'message': 'New nodes have been added',
    'total_nodes': list(blockchain.nodes)
  }

  return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
  replaced = blockchain.resolve_conflicts()

  if replaced:
    response = {
      'message': 'The chain needed to be replaced, and has been',
      'new_chain': blockchain.get_chain(),
    }
  else:
    response = {
      'message': 'Our chain is valid',
      'chain': blockchain.get_chain()
    }
  
  return jsonify(response), 200

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000)