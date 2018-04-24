#!/usr/bin/env python
import hashlib
import datetime
import json
import string
import random
import sys


sys.setrecursionlimit(10000)


class Block:
    """
        this class create a block object
    """

    def __init__(self, index, timestamp, data, prev_hash, prev=None):
        self.index = index
        self.data = data
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.hash = self.hashing()
        self.prev = prev


    def hashing(self):
        """
            create block hash
        """
        sha = hashlib.sha256()
        blockString = "%s%s%s%s" % (self.index, self.data, self.timestamp, self.prev_hash)
        sha.update(blockString)
        return sha.hexdigest()

    def __repr__(self):
        return "Object ID {index} received on {timestamp} with hash {hash} and data {data}".format(
            index=self.index,
            timestamp=str(self.timestamp).replace(' ','T'),
            hash=self.hash,
            data=self.data
        )


class BlockChain:

    chain = []

    def __init__(self):
        self.generate_first_block()

    def generate_first_block(self):
        timestamp = str(datetime.datetime.now()).replace(' ', 'T')
        block = Block(0, timestamp, "{}", "0")
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1]

    def get_random_string(self, length=32):
        st = "%s%s%s" % (string.ascii_uppercase, string.digits, '$-')
        return ''.join(random.SystemRandom().choice(st) for k in range(length))

    def new_block(self, data):
        previous = self.get_last_block()
        index = previous.index + 1
        timestamp = str(datetime.datetime.now()).replace(' ', 'T')
        hash = previous.hash
        block = Block(index, timestamp, data, hash, prev=previous)
        self.chain.append(block)
        return block

    def mining(self):
        r = hashlib.sha256(self.get_random_string()).hexdigest()
        if r.startswith('00'):
            return self.new_block({"proof" : r})
        return self.mining()

    def printChain(self):
        return [str(x) for x in self.chain]

    def searchBlock(self, hash=None, index=None):
        if index:
            return self.chain[index]
        if hash:
            for k in self.chain:
                if k.hash == hash:
                    return k

        raise Exception("block not found")

    def validate(self):
        prev_hash = None
        if len(chain.chain) > 0:
            for k in self.chain:
                if not prev_hash:
                    prev_hash = k.hash
                else:
                    assert k.prev_hash == prev_hash, "chain is corrupted"
            return True
        return False

