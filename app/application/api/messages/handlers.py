from fastapi import Depends, status
from fastapi import HTTPException
from fastapi.routing import APIRouter

from domain.exceptions.base import BaseEntityException
from domain.entities.model import City, ShowPlace
from infra.repository.converter import convert_city_to_model
from domain.entities.place_types import PlaceType
from infra.repository.exceptions.base import RepositoryException
from application.api.messages.shemas import CreateCityRequestShema, CreateCityResponceShema, CreateShowPlaceRequestShema, CreateShowPlaceResponceShema
from infra.repository.show_place import add_city, add_show_place, get_city

router = APIRouter(tags=['City'])
router_showplace = APIRouter(tags=['Show Place'])


@router.post(
        '/add', 
        response_model=CreateCityResponceShema, 
        status_code=status.HTTP_201_CREATED,
        description='Эндпоинт создаёт новый город, если город с таким названием уже существует, то возвращается 400 ошибка',
        responses={
            status.HTTP_201_CREATED: {'model': CreateCityResponceShema},
            # status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
        }
)
async def create_city_handler(schema: CreateCityRequestShema):
    '''Создать новый город'''
    try:
        _city = City(name=schema.name, country=schema.country)
        city = convert_city_to_model(add_city(_city))
    except RepositoryException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    return CreateCityResponceShema.from_entity(city)


@router_showplace.post(
    '/add', 
        response_model=CreateShowPlaceResponceShema, 
        status_code=status.HTTP_201_CREATED,
        description='Эндпоинт создаёт новую достопримечательность, если достопримечательность с таким названием уже существует, то возвращается 400 ошибка',
        responses={
            status.HTTP_201_CREATED: {'model': CreateShowPlaceResponceShema},
            # status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
        })
async def create_show_place(schema: CreateShowPlaceRequestShema):
    '''Создать новую достопримечательность'''
    try:
        city = convert_city_to_model(get_city(schema.city_name))
        _show_place = ShowPlace(
            name=schema.name, 
            _place_type=schema.place_type,
            description=schema.description,
            latitude=schema.latitude,
            longitude=schema.longitude,
            city=city,
            addres=schema.addres)
        
        show_place = add_show_place(_show_place)
            
    except RepositoryException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    except BaseEntityException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    return CreateShowPlaceResponceShema.from_entity(show_place)