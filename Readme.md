# Проект - Тестовое задания для газпром

## Описание проекта
Имеется xlsx файл, данные которого необходимо сохранить в БД
После чего сформировать на основе данных в бд отчет, пример отчета представлен ниже

![App Screenshot](./documentation_data/report_content.png)  

## Структура проекта
```bash
├─── sender/
│   ├─── report_api/
│   │   ├─── migrations/
│   │   │   ├─── 0001_initial.py
│   │   │   └─── __init__.py
│   │   ├─── tests/
│   │   │   ├─── test_files/
│   │   │   │   └───testing_data.xslx
│   │   │   ├─── test_model.py
│   │   │   ├─── test_serializer.py
│   │   │   └─── test_views.py
│   │   ├─── __init__.py
│   │   ├─── admin.py
│   │   ├─── apps.py
│   │   ├─── models.py
│   │   ├─── producer.py
│   │   ├─── serializers.py
│   │   ├─── tests.py
│   │   ├─── urls.py
│   │   └─── views.py
│   ├─── sender/
│   │   ├─── __init__.py
│   │   ├─── asgi.py
│   │   ├─── settings.py
│   │   ├─── urls.py
│   │   └─── wsgi.py
│   ├─── utils/
│   │   ├───__init__.py
│   │   ├───async_file.py
│   │   ├───report_generate.py
│   │   └─── wrappers.py
│   ├─── Dockerfile
│   ├─── entrypoint.sh
│   ├─── manage.py
│   ├─── pytest.ini
│   └─── requirements.txt
├─── .env
├─── .gitignore
├─── Readme.md
└─── unix-docker-compose.yml
```

## Описание решения
### Приложения
В данном проекте имеется одно приложение
- report_api

В данном приложении реализовано два представления
- получение файла, обработка и сохранение данные (post)
- генерация отчета на основе данных из бд (get)

### Тестирование


Описание входныых данных можно узнать при исполь
Данный проект реализован при помощи async Django для достижения необходимых решений использовался uvicorn и asgiref


## Тестирование

