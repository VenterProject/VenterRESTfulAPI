from django.urls import path, include
from Venter.views import CategoryViewset, OrganisationViewset, FileViewset

urlpatterns = [
    path('', CategoryViewset.as_view, name='category'),
    path('category/<str:organisation_name>/', CategoryViewset.as_view({
        'get': 'list'
    }), name='category'),

    path('organisation/', OrganisationViewset.as_view({
        'get': 'list'
    }), name='organisation'),

    path('file/', FileViewset.as_view({
        'get': 'list'
    })),

    path('file/<str:organisation_name>/', FileViewset.as_view({
        'get': 'retrieve'
    })),

]