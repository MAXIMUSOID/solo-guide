# Solo Guide Приложение

Приложение для регистрации достопримечательностей города и отметок об их посещении

## Зависимости

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

## Как установить

1. **Склонировать репозиторий на свой компьютер:**

   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository

2. Установить все `Зависимости`.


### Основные команды

* `make app` - запуск контейнеров с приложением и базой данных
* `make app-logs` - отображение логов работы приложения
* `make app-down` - выключение контейнеров
* `make pytest` - тестирование приложения с использованием pytest