from django.db import models


class Location(models.Model):
    address = models.CharField(
        'Адрес',
        max_length=200,
        unique=True
    )
    lon = models.FloatField(verbose_name='Долгота', null=True, blank=True)
    lat = models.FloatField(verbose_name='Широта', null=True, blank=True)
    updated_at = models.DateTimeField('Обновлено', db_index=True)

    class Meta:
        verbose_name = 'локация'
        verbose_name_plural = 'локации'

    def __str__(self):
        return f'{self.address} - ({self.lon},{self.lat})'
