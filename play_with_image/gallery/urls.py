from django.urls import path
from . import views


app_name = 'gallery'

urlpatterns = [
    path('', views.tag_view, name='index'),
    path('tag/<str:tag>/', views.tag_view, name='tag_view'),
    path('image/<int:image_id>', views.image_view, name='image'),
    path('about/', views.about, name='about'),
    path('add-image/', views.add_image, name='add_image'),
]
