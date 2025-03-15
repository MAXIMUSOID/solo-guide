import pytest

from domain.entities.model import City, ShowPlace
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
    city = City(name="Сургут", country="Россия")
    add_city(city)

def test_add_unique_city():
    clear_all()
    city = City(name="Сургут", country="Россия")
    
    with pytest.raises(CityAlreadyExistException):
        add_city(city)
        add_city(city)

def test_add_show_place():
    clear_all()
    city = City(name="Сургут", country="Россия")
    showplace = ShowPlace(name="ГРЭС", _place_type="Архитектурный", description="", latitude=0, longitude=0, city=city, addres="")
    _city = add_city(city)
    sp = add_show_place(showplace)
    assert city == sp.city

def test_add_show_place_unique():
    clear_all()
    city = City(name="Сургут", country="Россия")
    _city = add_city(city)
    showplace = ShowPlace("ГРЭС", "Архитектурный", "", latitude=0, longitude=0, city=city, addres="")
    with pytest.raises(ShowPlaceAlreadyExistException):
        add_show_place(showplace)
        add_show_place(showplace)

def test_add_show_place_unnown_city():
    clear_all()
    with pytest.raises(CityNotFoundException):
        city=City("", "")
        showplace = ShowPlace("ГРЭС", PlaceType("Архитектурный"), "", latitude=0, longitude=0, city=city, addres="")
        add_show_place(showplace)