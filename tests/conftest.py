import json
import os

import pytest

from my_wallet.storage import FileStorage


@pytest.fixture
def file_storage():
    filename = 'tests/storage.json'
    content = []
    with open(filename, mode='w+') as f:
        json.dump(list(content), f)
    storage = FileStorage(filename)
    yield storage

    if os.path.exists(storage.filename):
        os.unlink(storage.filename)


@pytest.fixture(scope='session')
def transactions():
    return [
        {'type': 'income', 'description': None, 'value': 100.0, 'timestamp': 0, },
        {'type': 'income', 'description': None, 'value': 100.0, 'timestamp': 1, },
    ]