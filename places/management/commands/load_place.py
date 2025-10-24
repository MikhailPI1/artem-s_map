from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import json
import requests
from places.models import Place, Image
import os
from django.conf import settings
import shutil

class Command(BaseCommand):
    help = 'Загрузить место из JSON файла'
    
    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)
    
    def handle(self, *args, **options):
        json_file = options['json_file']
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                if data:
                    data = data[0]
                    print(f"Взял первый элемент из массива")
                else:
                    print(f"Пустой массив в {json_file}")
                    return
            
            if 'title' not in data or 'coordinates' not in data:
                print(f"Неверный формат JSON в {json_file}")
                return
            
            place, created = Place.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description_short': data.get('description_short', ''),
                    'description_long': data.get('description_long', ''),
                    'lng': float(data['coordinates']['lng']),
                    'lat': float(data['coordinates']['lat'])
                }
            )
            
            if created:
                print(f"Создано новое место: {place.title}")
            else:
                place.description_short = data.get('description_short', '')
                place.description_long = data.get('description_long', '')
                place.lat = float(data['coordinates']['lat'])
                place.lng = float(data['coordinates']['lng'])
                place.save()
                print(f"🔄 Обновлено существующее место: {place.title}")
            
            static_place_dir = os.path.join(settings.BASE_DIR, 'static', 'places', str(place.id))
            os.makedirs(static_place_dir, exist_ok=True)
            
            json_filename = os.path.basename(json_file)
            static_json_path = os.path.join(static_place_dir, json_filename)
            shutil.copy2(json_file, static_json_path)
            print(f"JSON сохранен: static/places/{place.id}/{json_filename}")
            
            place.images.all().delete()
            
            for i, img_url in enumerate(data.get('imgs', [])):
                try:
                    response = requests.get(img_url)
                    response.raise_for_status()
                    
                    filename = img_url.split('/')[-1]
                    
                    image = Image(place=place, position=i)
                    image.image.save(
                        filename, 
                        ContentFile(response.content),
                        save=True
                    )
                    
                    print(f"Фото сохранено: {image.image.name}")
                    
                except Exception as img_error:
                    print(f"Ошибка при загрузке изображения {img_url}: {img_error}")
                    continue
            
            print(f'Успешно загружено: {place.title}')
            
        except Exception as e:
            print(f'Ошибка в файле {json_file}: {e}')