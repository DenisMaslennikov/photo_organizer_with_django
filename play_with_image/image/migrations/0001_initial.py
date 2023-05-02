# Generated by Django 4.2 on 2023-04-29 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tag_anything', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='img/%Y/%m/%d', verbose_name='Изображение')),
                ('image_name', models.CharField(max_length=30, verbose_name='Название изображения')),
                ('tags', models.ManyToManyField(to='tag_anything.tag', verbose_name='Теги')),
            ],
        ),
    ]
