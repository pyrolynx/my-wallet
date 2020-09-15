import time
from unittest import TestCase, mock
import os.path

from my_wallet.const import TransactionType
from my_wallet.storage import FileStorage
from my_wallet.manager import Transaction, TransactionManager


class TestTransactionManager(TestCase):
    def setUp(self) -> None:
        self.storage = FileStorage('tests/test_transactions.json')
        self.storage.save([])
        self.manager = TransactionManager(self.storage)

    def tearDown(self) -> None:
        if os.path.exists(self.storage.filename):
            os.unlink(self.storage.filename)

    def test_summary(self):
        self.assertEqual(self.manager.summary, {'transactions': [], 'balance': 0.0})

        transaction = Transaction(time.time(), TransactionType.income, 100.0)
        self.storage.save([transaction])
        self.manager.load_transactions()
        self.assertEqual(self.manager.summary, {'transactions': [dict(transaction)], 'balance': 100.0})