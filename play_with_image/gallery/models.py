from django.db import models
from django.urls import reverse


class Image(models.Model):
    image = models.ImageField(upload_to='img/%Y/%m/%d',
                              verbose_name='Изображение')
    image_name = models.CharField(max_length=30,
                                  verbose_name='Название изображения')
    tags = models.ManyToManyField('Tag', verbose_name='Теги')

    def __str__(self) -> str:
        return self.image_name

    def get_absolute_url(self):
        return reverse('gallery:image', kwargs={'image_id': self.pk})


class Tag(models.Model):
    tag = models.CharField("tag", max_length=20, unique=True)

    def __str__(self) -> str:
        return self.tag

    def get_absolute_url(self):
        return reverse('gallery:tag_view', kwargs={'tag': self.tag})


# class ImageTags(models.Model):
#     id_image = models.ForeignKey("Image",
#                                  verbose_name="id image",
#                                  on_delete=models.CASCADE)
#     id_tag = models.ForeignKey("Tag",
#                                verbose_name="id tag",
#                                on_delete=models.CASCADE)


class Settings(models.Model):
    setting_name = models.CharField("setting name", max_length=30)
    setting_value = models.CharField("setting value", max_length=300)

    def __str__(self):
        return f'{self.setting_name} {self.setting_value}'
