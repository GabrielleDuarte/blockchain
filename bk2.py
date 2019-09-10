from hashlib import sha256
import json
from time import time
import copy
from bitcoin.wallet import CBitcoinSecret
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage

DIFFICULTY = 4 

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
        nonce = 0
        while self.isValidProof(prevBlock, nonce) is False:
            nonce += 1

        return nonce

    @staticmethod
    def isValidProof(block, nonce):
        block['nonce'] = nonce
        guessHash = Blockchain.getBlockID(block)
        return guessHash[:DIFFICULTY] == '0' * DIFFICULTY 

    @staticmethod
    def generateHash(data):
        blkSerial = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(blkSerial).hexdigest()

    @staticmethod
    def getBlockID(block):
        blockCopy = copy.copy(block)
        blockCopy.pop("transactions", None)
        return Blockchain.generateHash(blockCopy)

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
            print('Hash do ultimo bloco: ')
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

    @staticmethod
    def sign(privKey, m):
        secret = CBitcoinSecret(privKey)
        message = BitcoinMessage(m)
        return SignMessage(secret, message)
        
      
    @staticmethod
    def verifySignature(address, signature, m):
        message = BitcoinMessage(m)
        return VerifyMessage(address, message, signature)
    
    

# Teste
address = '1PVSAdiC61KdZ3YifgAPo2EfFmxVRoWF86'
privKey = 'Kyaewtn291GiUL2aEFcH3fuCjY9MHg7aT2L4QpfCBANyZkJfnoYs'

message = 'jkdfgdrhgfoshjrg'

signature = Blockchain.sign(privKey, message)
print('Assinatura gerada: {}'.format(signature))

print('Assinatura valida para mensagem e endereco indicado? {}'.format(Blockchain.verifySignature(address, signature, message)))

