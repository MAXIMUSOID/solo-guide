from datetime import datetime
from typing import List
from pydantic import BaseModel

from domain.entities.model import City, ShowPlace, User, Visit


class CreateCityRequestShema(BaseModel):
    name:str
    country:str


class CreateCityResponceShema(BaseModel):
    name:str
    country:str

    @classmethod
    def from_entity(cls, city: City) -> 'CreateCityResponceShema':
        return CreateCityResponceShema(
            name=city.name,
            country=city.country
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
