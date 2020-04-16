import abc
import json
import os


class AbstractStorage(abc.ABC):
    def load(self):
        raise NotImplementedError

    def save(self, data):
        raise NotImplementedError


class FileStorage(AbstractStorage):
    def __init__(self, filename: str):
        self.filename = filename

    def _check_file_exists(self):
        if not os.path.exists(self.filename):
            self.save([])

    def load(self):
        self._check_file_exists()
        with open(self.filename, 'r+') as f:
            return json.load(f)

    def save(self, data):
        with open(self.filename, 'w+') as f:
            json.dump(data, f)
