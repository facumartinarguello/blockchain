'''Provide verification helper mothods'''
from .hash_util import hash_block, get_sha256


class Verification:

    @staticmethod
    def valid_proof(transactions, last_block_hash, proof, difficulty):
        '''Check amount of leading zerroes in hash
        Only after getting True inside this function
        new block will be added to the blockchain'''
        # IMPORTANT: Proof of Work should NOT INCLUDE REWARD TRANSACTION
        guess = str([tx.to_ordered_dict() for tx in transactions[:-1]]) + str(last_block_hash) + str(proof)
        guess_hash = get_sha256(guess)
        print('Verify nonce:', guess_hash)
        return guess_hash.startswith(difficulty)

    @classmethod
    def verify_chain(cls, blockchain, difficulty):
        '''Verify each block['previous_block_hash'] vith calculated hash_block() of previous block'''
        for previous_block, block in enumerate(blockchain[1:]):
            # Verify previous block hash
            print('erify chain > Verify previous block hash')
            if block.previous_hash != hash_block(blockchain[previous_block]):
                print('Previous block hash is invalid')
                return False
            # Verify PoW of current block
            print('Verify chain > Validate PoW')
            # if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.nonce, difficulty):
            if not cls.valid_proof(block.transactions, block.previous_hash, block.nonce, difficulty):
                print('Proof of Work is invalid')
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance):
        '''Verify sender ability to do transaction
        If balance >= tx_amount
        '''
        sender_balance = get_balance(transaction.sender)
        return sender_balance >= transaction.amount

    @staticmethod
    def verify_transactions(open_transactions, get_sender_balance, get_sender_transactions_coins):
        '''Verify ALL open transaction in pull'''

        # All participants(senders) in open transactions
        participants = set([tx.sender for tx in open_transactions])

        return all([
            get_sender_balance(participant) >= get_sender_transactions_coins(participant)
            for participant in participants
        ])
