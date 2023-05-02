from django.urls import path
from . import views


app_name = 'gallery'

urlpatterns = [
    path('', views.ImageListView.as_view(), name='index'),
    path('tag/<str:tag_str>/', views.ImageListView.as_view(), name='tag_view'),
    path('image/<int:image_id>', views.ImageView.as_view(), name='image'),
    path('about/', views.about, name='about'),
    path('add-image/', views.AddImage.as_view(), name='add_image'),
]
