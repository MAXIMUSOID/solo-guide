from pydantic import BaseModel

from domain.entities.model import City, ShowPlace


class CreateCityRequestShema(BaseModel):
    name:str
    country:str


class CreateCityResponceShema(BaseModel):
    oid: int
    name:str
    country:str

    @classmethod
    def from_entity(cls, city: City) -> 'CreateCityResponceShema':
        return CreateCityResponceShema(
            oid=city.oid,
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
    oid:int
    name:str
    place_type:str
    description:str
    latitude:float
    longitude:float
    city:City

    @classmethod
    def from_entity(cls, showplace: ShowPlace) -> 'CreateShowPlaceResponceShema':
        return CreateShowPlaceResponceShema(
            oid=showplace.oid,
            name=showplace.name,
            place_type=showplace.place_type,
            description=showplace.description,
            latitude=showplace.latitude,
            longitude=showplace.longitude,
            city=showplace.city
        )