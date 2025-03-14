import pytest

from infra.repository.show_place import add_city


def test_add_city():
    add_city(name="Сургут", country="Россия")