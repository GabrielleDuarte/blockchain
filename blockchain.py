import hashlib
import json
from time import time
import copy

DIFFICULTY = 4 # Quantidade de zeros (em hex) iniciais no hash válido.

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.memPool = []
        self.createGenesisBlock()

    def createGenesisBlock(self):
        self.createBlock(previousHash='0'*64, nonce=0)
        self.mineProofOfWork(self.prevBlock) 

    def createBlock(self, nonce=0, previousHash=None):
        if (previousHash == None):
            previousBlock = self.chain[-1]
            previousBlockCopy = copy.copy(previousBlock)
            previousBlockCopy.pop("transactions", None)

        block = {
            'index': len(self.chain) + 1,
            'timestamp': int(time()),
            'transactions': self.memPool,
            'merkleRoot': '0'*64,
            'nonce': nonce,
            'previousHash': previousHash or self.generateHash(previousBlockCopy),
        }

        self.memPool = []
        self.chain.append(block)
        return block

    def mineProofOfWork(self, prevBlock):
        while (True):
            if(self.isValidProof(prevBlock, prevBlock["nonce"]+1)):
                break
        # TODO Implemente seu código aqui.
        # GERAR NONCE ATÉ SER VÁLIDO (TER 4 0 NO INÍCIO)

    @staticmethod
    def isValidProof(block, nonce):
        # TODO Implemente seu código aqui.
        block["nonce"] = nonce # acessar atributos de um objeto 
        hash=Blockchain.getBlockID(block)
        if( hash[:DIFFICULTY] == DIFFICULTY*"0"):
            return True
        return False


        #  if (Blockchain.getBlockID(block)[:DIFFICULTY] == DIFFICULTY*'0'):
        #     return True
        # return False
        # for block["nonce"] in "python":

        # if (block["nonce"] == '0000')


        #gerar hash testar se  começa com 4 0 
    @staticmethod
    def generateHash(data):
        #GERA UM HASH A PARTIR DO BLOCO 
        blkSerial = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(blkSerial).hexdigest()

    @staticmethod
    def getBlockID(block):
        # TODO Implemente seu código aqui. Passa o bloco e retorna o rash do bloco
        
        newblock = copy.copy(block)
        newblock.pop("transactions", None)

        return Blockchain.generateHash(newblock) 

    def printChain(self):
          for block in self.chain:
            print('--------------------------------------------------------------------')
            previousBlock = copy.copy(block)
            del(previousBlock["transactions"])
            previousHash = self.generateHash(previousBlock)
            print(previousHash)
            print('*********')
            print('Indice: ')
            print(block['index'])
            print('*********')
            print('timestamp: ')
            print(block['timestamp'])
            print('*********')
            print('nonce')
            print(block['nonce'])
            print('*********')
            print('merkleRoot')
            print(block['merkleRoot'])
            print('*********')
            print('Hash do último bloco: ')
            print(block['previousHash'])
            print('[|]')
            print(' | ')
            print(' | ')
            print(' | ')
            print(' | ')
            print('[|]')


    @property
    def prevBlock(self):
        return self.chain[-1]

# Teste
blockchain = Blockchain()
for x in range(0, 4): 
    blockchain.createBlock()
    blockchain.mineProofOfWork(blockchain.prevBlock)

for x in blockchain.chain :
    print('[Bloco #{} : {}] Nonce: {} | É válido? {}'.format(x['index'], Blockchain.getBlockID(x), x['nonce'], Blockchain.isValidProof(x, x['nonce'])))