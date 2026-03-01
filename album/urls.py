from django.urls import path
from . import views

urlpatterns = [
    path('', views.photo_list, name='photo_list'),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('my_photos/', views.my_photos, name='my_photos'),
    path('delete/<int:photo_id>/', views.delete_photo, name='delete_photo'),
]