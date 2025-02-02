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
    def __str__(self):
        return f'{self.user} {self.full_name}'
    

class ComeGoneTimeModel(models.Model):
    user = models.ForeignKey(UserModel, related_name='time', on_delete=models.CASCADE)
    status = models.BooleanField(null=True, blank=True)
    time = models.DateTimeField()
    def __str__(self):
            formatted_time = self.time.strftime('%d-%m %H:%M')
            if self.status==True:
                return f"{self.user} {formatted_time}da keldi"
            else:
                return f"{self.user} {formatted_time}da ketdi"