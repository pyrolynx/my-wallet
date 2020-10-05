import enum
import json
from typing import Any, Type, Union


class EnumEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        v = o
        if isinstance(o, enum.Enum):
            return o.value
        return super().default(v)


class TransactionType(enum.Enum):
    income = "income"
    outcome = "outcome"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)

    def __str__(self):
        return self.value

    @classmethod
    def check(
        cls, value: str, error: Union[Type[Exception], Exception] = ValueError
    ):
        try:
            return cls(value)
        except ValueError:
            raise error
