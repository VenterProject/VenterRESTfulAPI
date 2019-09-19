from datetime import datetime
from django.core.validators import FileExtensionValidator
from django.db import models


class Organisation(models.Model):
    """
        An organisation that is associated with Venter application.
        Eg: xyz is an organisation associated with Venter
        # Create an organisation
        >>> organisation_1 = Organisation.objects.create(organisation_name="xyz")
    """
    organisation_name = models.CharField(
        max_length=200,
        primary_key=True,
    )

    def __str__(self):
        return self.organisation_name

    class Meta:
        """
        Declares a plural name for Organisation model
        """
        verbose_name_plural = 'Organisation'
    

class Category(models.Model):
    """
        A Category list associated with each organisation.
        Eg: Organisation xyz may contain categories in the csv file such as- hawkers, garbage etc
        # Create a category instance
        >>> Category.objects.create(organisation_name="xyz", category="hawkers")
    """
    organisation_name = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
    )
    category = models.CharField(
        max_length=200
    )

    class Meta:
        """
        Declares a plural name for Category model
        """
        verbose_name_plural = 'Category'

class File(models.Model):
    """
        An output File created for a particular organisation.
        Eg: Organisation 'xyz' may have two or more output files per month.
        # Create a file instance
        >>> File.objects.create(organisation_name=xyz, ckpt_date = "Jan. 29, 2019, 7:59 p.m.", has_prediction=False)
    """        
    organisation_name = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
    )
    ckpt_date = models.DateTimeField(
        default=datetime.now,
    )
    has_prediction = models.BooleanField(
        default=False,
    )
    output_file_json = models.FileField(
        blank=True, 
        max_length=255,
        validators=[FileExtensionValidator(allowed_extensions=['json'],
    )
    wordcloud_data = models.FileField(
        blank=True,
        max_length=255,
        validators=[FileExtensionValidator(allowed_extensions=['json'],
    )

    class Meta:
        """
        Declares a plural name for File model
        """
        verbose_name_plural = 'File'

