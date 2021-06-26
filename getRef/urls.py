from django.urls import path
from .views import RefFormView

urlpatterns = [
    path('', RefFormView.as_view(), name='refform'),
]

