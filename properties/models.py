from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from django_ckeditor_5.fields import CKEditor5Field

from builders.models import Builder

# Country, State, and City Models (unchanged)

class State(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return self.name

class City(models.Model):
    state = models.ForeignKey(State, related_name='cities', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return f"{self.name}, {self.state.name}"

    class Meta:
        verbose_name_plural = "Cities"


# Property Model
class Property(models.Model):
    PROPERTY_TYPES = [
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Sold', 'Sold'),
        ('Rented', 'Rented'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    description = CKEditor5Field(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    area = models.FloatField(help_text="Area in square feet")
    builder = models.ForeignKey(Builder, related_name='builder', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=255)
    location = models.URLField(blank=True)
    city = models.ForeignKey(City, related_name='properties', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    # New relationships with features, amenities, and floor plans
    features = models.ManyToManyField('Feature', blank=True)
    amenities = models.ManyToManyField('Amenity', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "properties"

    def set_slug(self):
        """
        Auto-populate an empty slug field from the Entry title
        """
        if not self.slug:
            # Where self.name is the field used for 'pre-populate from'
            self.slug = slugify(self.title)

    # Restricting Property Creation to Admin
    def save(self, *args, **kwargs):
        self.set_slug()
        if not self.pk and not User.objects.filter(is_staff=True).exists():
            raise PermissionError("Only admin can add or modify properties")
        super().save(*args, **kwargs)


# Floor Plan Model (modified related_name for reverse accessor)
class FloorPlan(models.Model):
    property = models.ForeignKey(Property, related_name='floor_plans', on_delete=models.CASCADE)
    floor_plan_file = models.FileField(upload_to='floor_plans/', help_text="Upload a PDF or image of the floor plan.")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Floor Plan for {self.property.title}"


# Property Image Model
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='property_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.property.title}"


# Feature Model (for property-specific features like 'Garden', 'Swimming Pool', etc.)
class Feature(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Amenity Model (for general amenities like 'Wi-Fi', 'Parking', etc.)
class Amenity(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Amenities'





# Enquiry Model
# class Enquiry(models.Model):
#
#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('Working', 'Working'),
#         ('Resolved', 'Resolved'),
#     ]
#
#     client = models.CharField(max_length=255)
#     property = models.ForeignKey(Property, related_name='enquiries', on_delete=models.CASCADE)
#     message = models.TextField()
#     enquiry_date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available')
#
#     def __str__(self):
#         return f"Enquiry for {self.property.title} from {self.client.user.username}"
