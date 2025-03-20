import pytest

from domain.entities.model import City, ShowPlace, User, Visit
from domain.entities.place_types import PlaceType
from infra.repository.exceptions.user import UserAlreadyExistException
from infra.repository.exceptions.route_to_db import CityAlreadyExistException, CityNotFoundException, ShowPlaceAlreadyExistException, VisitAlreadyExistException
from infra.repository.clear_db import clear_all
from infra.repository.connect import _init_db
from infra.repository.entrypoint import add_city, add_show_place, add_user, add_visit, change_user_password, check_user_password


_init_db(is_test=True)

'''
Создание городов
'''
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

'''
Создание достопримечательностей
'''
def test_add_show_place():
    clear_all()
    city = City(name="Сургут", country="Россия")
    showplace = ShowPlace(name="ГРЭС", _place_type="Архитектурный", description="", latitude=0, longitude=0, city=city, addres="")
    _city = add_city(city)
    sp = add_show_place(showplace)
    assert city.is_generic_type() == sp.city.is_generic_type()

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


'''
Создание и редактирование пользователя
'''
def test_add_user():
    clear_all()
    user:User = User("MAX", "MAX")
    user_added = add_user(user, "12345")
    assert user.is_generic_type() == user_added.is_generic_type()


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


'''
Создание посещения достопримечательности пользователем
'''
def test_add_visit():
    clear_all()
    city = City("Сургут", "Россия")
    show_place = ShowPlace("ГРЭС", "Архитектурный", "", 0, 0, city, "")
    user = User("Max", "max")
    add_user(user, "111")
    add_city(city)
    add_show_place(show_place)
    add_visit(user_login=user.login, 
              show_place_name=show_place.name, 
              show_place_city=show_place.city.name,
              grade=5,
              review="Хорошее место")


def test_add_unique_visit():
    clear_all()
    city = City("Сургут", "Россия")
    show_place = ShowPlace("ГРЭС", "Архитектурный", "", 0, 0, city, "")
    user = User("Max", "max")
    add_user(user, "111")
    add_city(city)
    add_show_place(show_place)
    visit = Visit(
        user=user,
        show_place=show_place,
        grade=5,
        review="Хорошее место"
    )
    with pytest.raises(VisitAlreadyExistException):
        add_visit(user_login=user.login, 
              show_place_name=show_place.name, 
              show_place_city=show_place.city.name,
              grade=5,
              review="Хорошее место")
        add_visit(user_login=user.login, 
              show_place_name=show_place.name, 
              show_place_city=show_place.city.name,
              grade=5,
              review="Хорошее место")
