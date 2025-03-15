import pytest

from domain.exceptions.model import CityCountryToLongException, CityEmptyCountryException, CityEmptyNameException, CityNameToLongException, PlaceTypeNotFoundException, ShowPlaceEmptyNameException, ShowPlaceNameToLongException
from domain.entities.model import City, ShowPlace


def test_create_city():
    city = City("Сургут", "Россия")


def test_empty_name_city():
    with pytest.raises(CityEmptyNameException):
        city = City("", "Россия")


def test_empty_country_name_city():
    with pytest.raises(CityEmptyCountryException):
        city = City("Сургут", "")


def test_long_name_city():
    with pytest.raises(CityNameToLongException):
        city = City("a"*256, "1")
    

def test_long_country_name_city():
    with pytest.raises(CityCountryToLongException):
        city = City("a", "1"*256)


def test_create_show_place():
    city = City("Сургут", "Россия")
    show_place = ShowPlace("ГРЭС", "Архитектурный", "", 0, 0, city, "")
    assert show_place.city == city


def test_empty_name_show_place():
    with pytest.raises(ShowPlaceEmptyNameException):
        city = City("1", "Россия")
        show_place = ShowPlace("", "Архитектурный", "", 0, 0, city, "")


def test_name_to_long_show_place():
    with pytest.raises(ShowPlaceNameToLongException):
        city = City("1", "Россия")
        show_place = ShowPlace("Г"*256, "Архитектурный", "", 0, 0, city, "")

def test_place_type_not_found():
    with pytest.raises(PlaceTypeNotFoundException):
        city = City("Сургут", "Россия")
        show_place = ShowPlace("ГРЭС", "Архитектурный1", "", 0, 0, city, "")