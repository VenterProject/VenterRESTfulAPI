import json
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Venter.models import Category, Organisation, File
from Venter.serializers import CategorySerializer, OrganisationSerializer, FileSerializer
from .wordcloud import generate_wordcloud
from .ML_Model.ICMC.model.ClassificationService import ClassificationService
from django.http import HttpResponse
from rest_framework.views import APIView

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

        with open("output_from_ml.json", 'w') as temp:
            json.dump(ml_output, temp)

        '''
            building code

        # output_directory_path = os.path.join(MEDIA_ROOT, f'{filemeta.uploaded_by.organisation_name}/{filemeta.uploaded_by.user.username}/{filemeta.uploaded_date.date()}/output')

        # if not os.path.exists(output_directory_path):
        #     os.makedirs(output_directory_path)

        # print(output_directory_path)
        # output_file_path_json = os.path.join(output_directory_path, 'ml_output_result.json')
        # output_file_path_xlsx = os.path.join(output_directory_path, 'wordcloud_output_result.json')            

        

        # org_name = Organisation.objects.get(organisation_name='ICMC')
        # file_instance = File.objects.create(
        #     organisation_name=org_name,
        #     has_prediction = True,
        #     output_file_json = 
        # )
        # file_instance.save()

        '''    

        # NOTE -------------------------------------------------
        # filemeta.output_file_json = output_file_path_json

        # save ml output in filefield json
        # save input to API in wordcloud fieldfield
        # change category extraction in import graph

        return HttpResponse(json.dumps(ml_output), content_type="application/json")


# @require_http_methods(["POST"])
# def modelWCView(request, pk):
#     filemeta = File.objects.get(pk=pk)
#     output_file_json = json.load(filemeta.output_file_json)

    
    # wordcloud_output = generate_wordcloud(input_wordcloud)
    # with open(wordcloud_data_path_json, 'w') as temp:
    #     json.dump(output_dict, temp)

    # filemeta.wordcloud_data = wordcloud_data_path_json
    # filemeta.save()
