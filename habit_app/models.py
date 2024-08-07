from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='related_to')
    frequency = models.PositiveIntegerField(default=1)  # в днях
    reward = models.CharField(max_length=255, null=True, blank=True)
    duration = models.PositiveIntegerField()  # в секундах
    is_public = models.BooleanField(default=False)

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError('Нельзя указать как вознаграждение, так и связанную привычку.')
        if self.duration > 120:
            raise ValidationError('Время выполнения должно быть не больше 120 секунд.')
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError('Связанная привычка должна быть приятной.')
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError('Приятная привычка не может иметь вознаграждение или связанную привычку.')
        if self.frequency < 1 or self.frequency > 7:
            raise ValidationError('Периодичность должна быть между 1 и 7 днями.')

    def __str__(self):
        return self.action




