import pytest

from domain.entities.place_types import PlaceType
from infra.repository.exceptions.route_to_db import CityAlreadyExistException, CityNotFoundException, ShowPlaceAlreadyExistException
from infra.repository.clear_db import clear_all
from infra.repository.connect import _init_db
from infra.repository.show_place import add_city, add_show_place

from pathlib import Path

import environ

_init_db(is_test=True)
def test_add_city():
    clear_all()
    add_city(name="Сургут", country="Россия")

def test_add_unique_city():
    clear_all()
    with pytest.raises(CityAlreadyExistException):
        add_city(name="Сургут", country="Россия")
        add_city(name="Сургут", country="Россия")

def test_add_show_place():
    clear_all()
    city = add_city(name="Сургут", country="Россия")
    showplace = add_show_place("ГРЭС", PlaceType("Архитектурный"), "", latitude=0, longitude=0, city_name="Сургут", addres="")
    assert city == showplace.city

def test_add_show_place_unique():
    clear_all()
    city = add_city(name="Сургут", country="Россия")
    with pytest.raises(ShowPlaceAlreadyExistException):
        showplace = add_show_place("ГРЭС", PlaceType("Архитектурный"), "", latitude=0, longitude=0, city_name="Сургут", addres="")
        showplace = add_show_place("ГРЭС", PlaceType("Архитектурный"), "", latitude=0, longitude=0, city_name="Сургут", addres="")

def test_add_show_place_unnown_city():
    clear_all()
    with pytest.raises(CityNotFoundException):
        add_show_place("ГРЭС", PlaceType("Архитектурный"), "", latitude=0, longitude=0, city_name="Сургут", addres="")