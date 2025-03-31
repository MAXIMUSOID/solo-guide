from contextlib import asynccontextmanager

import requests
import json

from fastapi import FastAPI
import flet as ft
import flet.fastapi as flet_fastapi

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
                ft.TextButton("Выйти", on_click=exit),
                ft.TextButton("Найти достопримечательность", on_click= lambda _: page.go("/watch_showplace"))
            ]
        )
    )

def get_get_all_showplace(page:ft.Page):
    if user.token == "":
        page.go("/")

    def exit(e):
        user.clear()
        page.go("/")

    city_name = ft.TextField(label="Название города")
    

    content = ft.Container(
        content=ft.Column(
            controls=[]
        )
    )

    def get_show_place(e):
        result:dict = requests.get(f"http://0.0.0.0:8000/city/{city_name.value}/show_places").json()
        
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
                    ft.TextButton("Выйти", on_click=exit),
                    city_name,
                    ft.Button("Найти", on_click=get_show_place),
                    content,
                    ft.Text("Окно для вывода всех достопримечательностей города")
                
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