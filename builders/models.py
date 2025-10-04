from django.db import models
from django.template.defaultfilters import slugify
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.

class Builder(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    description = CKEditor5Field(blank=True)
    logo = models.ImageField(upload_to='builders/logos/', blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def set_slug(self):
        """
        Auto-populate an empty slug field from the Entry title
        """
        if not self.slug:
            # Where self.name is the field used for 'pre-populate from'
            self.slug = slugify(self.name)

    def save(self, *args, **kwargs):
        self.set_slug()
        super().save(*args, **kwargs)