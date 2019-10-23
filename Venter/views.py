import json
import os

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from Venter.models import File, Organisation, Draft, UserResponse, Category
from Venter.serializers import FileSerializer
from Venter.ML_Model.keyword_model.modeldriver import KeywordSimilarityMapping
from Backend.settings import MEDIA_ROOT


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

class ModelKMView(APIView):
    """
        YET TO ADD
    """
    def post(self, request):
        ml_input_json_data=json.loads(request.body)

        draft = list(ml_input_json_data.keys())[0]
        draft_name = draft.lower()

        org_obj = Organisation.objects.get(organisation_name='CIVIS')

        response=[]
        for draft, val in ml_input_json_data.items():
            for item in val['responses']:
                response.append(item['response'])
        keyword_dict={}
        for draft, val in ml_input_json_data.items():
            keyword_list = val['summary']
        keyword_dict[draft_name] = keyword_list

        sm = KeywordSimilarityMapping(draft_name, response, keyword_dict)
    
        ml_output = sm.driver()

        # create Draft, Category, UserResponses, File objects instances in Database
        draft_obj = Draft.objects.create(organisation_name=org_obj, draft_name=draft_name)
        for cat in keyword_list:
            Category.objects.create(draft_name=draft_obj, category=cat)
        for resp in response:
            UserResponse.objects.create(draft_name=draft_obj, user_response=resp)

        file_instance = File.objects.create(
            organisation_name=org_obj,
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

        Draft.objects.filter(draft_name=draft_name).update(ml_output=file_instance)

        return HttpResponse(json.dumps(ml_output), content_type="application/json")
