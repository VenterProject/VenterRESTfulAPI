from django.urls import path, include
from Venter.views import CategoryViewset

urlpatterns = [
    path('', CategoryViewset.as_view, name='category'),
    path('category/', CategoryViewset.as_view, name='category'),
]