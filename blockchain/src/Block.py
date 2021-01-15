class Block:
  def __init__(self, **kwargs):
    self.index = kwargs.get('index')
    self.timestamp = kwargs.get('timestamp')
    self.transactions = kwargs.get('transactions')
    self.proof = kwargs.get('proof')
    self.previous_hash = kwargs.get('previous_hash')

  # Allows for Block to be represented as a dictionary
  # dict() constructor accepts an iterable of (key, value) pairs to construct a dictionary
  def __iter__(self):
    yield 'index', self.index
    yield 'timestamp', self.timestamp
    yield 'transactions', self.transactions
    yield 'proof', self.proof
    yield 'previous_hash', self.previous_hash

  # Force representation as a dictionary in all printable formats
  def __repr__(self):
    return dict(self)