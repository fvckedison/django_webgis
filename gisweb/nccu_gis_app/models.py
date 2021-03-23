from django.db import models

# Create your models here.
class imgData(models.Model):	
    title = models.CharField(max_length=60, null=False, default = "")	
    content = models.TextField(null=False, default = "")	
    type = models.CharField(max_length=20, null=False, default = "")
    purl = models.CharField(max_length=100, null=False, default = "")
    create_at =  models.DateTimeField(auto_now_add=True)	
    lon = models.CharField(max_length=20, null=False, default = "")
    lat = models.CharField(max_length=20, null=False, default = "")

    def __str__(self):		
        return self.title	