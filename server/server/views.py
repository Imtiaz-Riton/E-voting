from django.http import JsonResponse
from rest_framework.decorators import api_view
from time import time, sleep
import json
import csv
from hashlib import *
from .enc import *
from .aes import *
import pickle



DIFFICULTY = 3

#frequency of mining of blocks seconds
BLOCK_TIME_LIMIT = 20

#--path of project files
PROJECT_PATH = "/home/s6088/Desktop/RSN/server"

EVoting = Blockchain()

class vote:
    count = 0

    def __init__(self, hiddenvoterid, candidateID, voterpubkey):
        #--voterid hashed with PIN (ZKP)
        self.hiddenvoterid = hiddenvoterid
        self.candidate = candidateID
        self.voterpubkey = voterpubkey
        self.time = time()
        self.votedata = [self.hiddenvoterid, self.candidate, self.time]


    #--returns the voter's public key in pickle object as a byte value
    def get_voter_pk(self):
        return self.voterpubkey


    #--vote gets a digital signature by voter's private key and gets signed by admin public key
    def encryptvote(self):
        """
        the data of the vote (in the votedata list) will be first hashed by SHA-256
        and then, the data will be converted into bytes and signed by voter's private key
        and that hashed signature will be appended with votedata itself
        """
        
        self.votedata.append(enc_sign(voterkeys['sk'], bytes(sha256(str('---'.join(str(x) for x in self.votedata)).encode('utf-8')).hexdigest(),'utf-8')))
        #print(self.votedata)
        """
        now that whole data (the new votedata list) will be encrypted by AES encryption
        and the shared key of AES will be encrypted with admin's public key
        this data will be broadcasted and saved into the unconfirmed votepool and will be added in the block
        """
        

        voterpk = self.get_voter_pk().export_key()

        #--byte value of voter public key pickle object is converted to string
        #--then added to list
        return [str(voterpk)[2:-1], str(aes_encrypt('***'.join(str(i) for i in self.votedata),voterkeys['aeskey']))[2:-1], str(enc_encrypt(Blockchain.adminpub,voterkeys['aeskey']))[2:-1]]

    #--keep track of no. of votes
    @classmethod
    def inc_votecount(cls):
        cls.count+=1

    @classmethod
    def get_votecount(cls):
        #--return the current number of votes
        return cls.count


class Blockchain:

    #--holds the info of chain of blocks as objects
    chain = []
    adminpriv , adminpub = enc_rsakeys()
    #--administrator public/private key pair generated along with the blockchain initialization.
    #--the public key of admin will be used to encrypt the vote data for confidentiality
    with open('temp/Adminkeys.txt', 'wb') as adminkeyfile:
        pickle._dump(adminpriv, adminkeyfile)
        pickle._dump(adminpub, adminkeyfile)

    def __init__(self):
        self.addGenesis()
        print('Blockchain initialized')

    @staticmethod
    #--genesis block creation has nothing to do with blockchain class,
    #--..but has to be created when blockchain is initialized
    def genesis():

        #--genesis block created
        gen = Block(0,"Let the real democracy rule!!",0, sha256(str("Let the real democracy rule!!").encode('utf-8')).hexdigest(), DIFFICULTY, time(),'',0,'Errrrrorrr')
        return gen


    @staticmethod
    def addGenesis():
        genesisblock = Blockchain.genesis()

        #--find the proof of work for genesis block
        genesisblock.nonce = genesisblock.pow()
        genesisblock.hash = genesisblock.calcHash()
        Blockchain.chain.append(genesisblock)

        #--information of genesis block written to the blockchain data file
        with open('temp/Blockchain.dat', 'ab') as genfile:
            pickle._dump(genesisblock, genfile)
        print("Genesis block added")


    @staticmethod
    def display():
        #--print the information of blocks of the blockchain in the console
        try:
            with open('temp/Blockchain.dat','rb') as blockfile:
                for block in range(len(EVoting.chain)):
                    data = pickle._load(blockfile)

                    #--print all data of a block
                    print("Block Height: ", data.height)
                    print("Data in block: ", data.data)
                    print("Number of votes: ",data.number_of_votes)
                    print("Merkle root: ", data.merkle)
                    print("Difficulty: ", data.DIFFICULTY)
                    print("Time stamp: ", data.timeStamp)
                    print("Previous hash: ", data.prevHash)
                    print("Block Hash: ", data.hash)
                    print("Nonce: ", data.nonce, '\n\t\t|\n\t\t|')

        except FileNotFoundError:
            print("\n.\n.\n.\n<<<File not found!!>>>")


    @staticmethod
    #--to clear up the votepool after a block has been mined...
    def update_votepool():
        try:
            votefile = open('temp/votefile.csv','w+')
            votefile.close()

        except Exception as e:
            print("Some error occured: ", e)
        return "Done"

    #--to check if whether the data pool has some data or not
    def is_votepool_empty(self):

    #--path to votefile
        my_path = PROJECT_PATH + '/temp/votefile.csv'

    #--will return true if file exists and has no data
        if os.path.isfile(os.path.expanduser(my_path)) and os.stat(os.path.expanduser(my_path)).st_size==0:
            return True

    #--False otherwise
        return False


    """
    After regular intervals, we need to verify that the blockchain
    is indeed valid at all points. And no data has been tampered - EVEN IN ONE SINGLE COPY
    (if not for the whole network).
    We do that by verifying the chain of block hashes.
    """
    @classmethod
    def verify_chain(cls):
        index, conclusion = ver.sync_blocks(cls.chain)
        if not conclusion:
            if len(str(index))==1:
                error_msg ="""+-----------------------------------------+
                            |                                         |
                            | Somebody messed up at Block number - {}  |
                            |                                         |
                            +-----------------------------------------+""".format(index)

            else:
                error_msg ="""+-----------------------------------------+
                            |                                         |
                            | Somebody messed up at Block number - {} |
                            |                                         |
                            +-----------------------------------------+""".format(index)

            raise Exception(error_msg)

        return True


