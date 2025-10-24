from ckeditor.fields import RichTextField
from django.db import models


class Place(models.Model):
    title = models.CharField("Название", max_length=200)
    description_short = RichTextField("Краткое описание", blank=True)
    description_long = RichTextField("Полное описание", blank=True)
    lat = models.FloatField("Широта")
    lng = models.FloatField("Долгота")

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField("Изображение", upload_to="places/")
    position = models.PositiveIntegerField("Позиция", default=0)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"Изображение для {self.place.title}"
