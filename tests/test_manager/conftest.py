import pytest
from my_wallet.manager import TransactionManager, Transaction


@pytest.fixture(scope='module')
def transaction():
    return Transaction(timestamp=0, type='income', value=100)
