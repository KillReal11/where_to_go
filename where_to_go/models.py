from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Название', max_length=100, unique=True)
    short_description = models.TextField('Краткое описание', blank=True)
    long_description = HTMLField('Полное описание', blank=True)
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')

    class Meta:
        ordering = ['title']
        verbose_name = 'место'
        verbose_name_plural = 'места'

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(
        'Place',
        on_delete=models.CASCADE,
        verbose_name='локация картинки',
        related_name='images',
    )
    file = models.ImageField(
        'Картинка',
        upload_to='media/',
    )
    position_number = models.PositiveSmallIntegerField(
        'порядковый номер',
        default=0,
    )

    class Meta:
        ordering = ['position_number']
        verbose_name = 'картинка'
        verbose_name_plural = 'картинки'
        indexes = [
            models.Index(fields=['position_number']),
        ]

    def __str__(self):
        return f'{self.position_number} {self.place}'
