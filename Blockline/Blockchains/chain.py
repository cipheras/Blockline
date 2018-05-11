import hashlib, json, urllib
from urllib.parse import urlparse
import urllib.request 
import time
from time import clock
from uuid import *
from Mychain import forms
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django import http
import threading


class Blockchain:
   
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        self.new_block(previous_hash='1110', proof=100)

    # Register node
    def register_node(self,address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    # Valid chain
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # print(f'{last_block}')
            # print(f'{block}')
            # print('\n-----------\n')
            if block['previous_hash'] != self.hash(last_block):
                return False
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        
        return True 

    # Resolve conflicts
    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)
        for node in neighbours:
            response = urllib.request.urlopen(f'http://{node}/chain/')
          
            if response.status == 200 :
                json_chain = json.loads(response.read())
                length = json_chain['length']
                chain = json_chain['chain']
                                        
                if length > max_length  and  self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        
        if new_chain:
            self.chain = new_chain
            return True

        return False


    # new block
    def new_block(self, proof, previous_hash=None):
        block = {
			"index" : len(self.chain) + 1 ,
			"timestamp" : clock(),
            "transactions" : self.current_transactions,
			"proof" : proof,
			"previous_hash" : previous_hash or self.hash(self.chain[-1]),
		    }
        self.current_transactions = []
        self.chain.append(block)
        return block

    # new transaction
    def new_transaction(self, sender, recipient, amount, id, data):
        self.current_transactions.append({
			"sender": sender,
			"recipient": recipient,
			"amount": amount,
            "id" : id,
            "data" : data,
			})
        return self.last_block['index'] + 1


    # last block
    @property
    def last_block(self):
        return self.chain[-1]

    # hashing
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    # proof of work
    def proof_of_work(self,last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof
    
    # valid proof
    @staticmethod
    def valid_proof(last_proof,proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'
    
    
node_identifier = str(uuid4()).replace('-','')
   
blockchain = Blockchain()



def mine(request):
    last_block = blockchain.last_block                          
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender = 'Mining reward',
        recipient = node_identifier,
        amount = 100,
        id = "host_" + node_identifier,
        data = None
        )
    block = blockchain.new_block(proof)

    response = {
            "message" : "New block forged",
            "index" : block['index'],
            "transactions" : block['transactions'],
            "proof" : block['proof'],
            "previous_hash" : block['previous_hash'],
        }
    return JsonResponse(response)
   
    
def new_transactions(request):
    if request.method == 'POST':
        # value = json.loads(request.POST)
        val = forms.TransactionData(request.POST)
        if val.is_valid():
            values = val.cleaned_data
            index = blockchain.new_transaction(values['sender'], values['receiver'], values['amount'], values['id'],values['data'])
            response = {"message" : f"transaction will be added to block {index}"}
        else:
            response = {"message" : "Incorrect details"}
        # return render(request, 'transaction.html', {'response': response})
        return JsonResponse(response)
    else:
        # forward to New_transaction page
        return http.HttpResponseBadRequest('Bad request')

   
def full_chain(request):
    response= {
        "chain":blockchain.chain,
        "length":len(blockchain.chain)
        }
    return JsonResponse(response)


def register_nodes(request):
    if request.method == 'POST' :
        val = forms.RegisterNode(request.POST)
        if val.is_valid():
            values = val.cleaned_data
            nodes = values['node']
            # for node in nodes :
                 # blockchain.register_node(node)
 
            blockchain.register_node(nodes)
            response = {
                    "message" : "New node has been added",
                    "all_nodes" : list(blockchain.nodes),
                    }
        else:
            http.HttpResponseNotFound("Érror : Please supply a valid list of nodes")
            response = {
                "message" : "Invalid node",
                "total_nodes" : list(blockchain.nodes),
                "num_nodes" : len(blockchain.nodes),
                }
        return JsonResponse(response)
    else:
        return JsonResponse({
                "total_nodes" : list(blockchain.nodes),
                "num_nodes" : len(blockchain.nodes),
                })
    

def consensus(request):
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            "message" : "Our chain was replaced",
            "new_chain" : blockchain.chain
          }
    else:
        response = {
            "message" : "Our chain was taken as the main chain",
            "chain" : blockchain.chain
            }

    return JsonResponse(response)

#########################################################################

# Get nodes
def bootstrap():
    b = threading.Timer(30, bootstrap)
    b.daemon = True
    b.start()
    
    neighbours = blockchain.nodes
    new_nodes = None
    len_nodes = len(blockchain.nodes)
       
    for node in neighbours :
        response = urllib.request.urlopen(f'http://{node}/nodes/register')
        if response.status == 200:
            json_nodes = json.loads(response.read())
            num_nodes = json_nodes['num_nodes']
            nodes = json_nodes['total_nodes']
            
            if len_nodes < num_nodes :
                len_nodes = num_nodes
                new_nodes = nodes

        if new_nodes :
            blockchain.nodes = new_nodes
            return True
        
    return False


def resolve():
    res = threading.Timer(60, resolve)
    blockchain.resolve_conflicts()
    res.daemon = True
    res.start()

    
def demomine():
    t = threading.Timer(50,demomine)
    t.daemon = True
    t.start()

    last_block = blockchain.last_block                          
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender = 'Mining incentive',
        recipient = node_identifier,
        amount = 100,
        id = '1234567890'
        )
    block = blockchain.new_block(proof)


def genesis():
    gen = threading.Timer(3600, genesis)
    gen.daemon = True
    gen.start()

    req = urllib.request.urlopen('http://technoboy.pythonanywhere.com/chain').read()
    file = open('/Genesis.json','w')
    file.write(str(json.loads(req)))
    file.close()


def save_nodes():
    bs = threading.Timer(3600, bootstrap)
    bs.daemon = True
    bs.start()

    req = urllib.request.urlopen('http://technoboy.pythonanywhere.com/nodes/register').read()
    file = open('/Nodes.json','w')
    file.write(str(json.loads(req)['total_nodes']))
    file.close()
 

def save(request):
    genesis()
    bootstrap()
    return HttpResponse('Saved')


########################################################################
'''
if __name__ == '__main__':
    
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--p', '--port', default =5000, type =int ,help ='port to listen on')
    args = parser.parse_args()
    ports = args.port()

    app.run(host = '0.0.0.0', port = ports)
'''

# demomine()
# bootstrap()
# resolve()
blockchain.register_node('http://technoboy.pythonanywhere.com')
