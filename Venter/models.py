from django.db import models

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

