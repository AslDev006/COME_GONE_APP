from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import timedelta

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


class MonthlyWorkSummary(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='monthly_summaries')
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    total_hours_worked = models.DurationField(default=timedelta(0))
    total_days_worked = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Oylik Ish Vaqti Hisoboti"
        verbose_name_plural = "Oylik Ish Vaqti Hisobotlari"
        unique_together = ('user', 'year', 'month')
        ordering = ['-year', '-month', 'user']

    def __str__(self):
        total_seconds = self.total_hours_worked.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{self.user.full_name} - {self.year}/{self.month:02d} - {self.total_days_worked} kun ({hours} soat {minutes} daqiqa)"