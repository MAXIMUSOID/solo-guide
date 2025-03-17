from datetime import datetime
import pytest

from domain.exceptions.model import (CityCountryToLongException, 
                                     CityEmptyCountryException, 
                                     CityEmptyNameException, 
                                     CityNameToLongException, 
                                     PlaceTypeNotFoundException, 
                                     ShowPlaceEmptyNameException, 
                                     ShowPlaceNameToLongException, 
                                     UserLoginEmptyException, 
                                     UserLoginToLongException, 
                                     UserNicknameEmptyException, 
                                     UserNicknameToLongException, VisitEmptyShowPlaceException, VisitEmptyUserException, VisitGradeIncorrectException, VisitReviewToLongException,
                                     )
from domain.entities.model import City, ShowPlace, User, Visit


'''
Тестирование создания города
'''
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


'''
Тестирование создания достопримечательности
'''
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


'''
Тестирование создания пользователя
'''
def test_create_user():
    user = User("Max", "max")

def test_empty_nickname():
    with pytest.raises(UserNicknameEmptyException):
        user = User("", "max")

def test_to_long_nickname():
    with pytest.raises(UserNicknameToLongException):
        user = User("1"*256, "max")

def test_empty_login():
    with pytest.raises(UserLoginEmptyException):
        user = User("12", "")

def test_to_long_login():
    with pytest.raises(UserLoginToLongException):
        user = User("1", "m"*256)


'''
Тестирование создание информации о визите достопримечательности пользователем
'''
def test_add_visit():
    city = City("Сургут", "Россия")
    show_place = ShowPlace("ГРЭС", "Архитектурный", "", 0, 0, city, "")
    user = User("Max", "max")
    visit = Visit(
        user=user,
        show_place=show_place,
        grade=5,
        review="Хорошее место"
    )
    assert visit.create_at.date() == datetime.now().date()


def test_visit_empty_user():
    city = City("Сургут", "Россия")
    show_place = ShowPlace("ГРЭС", "Архитектурный", "", 0, 0, city, "")

    with pytest.raises(VisitEmptyUserException):
        visit = Visit(
        user=None,
        show_place=show_place,
        grade=5,
        review="Хорошее место"
    )
        

def test_visit_empty_show_place():
    user = User("Max", "max")
    city = City("Сургут", "Россия")
    show_place = ShowPlace("ГРЭС", "Архитектурный", "", 0, 0, city, "")

    with pytest.raises(VisitEmptyShowPlaceException):
        visit = Visit(
        user=user,
        show_place=None,
        grade=5,
        review="Хорошее место"
    )
        

def test_visit_incorrect_grade():
    user = User("Max", "max")
    city = City("Сургут", "Россия")
    show_place = ShowPlace("ГРЭС", "Архитектурный", "", 0, 0, city, "")

    with pytest.raises(VisitGradeIncorrectException):
        visit = Visit(
        user=user,
        show_place=show_place,
        grade=-1,
        review="Хорошее место"
    )
        
    with pytest.raises(VisitGradeIncorrectException):
        visit = Visit(
        user=user,
        show_place=show_place,
        grade=6,
        review="Хорошее место"
    )
        

def test_add_visit():
    city = City("Сургут", "Россия")
    show_place = ShowPlace("ГРЭС", "Архитектурный", "", 0, 0, city, "")
    user = User("Max", "max")
    with pytest.raises(VisitReviewToLongException):
        visit = Visit(
            user=user,
            show_place=show_place,
            grade=5,
            review="1"*256
        )