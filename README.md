# 🗺️ Artem Map - Интерактивная карта достопримечательностей

![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue.svg)
![Leaflet](https://img.shields.io/badge/Leaflet-Maps-brightgreen.svg)
![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)

Веб-приложение для создания и управления интерактивной картой с точками интереса. Позволяет добавлять места с фотографиями, описаниями и координатами с удобной административной панелью.

---

## ✨ Возможности

### 🎯 Основной функционал
- **Интерактивная карта** на основе Leaflet с точками интереса
- **Детальная информация** о каждом месте при клике на маркер  
- **Галерея изображений** для каждого места с превью
- **GeoJSON API** для интеграции с другими системами
- **Адаптивный дизайн** для мобильных устройств

### 🛠️ Администрирование
- 📍 Добавление/редактирование мест через админку Django
- 🖼️ Загрузка нескольких фотографий для каждого места
- 🔄 Drag & Drop сортировка изображений
- 📊 Превью фотографий прямо в админке
- 📝 Rich-text редактор для описаний (CKEditor)
- 🗃️ Автоматическая загрузка данных из JSON файлов

### 🔧 Технические особенности
- **Django 4.2** с архитектурой MVC
- **PostgreSQL** для хранения данных
- **Docker** контейнеризация для простого развертывания
- **RESTful API** для получения данных о местах
- **Автоматический линтинг** с black и isort

---

## 🏗️ Архитектура проекта

### Модели данных
```python
class Place:
    title: str                    # Название места
    description_short: RichText   # Краткое описание  
    description_long: RichText    # Полное описание
    lat: float                   # Широта
    lng: float                   # Долгота

class Image:
    place: ForeignKey            # Связь с местом
    image: ImageField            # Фотография
    position: int                # Позиция для сортировки
```

## 🚀 Быстрый старт

### Установка и запуск с Make (рекомендуется)

```bash
# Клонирование репозитория
git clone https://github.com/MikhailPI1/artem-s_map.git
cd artem-s_map

# Установка зависимостей
make install

# Настройка базы данных
make migrate

# Создание администратора
make superuser

# Запуск сервера
make run

```

## Добавление новых позиций прямо с помощью GEOJSON
```python
python manage.py load_place (адрес JSON файла)
```

### GeoJSON внутри:
```bash
{
    "title": "Название места",
    "imgs": ["url1.jpg", "url2.jpg"],
    "description_short": "Краткое описание", 
    "description_long": "Полное описание",
    "coordinates": {"lng": 37.6173, "lat": 55.7558}
}
```
