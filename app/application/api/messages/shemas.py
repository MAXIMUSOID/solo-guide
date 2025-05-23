from datetime import datetime
from typing import List
from pydantic import BaseModel

from domain.entities.model import City, ShowPlace, User, Visit


class CreateCityRequestSchema(BaseModel):
    name:str
    country:str


class CreateCityResponceSchema(BaseModel):
    name:str
    country:str

    @classmethod
    def from_entity(cls, city: City) -> 'CreateCityResponceSchema':
        return CreateCityResponceSchema(
            name=city.name,
            country=city.country
        )
    
class GetAllCitiesResponceSchema(BaseModel):
    cities:list[City]

    @classmethod
    def from_entity(cls, cities:list[City]) -> 'GetAllCitiesResponceSchema':
        return GetAllCitiesResponceSchema(
            cities=cities
        )
    

class CreateShowPlaceRequestShema(BaseModel):
    name:str
    place_type:str
    description:str
    latitude:float
    longitude:float
    city_name:str
    addres:str

class CreateShowPlaceResponceShema(BaseModel):
    name:str
    place_type:str
    description:str
    latitude:float
    longitude:float
    city:City

    @classmethod
    def from_entity(cls, showplace: ShowPlace) -> 'CreateShowPlaceResponceShema':
        return CreateShowPlaceResponceShema(
            name=showplace.name,
            place_type=showplace.place_type,
            description=showplace.description,
            latitude=showplace.latitude,
            longitude=showplace.longitude,
            city=showplace.city
        )
    

class GetShowPlacesToCityRequestSchema(BaseModel):
    city_name:str
    

class GetShowPlacesToCityResponceSchema(BaseModel):
    show_places:List[ShowPlace]

    @classmethod
    def from_entity(cls, show_places:list[ShowPlace]) -> 'GetShowPlacesToCityResponceSchema':
        return GetShowPlacesToCityResponceSchema(
            show_places=show_places
        )

class CreateUserRequestSchema(BaseModel):
    nickname:str
    login:str
    password:str


class CreateUserResponceSchema(BaseModel):
    nickname:str
    login:str
    oid:int

    @classmethod
    def from_entity(cls, user: User) -> 'CreateUserResponceSchema':
        return CreateUserResponceSchema(
            nickname=user.nickname,
            login=user.login,
            oid=user.oid
        )
    
class LoginUserRequestSchema(BaseModel):
    login:str
    password:str


class LoginUserResponceShcema(BaseModel):
    nickname:str
    login:str
    oid:int
    token:str

    @classmethod
    def from_entity(cls, user: User, token:str) -> 'LoginUserResponceShcema':
        return LoginUserResponceShcema(
            nickname=user.nickname,
            login=user.login,
            oid=user.oid,
            token=token
        )
    
class ChangePasswordRequestSchema(BaseModel):
    user_login:str
    password:str


class ChangePasswordResponceSchema(BaseModel):
    user:User

    @classmethod
    def from_entity(cls, user:User) -> 'ChangePasswordResponceSchema':
        return ChangePasswordResponceSchema(
            user=user
        ) 
    

class CreateVisitRequestSchema(BaseModel):
    user_login:str
    show_place_name:str
    show_place_city:str
    grade:int
    review:str

class CreateVisitResponceSchema(BaseModel):
    user_login:str
    show_place_name:str
    show_place_city_name:str
    grade:int
    review:str
    created_at:datetime
    
    @classmethod
    def from_entity(cls, visit: Visit) -> 'CreateVisitResponceSchema':
        return CreateVisitResponceSchema(
            user_login=visit.user.login,
            show_place_name=visit.show_place.name,
            show_place_city_name=visit.show_place.city.name,
            grade=visit.grade,
            review=visit.review,
            created_at=visit.create_at
        )

class GetUserHistoryRequestSchema(BaseModel):
    user_login:str

class GetUserHistoryResponceSchema(BaseModel):
    visits:list[Visit]

    @classmethod
    def from_entity(cls, visits:list[Visit]) -> 'GetUserHistoryResponceSchema':
        return GetUserHistoryResponceSchema(
            visits=visits
        )