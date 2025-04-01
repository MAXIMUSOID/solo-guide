from authx import RequestToken
from fastapi import Depends, status
from fastapi import HTTPException, Response
from fastapi.routing import APIRouter

from application.api.messages.auth import config
from application.api.messages.auth import SECURITY
from domain.exceptions.base import BaseEntityException
from domain.entities.model import City, ShowPlace, User, Visit
from infra.repository.converter import convert_city_to_model
from domain.entities.place_types import PlaceType
from infra.repository.exceptions.base import RepositoryException
from application.api.messages.shemas import (CreateCityRequestShema, 
                                             CreateCityResponceShema, 
                                             CreateShowPlaceRequestShema, 
                                             CreateShowPlaceResponceShema, 
                                             CreateUserRequestSchema, 
                                             CreateUserResponceSchema, 
                                             CreateVisitRequestSchema, 
                                             CreateVisitResponceSchema, 
                                             GetAllCitiesResponceSchema, 
                                             GetShowPlacesToCityRequestSchema, 
                                             GetShowPlacesToCityResponceSchema, 
                                             LoginUserRequestSchema, 
                                             LoginUserResponceShcema,
                                             )
from infra.repository.entrypoint import add_city, add_show_place, add_user, add_visit, get_cities, get_city, get_show_place, get_show_places_by_city, get_user_to_model, login_user

router = APIRouter(tags=['City'])
router_showplace = APIRouter(tags=['Show Place'])
router_user = APIRouter(tags=['User'])
router_visit = APIRouter(tags=['Visit'])

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
        city = add_city(_city)
    except RepositoryException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    return CreateCityResponceShema.from_entity(city)


@router.get(
        '/{city_name}/show_places',
        response_model=GetShowPlacesToCityResponceSchema,
        status_code=status.HTTP_200_OK,
        description="Получение всех достопримечательностей города",
        responses={
            status.HTTP_200_OK: {'model': GetShowPlacesToCityResponceSchema}
        }
)
async def get_city_show_places_handler(city_name:str):
    try:
        show_places:list[ShowPlace] = get_show_places_by_city(city_name)
    except RepositoryException as exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': exception.message})
    except BaseEntityException as exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': exception.message})
    return GetShowPlacesToCityResponceSchema(show_places=show_places)


@router.get(
    '/all',
    response_model=GetAllCitiesResponceSchema,
    status_code=status.HTTP_200_OK,
    description="Получение всех городов",
    responses={
        status.HTTP_200_OK: {'model': GetAllCitiesResponceSchema}
    }
)
async def get_all_cities_handler():
    try:
        cities = get_cities()
    except RepositoryException as exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': exception.message})
    except BaseEntityException as exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': exception.message})
    return GetAllCitiesResponceSchema(cities=cities)

@router_showplace.post(
    '/add', 
        dependencies=[Depends(SECURITY.get_token_from_request)],
        response_model=CreateShowPlaceResponceShema, 
        status_code=status.HTTP_201_CREATED,
        description='Эндпоинт создаёт новую достопримечательность, если достопримечательность с таким названием уже существует, то возвращается 400 ошибка',
        responses={
            status.HTTP_201_CREATED: {'model': CreateShowPlaceResponceShema},
            # status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
        })
async def create_show_place(schema: CreateShowPlaceRequestShema, token:RequestToken = Depends()):
    '''Создать новую достопримечательность'''
    try:
        SECURITY.verify_token(token=token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': 'Требуется вход'})
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

@router_user.post(
    '/add',
    response_model=CreateUserResponceSchema,
    status_code=status.HTTP_201_CREATED,
    description='Эндпоинт создаёт нового пользователя',
    responses={
        status.HTTP_201_CREATED: {'model': CreateUserResponceSchema}
    })
async def create_user(schema:CreateUserRequestSchema):
    '''
    Создать нового пользователя
    '''
    try:
        new_user:User = User(nickname=schema.nickname, login=schema.login)
        user = add_user(user=new_user, password=schema.password)
    except RepositoryException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    except BaseEntityException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    
    return CreateUserResponceSchema.from_entity(user)

@router_user.post(
    '/login',
    response_model=LoginUserResponceShcema,
    status_code=status.HTTP_200_OK,
    description='Эндпоинт вход пользователя пользователя',
    responses={
        status.HTTP_201_CREATED: {'model': LoginUserResponceShcema}
    })
async def login_user_handler(schema:LoginUserRequestSchema, responce: Response):
    '''
    Создать нового пользователя
    '''
    try:
        user:User = login_user(user_login=schema.login, password=schema.password)
        token = SECURITY.create_access_token(uid=str(user.oid))
        responce.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    except RepositoryException as exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': exception.message})
    except BaseEntityException as exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': exception.message})
    
    
    return LoginUserResponceShcema.from_entity(user=user, token=token)


@router_visit.post(
    '/add',
    dependencies=[Depends(SECURITY.get_token_from_request)],
    response_model=CreateVisitResponceSchema,
    status_code=status.HTTP_201_CREATED,
    description='Эндпоинт создаёт новое посещение пользователем достопримечательности',
    responses={
        status.HTTP_201_CREATED: {'model': CreateVisitResponceSchema}
    })
async def create_visit(schema:CreateVisitRequestSchema, token:RequestToken = Depends()):
    '''
    Создать нового пользователя
    '''
    try:
        SECURITY.verify_token(token=token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': 'Требуется вход'})
    try:
        visit:Visit = add_visit(
            user_login=schema.user_login,
            show_place_name=schema.show_place_name,
            show_place_city=schema.show_place_city,
            grade=schema.grade,
            review=schema.review
        )
    except RepositoryException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    except BaseEntityException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return CreateVisitResponceSchema.from_entity(visit=visit)