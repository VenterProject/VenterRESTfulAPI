from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # ex: /venter/
    path('', TemplateView.as_view(template_name='Venter/home.html'), name='home'),
    # ex: /venter/home/
    path('home/', TemplateView.as_view(template_name='Venter/home.html'), name='home'),
]    