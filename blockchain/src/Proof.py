import hashlib

class Proof:
  @staticmethod
  def proof_of_work(last_proof):
    proof = 0
    while Proof.is_valid_proof(last_proof, proof) is False:
      proof +=1

    return proof

  @staticmethod
  def is_valid_proof(last_proof, proof):
    # We'll know the proof is validated if the hash contains 4 leading zeroes
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"
    