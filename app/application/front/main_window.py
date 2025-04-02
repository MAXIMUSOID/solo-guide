from contextlib import asynccontextmanager
from functools import reduce

import requests
import json

from fastapi import FastAPI
import flet as ft
import flet.map as map
import flet.fastapi as flet_fastapi

from domain.entities.place_types import PlaceType
from application.front.models.models import User


user = User()

    
@asynccontextmanager
async def lifespan(app: FastAPI):
    await flet_fastapi.app_manager.start()
    yield
    await flet_fastapi.app_manager.shutdown()


def get_login_window_page(page:ft.Page):
    rst = ft.Text("Войдите в систему под своим профилем")
    login_field = ft.TextField(label="Логин", value="Test", width=500)
    password_field = ft.TextField(label="Пароль", password=True, value="test", width=500)

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

        else:
            rst.value = result["detail"]["error"]
            rst.update()
        
        
    
    return ft.Column(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        rst,
                        login_field,
                        password_field,
                        ft.TextButton("Войти", on_click=login),
                        ft.Text("Или"),
                        ft.TextButton("Создать", on_click=lambda _: page.go("/user_add"))
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )

def get_change_user_password_page(page:ft.Page):
    dlg_modal:ft.AlertDialog = ft.AlertDialog(
        title=ft.Text(""),
    )

    password_field = ft.TextField(label="Пароль", password=True, value="", width=500)
    password_field_repeate = ft.TextField(label="Повторите пароль", password=True, value="", width=500)
    
    def change_password(e:ft.TapEvent):
        if password_field.value == "" or password_field.value != password_field_repeate.value:
            dlg_modal.title.value = "Пароль не может быть пустым или он не совпадает"
            dlg_modal.update()
            page.open(dlg_modal)
            return
        
        data = {
            "user_login":user.login,
            "password":password_field.value
        }
        try:
            responce:requests.Response = requests.post("http://0.0.0.0:8000/user/change_password/", data=json.dumps(data), headers={'Content-Type': 'application/json' }, params={"location":"headers", "token":user.token})
            result = responce.json()
            responce.raise_for_status()
            dlg_modal.title.value = "Пароль успешно изменён"
            dlg_modal.update()
            page.open(dlg_modal)
        except requests.exceptions.HTTPError as errh:
            dlg_modal.title.value = str(result["detail"]["error"])
            dlg_modal.update()
            page.open(dlg_modal)
            return
    

    return ft.Column(
            expand=True,
            controls=[
                dlg_modal,
                ft.Column(
                    expand=True,
                    controls=[
                        password_field,
                        password_field_repeate,
                        ft.TextButton("Назад", on_click=lambda _: page.go("/user")),
                        ft.TextButton("Изменить", on_click=change_password),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )
    ...


def get_create_user_page(page:ft.Page):
    dlg_modal:ft.AlertDialog = ft.AlertDialog(
        title=ft.Text(""),
    )
    rst = ft.Text("Создайте свой профиль")
    login_field = ft.TextField(label="Логин", value="Test", width=500)
    nickname_field = ft.TextField(label="Ник", value="Test", width=500)
    password_field = ft.TextField(label="Пароль", password=True, value="", width=500)
    password_field_repeate = ft.TextField(label="Повторите пароль", password=True, value="", width=500)

    def login():
        
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

    def create_user(e):
        if password_field.value == "" or password_field.value != password_field_repeate.value:
            dlg_modal.title.value = "Пароль не может быть пустым или он не совпадает"
            dlg_modal.update()
            page.open(dlg_modal)
            return
        
        header = {
            "nickname":nickname_field.value,
            "login":login_field.value,
            "password":password_field.value
        }
        try:
            responce:requests.Response = requests.post("http://0.0.0.0:8000/user/add/", data=json.dumps(header))
            result = responce.json()
            responce.raise_for_status()
            login()
        except requests.exceptions.HTTPError as errh:
            dlg_modal.title.value = str(result["detail"]["error"])
            dlg_modal.update()
            page.open(dlg_modal)
            return
        

    return ft.Column(
            expand=True,
            controls=[
                dlg_modal,
                ft.Column(
                    expand=True,
                    controls=[
                        rst,
                        nickname_field,
                        login_field,
                        password_field,
                        password_field_repeate,
                        ft.Row(
                            controls=[
                            ft.TextButton("Создать", on_click=create_user),
                            ft.TextButton("Назад", on_click=lambda _: page.go("/"))
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )

def get_user_home_page(page:ft.Page):
    if user.token == "":
        page.go("/")

    data = {
        "user_login":user.login
    }
    history_data = ft.Column(
        controls=[]
    )
    try:
        responce = requests.post("http://0.0.0.0:8000/user/history/", data=json.dumps(data), headers={'Content-Type': 'application/json' }, params={"location":"headers", "token":user.token})
        result:dict = responce.json()
        responce.raise_for_status()
        
    except requests.exceptions.HTTPError:
        ...
    if "visits" in result.keys():
        for i in result["visits"]:
            history_data.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(i["show_place"]["name"]),
                        ft.Text(i["show_place"]["city"]["name"]),
                        ft.Text(i["review"])
                    ]
                )
            )
        
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(f"Здравстуй, {user.nickname}. Попутешествуем?"),
                ft.Text("Мои путь"),
                history_data
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

def get_get_all_showplace(page:ft.Page):
    if user.token == "":
        page.go("/")



    dlg:ft.AlertDialog = ft.AlertDialog(
        title=ft.Text(""),
    )

    city_name = ft.TextField(label="Название города")

    grade_field = ft.TextField("Оценка")
    review_field = ft.TextField("Отзыв")

    def create_review(e:ft.TapEvent):
        add_review(show_place_name=e.control.data["show_place_name"], show_place_city_name=e.control.data["show_place_city"])

    def add_review(show_place_name, show_place_city_name):
        data = {
            "user_login": user.login,
            "show_place_name": show_place_name,
            "show_place_city": show_place_city_name,
            "grade": grade_field.value,
            "review": review_field.value,
        }
        try:
            responce = requests.post("http://0.0.0.0:8000/visit/add/", data=json.dumps(data), headers={'Content-Type': 'application/json' }, params={"location":"headers", "token":user.token})
            result = responce.json() 
            responce.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            page.close(review_dialog)
            # raise ValueError(result)
            dlg.title.value = str(result["detail"]["error"])
            dlg.update()
            page.open(dlg)
            return
        
        dlg.title.value = "Отзыв зарегистрирован"
        dlg.update()
        page.open(dlg)
        ...

    review_dialog = ft.AlertDialog(
        # modal=True,
        title=ft.Text("Оставьте свой отзыв"),
        content=ft.Column(
            controls=[
                grade_field,
                review_field
            ],
        ),
        actions=[
            ft.Button("Оставить отзыв", on_click=create_review)
        ]
    )




    content = ft.Container(
        content=ft.Column(
            controls=[]
        )
    )

    def open_review_dialog(e:ft.ControlEvent):
        # raise ValueError(e.control.data)
        review_dialog.actions[0].data = e.control.data
        review_dialog.update()
        page.open(review_dialog)
        ...

    def get_show_place(e):
        try:
            responce = requests.get(f"http://0.0.0.0:8000/city/{city_name.value}/show_places")
            result:dict = responce.json()
            responce.raise_for_status()
            
        except requests.exceptions.HTTPError as errh:
            dlg.title.value = str(result)
            dlg.update()
            page.open(dlg)
            return
        # raise ValueError(str(result))
        show_places:list = result["show_places"]
        show_places_controls:list = []

        for show_place in show_places:
            data={
                "show_place_name":show_place["name"],
                "show_place_city":show_place["city"]["name"], 
                }
            show_places_controls.append(
                ft.Row(
                    controls=
                    [
                        ft.Text(show_place["name"], size=25),
                        ft.Text(show_place["description"], size=25),
                        ft.Text(show_place["addres"], size=25),
                        ft.Button("Оценить", data=data, on_click=open_review_dialog)
                    ],
                )
            )    
        content.content.controls = show_places_controls
        content.update()


    return ft.Container(
            content=ft.Column(
                controls=[
                    dlg,
                    review_dialog,
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
                        ft.Text(user.nickname),
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
    page.appbar = ft.AppBar(title=ft.Text("fffffffff"))

    def exit(e):
        user.clear()
        page.go("/")

    def route_change(route):
        page.views.clear()

        top_bar = ft.Column(
            width=3000,
            # expand=True,
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text("Сам себе гид"),
                                    ft.TextButton("Найти достопримечательность", on_click= lambda _: page.go("/watch_showplace")),
                                    ft.TextButton("Добавить достопримечательность", on_click= lambda _: page.go("/add_showplace")),
                                ],
                            ),
                            ft.Row(
                            controls=[
                                ft.Text(user.nickname),
                                ft.TextButton("Изменить пароль", on_click=lambda _: page.go("/user/change_password")),
                                ft.TextButton("Выйти", on_click=exit)
                            ],
                            alignment=ft.MainAxisAlignment.END
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.START
        )
        
        # page.views.append(
            
        # )
        
        if page.route == '/' or user.token == "":
            page.views.append(
                ft.Column(
                    controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Сам себе гид"),
                        ]
                    ),
                    get_login_window_page(page),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        if page.route == '/user_add':
            page.views.append(
                ft.Column(
                    controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Сам себе гид"),
                        ]
                    ),
                    get_create_user_page(page),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        if page.route == '/user':
            page.views.append(
                ft.Column(
                    controls=[
                    top_bar,
                    get_user_home_page(page),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        if page.route == '/user/change_password':
            page.views.append(
                ft.Column(
                    controls=[
                    top_bar,
                    get_change_user_password_page(page),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        if page.route == '/watch_showplace':
            page.views.append(
                ft.Column(
                    controls=[
                    top_bar,
                    get_get_all_showplace(page),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
                )
        if page.route == '/add_showplace':
            page.views.append(
                ft.Column(
                    controls=[
                    top_bar,
                    add_show_place(page),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
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