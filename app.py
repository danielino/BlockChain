#!/usr/bin/env python

from flask import Flask, jsonify, request
from blockchain.BlockChain import Block, BlockChain

app = Flask(__name__)

@app.route("/")
def index():
    if chain:
        return jsonify(chain.printChain())
    return jsonify({})


@app.route("/make_block")
def make_block():
    if chain:
        data = request.args.get('data')
        ret = chain.new_block(data)
        print ret.prev
        return jsonify(str(ret))


@app.route("/search/id/<int:id>")
def search_by_id(id):
    if chain:
        return chain.searchBlock(index=id)


@app.route("/search/hash/<string:hash>")
def search_by_hash(hash):
    if chain:
        return chain.searchBlock(hash=hash)


@app.route("/validate")
def validate():
    if chain:
        chain.validate()
        return jsonify({"result" : "success", "chain_status" : "consistent"})
    return jsonify({})


if __name__ == "__main__":
    chain = BlockChain()
    app.run(host="0.0.0.0", debug=True)
    
