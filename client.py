#!/usr/bin/env python3
import argparse
import datetime
import os
from functools import partial

import prettytable
import requests


class WalletClientError(Exception):
    message = 'Что-то пошло не так :с'


class CommandNotFound(WalletClientError):
    message = 'Неизвестная команда'


class ServerNotResponding(WalletClientError):
    message = 'Сервер не отвечает'


class ServerError(WalletClientError):
    message = 'Ошибка сервера: {}'

    def __init__(self, error: str):
        self.message = self.message.format(error)


TRANACTION_HUMAN = {
    'income': 'Доход',
    'outcome': 'Расход',
}


class WalletClient:
    """
    url = "http://0.0.0.0:8080/"
    """

    def __init__(self, url: str):
        self.url = url

    def api_request(self, method: str = 'GET', path: str = '/', json=None):
        """
        GET /
        POST /add
        """
        try:
            response = requests.request(method, os.path.join(self.url, path.lstrip('/')), json=json)
            response.raise_for_status()
            data = response.json()
            assert 'error' not in data, data['error']
        except requests.exceptions.ConnectionError:
            raise ServerNotResponding
        except requests.HTTPError as e:
            raise ServerError(e.response.json()['error'])
        except AssertionError as e:
            raise ServerError(str(e))
        return data

    def get_balance(self):
        data = self.api_request()
        return data['balance']

    def get_transactions(self):
        return self.api_request()['transactions']

    def make_transaction(self, type: str, value: float, description: str = None):
        transaction_data = {'type': type, 'value': value}
        if description:
            transaction_data['description'] = description
        self.api_request('POST', '/add', json=transaction_data)
        return True


class CommandHandler:
    def __init__(self, client: WalletClient):
        self._client = client

    def balance(self):
        print(f'Ваш баланс: {self._client.get_balance():.2f}')

    def make_transaction(self, type: str, value: float, description: str = None):
        if self._client.make_transaction(type, value, description):
            print('Транзакция создана')

    def timeline(self, start: str = None, end: str = None):
        transactions = self._client.get_transactions()
        table = prettytable.PrettyTable(['Дата', 'Тип транзакции', 'Описание', 'Сумма'])
        for transaction in transactions:
            table.add_row([
                datetime.datetime.fromtimestamp(transaction['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                # даты
                TRANACTION_HUMAN[transaction['type']],  # тип транзацкии
                transaction.get('description') or '',  # тип транзацкии
                f'{transaction["value"]:.2f}' or '',  # тип транзацкии

            ])
        print(table)

    HANDLERS = {
        'balance': balance,
        'make_transaction': make_transaction,
        'timeline': timeline,
    }

    def get_handler(self, command: str):
        try:
            return partial(self.HANDLERS[command], self)
        except KeyError:
            raise CommandNotFound


def make_parser():
    """
    > ./client.py balance
    Your balance: 200.00

    > ./client.py timeline --start 2020-04-01
    # Таблица
    # Дата | Тип транзакции | описание | Сумма

    > ./client make_transaction --type income --description
    OK!
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', help='Адрес сервера', required=True)
    subparsers = parser.add_subparsers(title='command')
    balance_parser = subparsers.add_parser('balance', help='Получение текущего баланса')
    balance_parser.set_defaults(command='balance')

    timeline_parser = subparsers.add_parser('timeline', help='Получение текущего баланса')
    timeline_parser.set_defaults(command='timeline')
    timeline_parser.add_argument('--start', help='Начало периода выписки')
    timeline_parser.add_argument('--end', help='Конец периода выписки')

    make_parser = subparsers.add_parser('make_transaction', help='Создание новой транзации')
    make_parser.set_defaults(command='make_transaction')
    make_parser.add_argument('--type', '-t', default='outcome', help='Тип транзакции')
    make_parser.add_argument('--description', '-d', help='Описание транзации')
    make_parser.add_argument('value', type=float, help='Сумма транзакции')

    return parser


if __name__ == '__main__':
    parser = make_parser()
    config = parser.parse_args()
    try:
        params = dict(config._get_kwargs())
        command = params.pop('command')
        client = WalletClient(params.pop('url'))
        handler = CommandHandler(client)
        handler.get_handler(command)(**params)
    except WalletClientError as e:
        print(f'Ошибка: {e.message}')
        exit(1)
    # except Exception:
    #     print(f'Ошибка: {WalletClientError.message}')
    #     exit(1)
