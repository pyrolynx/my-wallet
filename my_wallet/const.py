import enum
from typing import Type, Union


class TransactionType(enum.Enum):
    income = 'income'
    outcome = 'outcome'

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)

    def __str__(self):
        return self.value

    @classmethod
    def check(cls, value: str, error: Union[Type[Exception], Exception] = ValueError):
        try:
            return cls(value)
        except ValueError:
            raise error

    @classmethod
    def to_json(cls, value):
        if isinstance(value, cls):
            return str(value)
        return value
