from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from Venter.models import Category, Organisation, File
from django.contrib.admin.views.decorators import user_passes_test
from . import serializers

# Create your views here.

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def list(self, request, organisation_name):
        org_obj = Organisation.objects.get(organisation=organisation_name)
        queryset = Category.objects.filter(organisation=org_obj)
        serialized = serializers.CategorySerializer(queryset, many=True).data

        return Response(serialized)

class OrganisationViewset(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = serializers.OrganisationSerializer

    def list(self, request):
        queryset = Organisation.objects.all()
        serialized = serializers.OrganisationSerializer(queryset, many=True).data

        return Response(serialized)

class FileViewset(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = serializers.FileSerializer

    # @user_passes_test(lambda u: u.is_superuser)
    def list(self, request):
        queryset = File.objects.all()
        serialized = serializers.FileSerializer(queryset, context={'get':'filelist'}, many=True).data

        return Response(serialized)

    def retrieve(self, request, organisation_name):
        org_obj = Organisation.objects.get(organisation=organisation_name)
        queryset = File.objects.filter(organisation=org_obj)
        serialized = serializers.FileSerializer(queryset, context={'get':'organisationfilelist'}, many=True).data

        return Response(serialized)