from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class UserModel(models.Model):
    user = models.IntegerField(
        primary_key=True,
        validators=[
            MinValueValidator(100),  
            MaxValueValidator(999)   
        ]
    )
    full_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f'{self.user}'