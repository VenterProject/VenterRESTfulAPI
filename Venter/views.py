import json
import os

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from Backend.settings import MEDIA_ROOT
from Venter.models import Category, File, Organisation, UserComplaint, UserCategory
from Venter.serializers import (CategorySerializer, FileSerializer,
                                OrganisationSerializer)

from .ML_Model.ICMC.model.ClassificationService import ClassificationService
from .wordcloud import generate_wordcloud


class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects
    serializer_class = OrganisationSerializer

    @classmethod
    def list(cls, request):
        """
            OrganisationViewSet for getting a list of organisations associated with the application
        """
        queryset = Organisation.objects.all()

        # Serialize and return
        serialized = OrganisationSerializer(queryset, context={'get': 'list'}, many=True).data

        return Response(serialized)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects
    serializer_class = CategorySerializer

    @classmethod
    def list(cls, request):
        """
            CategoryViewSet for getting a list of categories present in all organisations registered with the application
        """
        queryset = Category.objects.all()

        # Serialize and return
        serialized = CategorySerializer(queryset, context={'get': 'list'}, many=True).data

        return Response(serialized)

    @classmethod
    def retrieve(cls, request, organisation):
        """
            CategoryViewSet for retrieving a list of categories associated with an organisation
        """
        org_name = Organisation.objects.get(organisation_name=organisation)
        queryset = Category.objects.filter(organisation_name=org_name)

        # Serialize and return
        serialized = CategorySerializer(queryset, context={'get': 'retrieve'}, many=True).data

        return Response(serialized)

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects
    serializer_class = FileSerializer

    @classmethod
    def list(cls, request):
        """
            FileViewSet for getting a list of output files predicted by the ML model
            for the input data(citizen responses) input by all organisations registered with the application
        """
        queryset = File.objects.all()

        # Serialize and return
        serialized = FileSerializer(queryset, context={'get': 'list'}, many=True).data

        return Response(serialized)

    @classmethod
    def retrieve(cls, request, organisation):
        """
            FileViewSet for retrieving a list of output files predicted by the ML model
            for the input data(citizen responses) input by a specific organisation
        """
        org_name = Organisation.objects.get(organisation_name=organisation)
        queryset = File.objects.filter(organisation_name=org_name).order_by('ckpt_date')

        # Serialize and return
        serialized = FileSerializer(queryset, context={'get': 'retrieve'}, many=True).data

        return Response(serialized)


class ModelCPView(APIView):
    def post(self, request):
        ml_input_json_data=json.loads(request.body)
        complaint_description = list(ml_input_json_data.keys())
        model = ClassificationService()
        category_list = model.get_top_3_cats_with_prob(complaint_description)

        ml_output = []

        for complaint, cat in zip(complaint_description, category_list):
            row_dict = {}
            cat_list = []
            cat_list = list(cat.keys())
            row_dict['complaint'] = complaint
            row_dict['category'] = cat_list
            ml_output.append(row_dict)

        org_name = Organisation.objects.get(organisation_name='ICMC')
        file_instance = File.objects.create(
            organisation_name=org_name,
            has_prediction = True,
        )
        file_instance.save()

        output_directory_path = os.path.join(MEDIA_ROOT, f'{file_instance.organisation_name}/{file_instance.ckpt_date.date()}/output')
        if not os.path.exists(output_directory_path):
            os.makedirs(output_directory_path)

        file_id = str(file_instance.id)
        output_file_json_name = 'ml_output__'+file_id+'.json'
        output_file_json_path = os.path.join(output_directory_path, output_file_json_name)

        with open(output_file_json_path, 'w') as temp:
            json.dump(ml_output, temp)
        file_instance.output_file_json = output_file_json_path
        file_instance.save()

        for complaint, category in zip(list(ml_input_json_data.keys()), list(ml_input_json_data.values())):
            user_complaint_instance = UserComplaint.objects.create(
                organisation_name=org_name,
                user_complaint=complaint,
            )
            user_complaint_instance.save()
            user_category_instance = UserCategory.objects.create(
                user_complaint=user_complaint_instance,
                user_category=category,
            )
            user_category_instance.save()

        return HttpResponse(json.dumps(ml_output), content_type="application/json")
