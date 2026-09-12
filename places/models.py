from django.db import models

print("Запущен файл models.py")


class Place(models.Model):
    place_id = models.CharField('Уникальный идентификатор локации', max_length=50)
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


class Image(models.Model):
    title = models.ForeignKey(
        'Place',
        on_delete=models.CASCADE,
        verbose_name="место, где сделана картинка",
        related_name='images',
    )
    file = models.ImageField(
        'Картинка',
        upload_to='media/',
        null=True,
        blank=True
    )
    position_number = models.IntegerField(
        'Номер картинки в расположении',
        default=0,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.position_number} {self.title}'

    class Meta:
        ordering = ['position_number']
        verbose_name = 'картинка'
        verbose_name_plural = 'картинки'
