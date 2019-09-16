from django.urls import path, include
from Venter.views import CategoryViewset, OrganisationViewset

urlpatterns = [
    path('', CategoryViewset.as_view, name='category'),
    path('category/', CategoryViewset.as_view, name='category'),
    path('organisation/', OrganisationViewset.as_view, name='organisation'),
]