
from infra.repository.model import City, ShowPlace, User
import domain.entities.model as model



def convert_city_to_model(city:City) -> model.City:
    return model.City(
        name=city.name,
        country=city.country
    )

def convert_show_place_to_model(show_place:ShowPlace, city:City) -> model.ShowPlace:
    return model.ShowPlace(
        name=show_place.name,
        _place_type=show_place.place_type, 
        description=show_place.description, 
        latitude=show_place.latitude, 
        longitude=show_place.longitude,
        city=city,
        addres=show_place.addres
        )


def convert_user_to_model(user:User) -> model.User:
    return model.User(
        nickname=user.nickname,
        login=user.login,
    )