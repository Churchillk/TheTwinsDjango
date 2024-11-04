
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    name = models.CharField(max_length=255, default='Jkuat Student')
    birthday = models.DateField(default='1990-04-01')
    degree = models.CharField(max_length=100, default='Course')
    experience = models.PositiveIntegerField(default=10)  # Assuming experience in years
    phone = models.CharField(max_length=20, default='+012 345 6789')
    email = models.EmailField(default='info@example.com')
    address = models.CharField(max_length=255, default='your address')
    institution = models.CharField(default="JKUAT", max_length=50, null=True)
    picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg')
    bio = models.TextField(default="Lorem, ipsum dolor sit amet consectetur adipisicing elit. Nemo, dolores, amet possimus ea, hic reiciendis sed porro voluptatem voluptatum architecto inventore! Earum sint repellat, soluta dicta qui quos quasi iure.")

    def __str__(self):
        return self.name