import json
import os
from datetime import date, datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework_swagger.views import get_swagger_view
from rest_framework.response import Response
from rest_framework.views import APIView

from Backend.settings import MEDIA_ROOT
from Venter.models import (Category, File, Organisation, UserCategory,
                           UserComplaint)
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
    """
    Arguments:  1) APIView: Handles POST requests of type DRF Request instance. 
    Methods:    1) post: This handler is utilized for ICMC App to send json Input to ML API endpoint
    Workflow:   1) On retrieval of DICT containing one or more complaint-category pair, the complaints are separately retrieved
                   to be fed into the method get_top_3_cats_with_prob(complaint_description).
                2) The ClassificationService class handles the request to the ICMC ML model.
                3) The output/ directory is created in order to save the ML model output results based on org_name, ckpt_date.
                4) The input category-complaint pairs are stored (unique pairs) in UserCategory, UserComplaint models required for Input to
                   wordcloud API.
                5) The output from the ICMC ML model is sent to the ICMC application as an HTTPResponse (JSON format).

    """
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

        for category, complaint in zip(list(ml_input_json_data.values()), list(ml_input_json_data.keys())):
            if UserCategory.objects.filter(organisation_name=org_name, user_category=category).exists():
                cat_queryset = UserCategory.objects.filter(organisation_name=org_name)
                for cat in cat_queryset:
                    db_complaint = UserComplaint.objects.get(user_category=cat)
                    str_complaint = str(db_complaint.user_complaint)
                    if (str_complaint.lower()==complaint.lower()):
                        flag = 1
                        break
                    else:
                        flag = 0
                if flag==0:
                    user_category_instance = UserCategory.objects.create(
                        organisation_name=org_name,
                        user_category=category,
                    )
                    user_category_instance.save()
                    user_complaint_instance = UserComplaint.objects.create(
                        user_category=user_category_instance,
                        user_complaint=complaint,
                    )
                    user_complaint_instance.save()
            else:
                user_category_instance = UserCategory.objects.create(
                    organisation_name=org_name,
                    user_category=category,
                )
                user_category_instance.save()
                user_complaint_instance = UserComplaint.objects.create(
                    user_category=user_category_instance,
                    user_complaint=complaint,
                )
                user_complaint_instance.save()
        return HttpResponse(json.dumps(ml_output), content_type="application/json")

schema_view = get_swagger_view(title="Swagger Docs")

