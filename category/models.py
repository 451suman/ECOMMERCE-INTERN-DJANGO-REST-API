from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=500)
    parent_category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
