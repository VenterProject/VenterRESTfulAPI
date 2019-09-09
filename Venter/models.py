from django.db import models

# Create your models here.

class Category(models.Model):
    """
    A Category list associated with each organisation.
    Eg: Organisation xyz may contain categories such as- hawkers, garbage etc

    # Create a category instance
    >>> Category.objects.create(category="hawkers")
    """
    category = models.CharField(
        max_length=200
    )

    class Meta:
        """
        Declares a plural name for Category model
        """
        verbose_name_plural = 'Category'