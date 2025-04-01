from contextlib import asynccontextmanager
from functools import reduce

import requests
import json

from fastapi import FastAPI
import flet as ft
import flet.fastapi as flet_fastapi

from domain.entities.place_types import PlaceType
from application.front.models.models import User


user = User()

    
@asynccontextmanager
async def lifespan(app: FastAPI):
    await flet_fastapi.app_manager.start()
    yield
    await flet_fastapi.app_manager.shutdown()


def get_login_window(page:ft.Page):
    rst = ft.Text("Войдите в систему под своим профилем")
    login_field = ft.TextField(label="Логин", value="Test")
    password_field = ft.TextField(label="Пароль", password=True, value="test")

    def login(e):
        
        header = {
            "login":login_field.value,
            "password":password_field.value
        }
        
        result:dict = requests.post("http://0.0.0.0:8000/user/login/", data=json.dumps(header)).json()
        rst.value=str(result)
        rst.update()
        if not "detail" in result.keys():
            user.login = result["login"]
            user.nickname = result["nickname"]
            user.oid = result["oid"]
            user.token = result["token"]
        
            page.go("/user")
        
    
    return ft.Container(
        content=ft.Column(
            controls=[
                rst,
                login_field,
                password_field,
                ft.TextButton("Войти", on_click=login)
            ]
        ),
        margin=10,
        width= 500,

    )

def get_user_home_page(page:ft.Page):
    if user.token == "":
        page.go("/")
    def exit(e):
        user.clear()
        page.go("/")

    
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextButton("Выйти", on_click=exit)
                    ],
                    alignment=ft.MainAxisAlignment.END
                ),
                ft.TextButton("Найти достопримечательность", on_click= lambda _: page.go("/watch_showplace")),
                ft.TextButton("Добавить достопримечательность", on_click= lambda _: page.go("/add_showplace"))
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

def get_get_all_showplace(page:ft.Page):
    if user.token == "":
        page.go("/")

    def exit(e):
        user.clear()
        page.go("/")

    city_name = ft.TextField(label="Название города")

    dlg_modal:ft.AlertDialog = ft.AlertDialog(
        title=ft.Text(""),
    )

    # page.add(dlg_modal)


    content = ft.Container(
        content=ft.Column(
            controls=[]
        )
    )

    def get_show_place(e):
        try:
            responce = requests.get(f"http://0.0.0.0:8000/city/{city_name.value}/show_places")
            result:dict = responce.json()
            responce.raise_for_status()
            
        except requests.exceptions.HTTPError as errh:
            dlg_modal.title.value = str(result)
            dlg_modal.update()
            page.open(dlg_modal)
            return
        # raise ValueError(str(result))
        show_places:list = result["show_places"]
        show_places_controls:list = []

        for show_place in show_places:
            show_places_controls.append(
                ft.Row(
                    controls=
                    [
                        ft.Text(show_place["name"], size=25),
                        ft.Text(show_place["description"], size=25),
                        ft.Text(show_place["addres"], size=25),
                    ],
                )
            )    
        content.content.controls = show_places_controls
        content.update()


    return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                    controls=[
                        ft.TextButton("Выйти", on_click=exit)
                    ],
                    alignment=ft.MainAxisAlignment.END
                    ),
                    dlg_modal,
                    city_name,
                    ft.Button("Найти", on_click=get_show_place),
                    content,
                    ft.Text("Окно для вывода всех достопримечательностей города")
                
                ]
            )
        )

def _get_options_cities() -> list[ft.DropdownOption]:
    responce = requests.get("http://0.0.0.0:8000/city/all")
    responce.raise_for_status()
    result = responce.json()
    options = []

    for i in result["cities"]:
        options.append(
            ft.DropdownOption(
                key=i["name"],
                content=ft.Text(
                    value=i["name"]
                ),
            )
        )
    return options

    
def _get_options_types() -> list[ft.DropdownOption]:
    sh_types = PlaceType

    options = []
    for i in sh_types:
        options.append(
            ft.DropdownOption(
                key=i.value,
                content=ft.Text(
                    value=i.value
                ),
            )
        )
    return options

def add_show_place(page: ft.Page):
    dlg_modal:ft.AlertDialog = ft.AlertDialog(
        title=ft.Text(""),
    )

    sh_name = ft.TextField(label="Название", value="")
    sh_type = ft.Dropdown(
        label="Тип достопримечательности",
        options=_get_options_types(),
        width=400
    )
    sh_city = ft.Dropdown(
        label="Город",
        options=_get_options_cities()
    )
    sh_addres = ft.TextField(label="Адрес", value="")
    sh_latitude = ft.TextField(label="Широта", value="")
    sh_longitude = ft.TextField(label="Долгота", value="")
    sh_description = ft.TextField(label="Описание", value="")

    def add_sh(e):
        required_fields = reduce(lambda x, y: True if x or bool(y) else False, [sh_name.value, sh_type.value, sh_city.value, sh_addres.value, sh_latitude.value, sh_longitude.value, sh_description.value])
        if not required_fields:
            dlg_modal.title.value = "Не заполнены требуемые поля"
            dlg_modal.update()
            page.open(dlg_modal)
            return
        data = {
            
            "name":sh_name.value,
            "place_type": sh_type.value,
            "description": sh_description.value,
            "latitude": sh_latitude.value,
            "longitude": sh_longitude.value,
            "city_name": sh_city.value,
            "addres": sh_addres.value
        }    
        # raise ValueError(data)
        try:
            responce = requests.post("http://0.0.0.0:8000/showplace/add/", data=json.dumps(data), headers={'Content-Type': 'application/json' }, params={"location":"headers", "token":user.token,})
            result = responce.json()
            responce.raise_for_status()
            dlg_modal.title.value = f"Достопримечательность {result["name"]} в городе {result["city"]["name"]}, {result["city"]["country"]} успешно зарегестрирована"
            str(result)
        except requests.exceptions.HTTPError as errh:
            dlg_modal.title.value = str(result["detail"]["error"])
        
        dlg_modal.update()
        page.open(dlg_modal)
        return

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextButton("Выйти", on_click=exit)
                    ],
                    alignment=ft.MainAxisAlignment.END
                ),
                dlg_modal,
                sh_name,
                ft.Row(
                    controls=[
                        sh_type,
                        sh_city,
                    ]
                ),
                sh_addres,
                ft.Row(
                    controls=[
                        sh_latitude,
                        sh_longitude,
                    ],
                ),
                sh_description,
                ft.Button("Добавить", on_click=add_sh),
                ft.Button("Домой", on_click=lambda _: page.go("/user"))
            ]
        )
    )

    

async def main_window(page: ft.Page):
    page.title = "Сам себе гид"

    def route_change(route):
        page.views.clear()
        
        # page.views.append(
            
        # )
        
        if page.route == '/' or user.token == "":
            
            page.views.append(
                get_login_window(page)
            )
        if page.route == '/user':
            page.views.append(
                get_user_home_page(page)
            )
        if page.route == '/watch_showplace':
            page.views.append(
                get_get_all_showplace(page)
                )
        if page.route == '/add_showplace':
            page.views.append(
                add_show_place(page)
                )
        
        page.update()
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    # page.add(get_login_window())
    
    # page.update()