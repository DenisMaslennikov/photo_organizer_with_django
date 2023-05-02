from django.db import models
from django.urls import reverse

from tag_anything.models import Tag


class Image(models.Model):
    image = models.ImageField(upload_to='img/%Y/%m/%d',
                              verbose_name='Изображение')
    image_name = models.CharField(max_length=30,
                                  verbose_name='Название изображения')

    tags = models.ManyToManyField(Tag, verbose_name='Теги', )

    class Meta:
        default_related_name = 'images'
        verbose_name = 'картинки'
        verbose_name_plural = 'Картинки'
        ordering = ('pk',)

    def __str__(self) -> str:
        return self.image_name

    def get_absolute_url(self):
        return reverse('gallery:image', kwargs={'image_id': self.pk})
