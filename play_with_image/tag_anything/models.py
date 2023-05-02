from django.db import models
from django.urls import reverse


class Tag(models.Model):
    tag = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Тег'
    )
    category = models.ForeignKey(
        'TagCategory',
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'
        ordering = ('category', 'tag')

    def __str__(self) -> str:
        return self.tag

    def get_absolute_url(self):
        return reverse('gallery:tag_view', kwargs={'tag': self.tag})


class TagCategory(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Название',
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('pk',)

    def __str__(self):
        return self.name
