import pytest

from domain.entities.model import City, ShowPlace, User
from domain.entities.place_types import PlaceType
from infra.repository.exceptions.user import UserAlreadyExistException
from infra.repository.exceptions.route_to_db import CityAlreadyExistException, CityNotFoundException, ShowPlaceAlreadyExistException
from infra.repository.clear_db import clear_all
from infra.repository.connect import _init_db
from infra.repository.entrypoint import add_city, add_show_place, add_user, change_user_password, check_user_password


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
        city=City("1", "1")
        showplace = ShowPlace(name="ГРЭС", _place_type="Архитектурный", description="", latitude=0, longitude=0, city=city, addres="")
        add_show_place(showplace)

def test_add_user():
    clear_all()
    user:User = User("MAX", "MAX")
    user_added = add_user(user, "12345")
    assert user == user_added

def test_add_unique_user():
    clear_all()
    with pytest.raises(UserAlreadyExistException):
        user:User = User(nickname="MAX", login="MAX")
        user_added = add_user(user, "12345")
        user_added = add_user(user, "12345")


def test_check_password():
    clear_all()
    user:User = User(nickname="MAX", login="MAX")
    user_added = add_user(user, "12345")

    assert check_user_password(user_added, "12345")

def test_change_password():
    clear_all()
    user:User = User(nickname="MAX", login="MAX")
    user_added = add_user(user, "12345")

    assert check_user_password(user_added, "12345")
    change_user_password(user, "asd")

    assert check_user_password(user, "asd")
