import json

import pytest


def test_storage_load_non_empty1(file_storage):
    assert file_storage.load() == []


@pytest.mark.parametrize(
    "data, exc",
    [
        ([], []),
        (
            pytest.lazy_fixture("transactions"),
            pytest.lazy_fixture("transactions"),
        ),
    ],
)
def test_storage_save(file_storage, data, exc):
    file_storage.save(data)
    with open(file_storage.filename) as f:
        assert json.load(f) == exc