class Block:

    """
    The basic structure of block that will be created when the block is generated
    the data in the block will be updated later and block will be mined then.
    """

    def __init__(self,height = 0,data = 'WARNING = SOME ERROR OCCURED',votes = 0,merkle = '0',DIFFICULTY = 0,time = 0,prevHash = '0',pow=0, hash = 'ERROR'):
        self.height = height                    #len(Blockchain.chain-1)
        self.data = data                        #loadvote()
        self.number_of_votes = votes            #votecount per block
        self.merkle = merkle                    #calculateMerkleRoot()
        self.DIFFICULTY = DIFFICULTY            #cryptography difficulty
        self.timeStamp = time                   #time()
        self.prevHash = prevHash                #previous block hash
        self.nonce = pow                        #proof of work function will find nonce
        self.hash = hash                        #hash of the current block

    #--The HEART OF BLOCKCHAIN - 'Proof-of-Work' function
    def pow(self,zero=DIFFICULTY):
        self.nonce=0
        while(self.calcHash()[:zero]!='0'*zero):
            self.nonce+=1
        return self.nonce

    #--calculate hash of a given block
    def calcHash(self):
        return sha256((str(str(self.data)+str(self.nonce)+str(self.timeStamp)+str(self.prevHash))).encode('utf-8')).hexdigest()

    """
    the vote data from the temporary pool will be loaded into the block
    and after successful loading of data, the pool will be cleared and
    will be reset for the next bunch of transactions
    """

    @staticmethod
    def loadvote():
        votelist = []
        votecount = 0
        try:
            with open('temp/votefile.csv', mode = 'r') as votepool:
                csvreader = csv.reader(votepool)
                for row in csvreader:
                    votelist.append({'Voter Public Key':row[0], 'Vote Data':row[1],'Key':row[2]})
                    votecount+=1
            return votelist,votecount

        except(IOError,IndexError):
            pass

        finally:
            print("data loaded in block")
            print("Updating unconfirmed vote pool...")
            print (Blockchain.update_votepool())


    #--create a merkle tree of vote transactions and return the merkle root of the tree
    def merkleRoot(self):
        return 'congrats'

    #--fill the block with data and append the block in the blockchain
    def mineblock(self):
        self.height = len(Blockchain.chain)                 #len(Blockchain.chain-1)
        self.data,self.number_of_votes = self.loadvote()    #loadvote() and return number of votes in current block
        self.merkle = self.merkleRoot()                     #MerkleRoot()
        self.DIFFICULTY = DIFFICULTY                        #DIFFICULTY for the cryptographic puzzle
        self.timeStamp = time()                             #time()
        self.prevHash = Blockchain.chain[-1].calcHash()     #Calculate the hash of previous
        self.nonce = self.pow()                             #Calculate nonce
        self.hash = self.calcHash()                         #compute hash of current block
        Blockchain.chain.append(self)

        return self     #--return block object



voterlist = [] 
invisiblevoter = ''
voterkeys = {}

@api_view(['POST'])
def sign_in(request):
    payload = json.loads(request.body)
    voterid = payload["voterid"]
    pin = payload["password"]
    voterkeys['pin'] = pin
    voterkeys['aeskey'] = aes_get_private_key(voterid)
    global invisiblevoter
    invisiblevoter = str(sha256((str(voterid)+str(pin)).encode('utf-8')).hexdigest())
    if voterid not in voterlist:
        voterlist.append(voterid)
        with open('temp/VoterID_Database.txt', 'a') as voterdata:
            voterdata.write(str(sha256(str(voterid).encode('utf-8')).hexdigest()))
            voterdata.write("\n")
        return JsonResponse({'success' : True, 'status': 'ok'})
    else:
        return JsonResponse({'success' : False, 'status': 'already voted'})



@api_view(['POST'])
def voter(request):
    payload = json.loads(request.body)
    choice = payload["candidate"]
    voterkeys['sk'], voterkeys['pk'] = enc_rsakeys()   
    v1 = vote(invisiblevoter, choice, voterkeys['pk'])
    vote.inc_votecount()
    
    with open('temp/votefile.csv','a',newline="") as votefile:
        writer = csv.writer(votefile)
        encvotedata = v1.encryptvote()
        writer.writerow(encvotedata)


    if vote.count%2==0:
        blockx = Block().mineblock()
        with open('temp/blockchain.dat','ab') as blockfile:
            pickle._dump(blockx, blockfile)

    return JsonResponse({'success' : True, 'status': 'thanks for vote!'})