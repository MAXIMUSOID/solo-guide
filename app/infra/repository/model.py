from datetime import date, datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, Text, ForeignKey

from domain.entities.place_types import PlaceType


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(nullable=False)
    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

           
class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), unique=True)
    country: Mapped[str] = mapped_column(String())


class ShowPlace(Base):
    __tablename__ = "showplaces"

    id: Mapped[int] = mapped_column(primary_key=True)
    place_type: Mapped[Enum] = mapped_column(Enum(PlaceType), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    addres: Mapped[str]


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    show_place_id: Mapped[int] = mapped_column(ForeignKey("showplaces.id"))
    grade: Mapped[int]
    review: Mapped[str]
    datetime:Mapped[date] = mapped_column(default=datetime.now())

class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    show_place_id: Mapped[int] = mapped_column(ForeignKey("showplaces.id"))


