from django.db import models
from datetime import datetime

# Create your models here.

class Organisation(models.Model):
    organisation = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.organisation}'


class Category(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    category = models.CharField(max_length = 1000)
    
    def __str__(self):
        return f'{self.category}'

class File(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    ckpt_date = models.DateTimeField(verbose_name="Upload Date", default=datetime.now)
    has_prediction = models.BooleanField(default=False)
    output_file_json = models.FileField(upload_to="")
    wordcloud_data = models.FileField(upload_to="")
