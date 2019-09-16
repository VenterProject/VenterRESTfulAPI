from django.shortcuts import render
from rest_framework import viewsets
from Venter.models import Category, Organisation
from . import serializers

# Create your views here.

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

class OrganisationViewset(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = serializers.OrganisationSerializer