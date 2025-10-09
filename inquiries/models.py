from django.db import models

# Create your models here.


class Inquiry(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Working', 'Working'),
        ('Resolved', 'Resolved'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
            return f"Enquiry from {self.full_name}-({self.email})"
