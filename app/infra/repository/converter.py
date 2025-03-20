
from infra.repository.model import City, ShowPlace, User, Visit
import domain.entities.model as model



def convert_city_to_model(city:City) -> model.City:
    return model.City(
        name=city.name,
        country=city.country,
        oid=city.id
    )

def convert_show_place_to_model(show_place:ShowPlace, city:City) -> model.ShowPlace:
    return model.ShowPlace(
        name=show_place.name,
        _place_type=show_place.place_type, 
        description=show_place.description, 
        latitude=show_place.latitude, 
        longitude=show_place.longitude,
        city=convert_city_to_model(city),
        addres=show_place.addres,
        oid=show_place.id
        )


def convert_user_to_model(user:User) -> model.User:
    return model.User(
        nickname=user.nickname,
        login=user.login,
        oid=user.id
    )

def convert_visit_to_model(visit:Visit, user:User, show_place:ShowPlace, city:City) -> model.Visit:
    user_model = convert_user_to_model(user)
    show_place_model = convert_show_place_to_model(show_place, city)
    return model.Visit(
        user=user_model,
        show_place=show_place_model,
        review=visit.review,
        grade=visit.grade,
        create_at=visit.datetime
    )