import time
from typing import List, Union

from my_wallet import const
from my_wallet.storage import AbstractStorage


class Transaction(dict):
    def __init__(
        self, timestamp: float, type: Union[str, const.TransactionType], value: float, description: str = None,
    ):
        super().__init__(timestamp=timestamp, type=const.TransactionType(type), value=value, description=description)

    @property
    def type(self) -> const.TransactionType:
        return self['type']

    @property
    def value(self):
        return self['value']

    @property
    def description(self):
        return self['description']


class TransactionManager:
    TRANSACTIONS_TYPE = ['income', 'outcome']

    def __init__(self, storage: AbstractStorage):
        self.transactions: List[Transaction] = []
        self.storage = storage

    def add_transaction(self, type: const.TransactionType, value: float, **data):
        data['timestamp'] = data.pop('timestamp', time.time())
        self.transactions.append(Transaction(type=type, value=value, **data))
        self.save_transactions()

    def load_transactions(self):
        transaction_data = self.storage.load()
        for data in transaction_data:
            self.transactions.append(Transaction(**data))

    def save_transactions(self):
        self.storage.save(self.transactions)

    @property
    def summary(self):
        return {
            'transactions': self.transactions,
            'balance': sum(x.value for x in self.transactions if x.type == 'income') - \
                       sum(x.value for x in self.transactions if x.type == 'outcome')
        }

