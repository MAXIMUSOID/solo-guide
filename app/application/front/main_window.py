from contextlib import asynccontextmanager

import requests
import json

from fastapi import FastAPI
import flet as ft
import flet.fastapi as flet_fastapi


@asynccontextmanager
async def lifespan(app: FastAPI):
    await flet_fastapi.app_manager.start()
    yield
    await flet_fastapi.app_manager.shutdown()


def get_login_window():
    rst = ft.Text("Войдите в систему под своим профилем")
    login_field = ft.TextField(label="Логин", value="Test")
    password_field = ft.TextField(label="Пароль", password=True, value="test")

    def login(e):
        
        header = {
            "login":login_field.value,
            "password":password_field.value
        }
        
        result = requests.post("http://0.0.0.0:8000/user/login/", data=json.dumps(header)).json()
        rst.value=str(result)
        rst.update()
        # flet_fastapi.
    
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
    

async def main_window(page: ft.Page):
    
    page.add(get_login_window())
    
    # page.update()