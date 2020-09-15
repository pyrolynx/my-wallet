import time
from unittest import TestCase, mock
import os.path

from my_wallet.const import TransactionType
from my_wallet.storage import FileStorage, AbstractStorage
from my_wallet.manager import Transaction, TransactionManager


class TestCaseWithFileStorage(TestCase):
    storage: AbstractStorage

    def setUp(self) -> None:
        super().setUp()
        self.storage = FileStorage('tests/test_transactions.json')
        self.storage.save([])

    def tearDown(self) -> None:
        if os.path.exists(self.storage.filename):
            os.unlink(self.storage.filename)
        super().tearDown()


class TestTransactionManager(TestCaseWithFileStorage):
    def setUp(self) -> None:
        super().setUp()
        self.manager = TransactionManager(self.storage)

    def test_summary(self):
        self.assertEqual(self.manager.summary, {
            'transactions': [],
            'balance': 0.0,
        })

        transaction = Transaction(time.time(), TransactionType.income, 100.0)
        self.storage.save([transaction])
        self.manager.load_transactions()
        self.assertGreaterEqual(self.manager.summary['balance'], 100)
        self.assertEqual(self.manager.summary, {
            'transactions': [dict(transaction)],
            'balance': 100.0
        })

    @mock.patch('time.time', return_value=time.time())
    def test_add_transaction(self, time_mock):
        self.assertEqual(self.manager.summary, {
            'transactions': [],
            'balance': 0.0,
        })
        values_set = [{'value': 50}, {'value': -50}, {'value': 0}]

        for values in values_set:
            with self.subTest('test_value', **values):
                self.manager.add_transaction(
                    type=TransactionType.income,
                    value=values['value'],
                    description='На пиво',
                )
                self.assertEqual(
                    self.manager.transactions[-1],
                    Transaction(timestamp=time.time(), value=values['value'], description='На пиво', type='income'),
                )
        print(self.manager.transactions)
