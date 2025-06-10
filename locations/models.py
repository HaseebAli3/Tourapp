from django.db import models
from django.conf import settings

class Location(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location_url = models.URLField(max_length=500, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='locations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Three image fields
    image1 = models.ImageField(upload_to='location_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='location_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='location_images/', blank=True, null=True)

    def __str__(self):
        return self.name