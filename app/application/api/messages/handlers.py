from fastapi import Depends, status
from fastapi import HTTPException
from fastapi.routing import APIRouter

from domain.entities.place_types import PlaceType
from infra.repository.exceptions.base import RepositoryException
from application.api.messages.shemas import CreateCityRequestShema, CreateCityResponceShema, CreateShowPlaceRequestShema, CreateShowPlaceResponceShema
from infra.repository.requests_db import add_city, add_show_place

router = APIRouter(tags=['City'])
router_showplace = APIRouter(tags=['Show Place'])


@router.post(
        '/', 
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
        city = add_city(name=schema.name, country=schema.country)
    except RepositoryException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    return CreateCityResponceShema.from_entity(city)


@router_showplace.post(
    '/', 
        response_model=CreateShowPlaceResponceShema, 
        status_code=status.HTTP_201_CREATED,
        description='Эндпоинт создаёт новую достопримечательность, если достопримечательность с таким названием уже существует, то возвращается 400 ошибка',
        responses={
            status.HTTP_201_CREATED: {'model': CreateShowPlaceResponceShema},
            # status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
        })
async def create_show_place(schema: CreateShowPlaceRequestShema):
    '''Создать новый город'''
    try:
        show_place = add_show_place(
            name=schema.name, 
            place_type=PlaceType(schema.place_type),
            description=schema.description,
            latitude=schema.latitude,
            longitude=schema.longitude,
            city_name=schema.city_name,
            addres=schema.addres)
    except RepositoryException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    return CreateShowPlaceResponceShema.from_entity(show_place)