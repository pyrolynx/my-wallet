import functools

from flask import Flask, jsonify, redirect, request

import config
from my_wallet import const, errors, utils
from my_wallet.manager import TransactionManager
from my_wallet.storage import FileStorage

app = Flask(__package__)

manager = TransactionManager(storage=FileStorage(config.FILE_STORAGE))
manager.load_transactions()


def json_api(func):
    @functools.wraps(func)
    def wrapper():
        try:
            if request.method == "POST" and not request.is_json:
                raise errors.InvalidContent
            return func()
        except errors.APIError as e:
            return jsonify({"error": e.message}), e.http_code
        except Exception as e:
            print(f"{type(e)}: {e}")
            return jsonify({"error": "unhandled server error"}), 500

    return wrapper


@app.route("/", methods=["GET"])
@json_api
def index():
    return jsonify(manager.summary)


@app.route("/add", methods=["POST"])
@json_api
def add_transactions():
    data = request.get_json()

    try:
        assert "type" in data, "type"
        assert "value" in data, "value"
    except AssertionError as e:
        raise errors.MissingArgument(str(e))

    transaction_type = const.TransactionType.check(
        data["type"], errors.InvalidArgument("type")
    )
    try:
        data["value"] = float(data["value"])
    except AssertionError:
        raise errors.InvalidArgument("type")
    except ValueError:
        raise errors.InvalidArgument("value")

    manager.add_transaction(
        timestamp=utils.now_timestamp(),
        type=transaction_type,
        value=data["value"],
        description=data.get("description"),
    )
    return redirect("/")
