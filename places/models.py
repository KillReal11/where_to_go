from django.db import models

print("Запущен файл models.py")


class Places(models.Model):
    title = models.CharField('Название', max_length=200)
    description_short = models.TextField('Краткое описание', blank=True)
    description_long = models.TextField('Полное описание', blank=True)
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'место'
        verbose_name_plural = 'места'
