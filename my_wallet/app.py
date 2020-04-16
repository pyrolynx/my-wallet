from flask import Flask, redirect, request, jsonify, abort

import datetime

import config
from my_wallet.storage import FileStorage
from my_wallet.manager import TransactionManager

app = Flask(__package__)

manager = TransactionManager(storage=FileStorage(config.FILE_STORAGE))
manager.load_transactions()


@app.route('/', methods=['GET'])
def index():
    return jsonify(manager.summary)


@app.route('/add', methods=['POST'])
def add_transactions():
    if not request.is_json:
        return abort(400, 'json expected')
    data = request.get_json()
    manager.add_transaction(timestamp=datetime.datetime.now().timestamp(), type=data['type'],
                            value=data['value'],
                            description=data['description'])
    return redirect('/')
