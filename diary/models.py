from django.db import models
from django.contrib.auth.models import User


class Trip(models.Model):
    """Запись о путешествии"""
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    
    
    location_name = models.CharField(max_length=200, verbose_name='Место')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, 
                                   null=True, blank=True, verbose_name='Широта')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, 
                                    null=True, blank=True, verbose_name='Долгота')
    
    
    cost = models.DecimalField(max_digits=10, decimal_places=2, 
                               null=True, blank=True, verbose_name='Стоимость (руб.)')
    
    
    rating_transport = models.IntegerField(default=3, verbose_name='Удобство передвижения')
    rating_safety = models.IntegerField(default=3, verbose_name='Безопасность')
    rating_population = models.IntegerField(default=3, verbose_name='Населённость')
    rating_nature = models.IntegerField(default=3, verbose_name='Растительность')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Путешествие'
        verbose_name_plural = 'Путешествия'

    def __str__(self):
        return f'{self.title} — {self.author.username}'

    def rating_avg(self):
        """Средняя оценка по всем критериям"""
        total = (self.rating_transport + self.rating_safety + 
                 self.rating_population + self.rating_nature)
        return round(total / 4, 1)


class TripPhoto(models.Model):
    """Фотографии к путешествию — отдельная таблица, т.к. фото может быть несколько"""
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, 
                             related_name='photos', verbose_name='Путешествие')
    image = models.ImageField(upload_to='trips/%Y/%m/', verbose_name='Фото')
    caption = models.CharField(max_length=200, blank=True, verbose_name='Подпись')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def __str__(self):
        return f'Фото к: {self.trip.title}'