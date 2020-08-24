from django.urls import path

from . import views

urlpatterns = [
    path('view/screen/<int:screen_id>', views.screen),
    path('internal/get_view/<int:screen_id>', views.get_next_image),
    path('', views.index)
]
