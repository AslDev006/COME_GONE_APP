from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class UserModel(models.Model):
    user = models.IntegerField(
        primary_key=True,
        validators=[MinValueValidator(1), MaxValueValidator(127)]
    )
    full_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user} - {self.full_name}'

class ComeGoneTimeModel(models.Model):
    user = models.ForeignKey(UserModel, related_name='times', on_delete=models.CASCADE)
    status = models.BooleanField(null=True, blank=True)
    time = models.DateTimeField()

    def __str__(self):
        formatted_time = self.time.strftime('%d-%m-%Y %H:%M')
        event = "Keldi" if self.status else "Ketdi"
        return f"{self.user.user} ({self.user.full_name}) {formatted_time} da {event.lower()}"

    class Meta:
        verbose_name = "Keldi-Ketdi Yozuvi"
        verbose_name_plural = "Keldi-Ketdi Yozuvlari"
        ordering = ['-time']