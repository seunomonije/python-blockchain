# Python-blockchain

Implementation of a simple blockchain in Python.

### Instructions

Interacting with the backend requires an HTTP Client for the time being. I recommend using [this Chrome extension](https://chrome.google.com/webstore/detail/advanced-rest-client/hgmloofddffdnphfgcellkdfbfbjeloo?hl=en-US).

I recommend running this project in a virtual environment to keep everything clean. The requirements for the project can be found in `requirements.txt`. You can setup a virtual environment and install the requirements with (assuming python points to Python 3.3 or newer):
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

You can then run the Flask server by running `routes.py` in `blockchain/api/routes.py`

Some simple requests to try out are the `/mine`, `/chain`, and `/transactions/new` requests. Reading the code in `/blockchain/api/routes.py` can give more clarity how exactly to test it out.

Data exchanged between nodes as of now is integers, but the code can be easily altered to include custom datatypes. Future commits will include further scalability.

### Future work
  - More Scalability
  - Quantum implementation