from rest_framework import serializers
from . import models

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('category', 'organisation',)
        model = models.Category

class OrganisationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('organisation',)
        model = models.Organisation