from rest_framework import serializers
from . import models
from datetime import date
from datetime import datetime

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('category', 'organisation',)
        model = models.Category


class OrganisationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('organisation',)
        model = models.Organisation


class FileSerializer(serializers.ModelSerializer):

    ckpt_date = serializers.DateTimeField(format="%d %B %Y")

    # ckpt_date = datetime.now()

    # ckpt_date = ckpt_date.strftime("%d %B %Y")

    class Meta:
        model = models.File
        fields = ('id','organisation', 'ckpt_date',)
        