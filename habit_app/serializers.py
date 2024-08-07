from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'


    def validate(self, data):
        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError('Нельзя указать как вознаграждение, так и связанную привычку.')
        if data.get('duration') > 120:
            raise serializers.ValidationError('Время выполнения должно быть не больше 120 секунд.')
        if data.get('related_habit') and not data.get('related_habit').is_pleasant:
            raise serializers.ValidationError('Связанная привычка должна быть приятной.')
        if data.get('is_pleasant') and (data.get('reward') or data.get('related_habit')):
            raise serializers.ValidationError('Приятная привычка не может иметь вознаграждение или связанную привычку.')
        if data.get('frequency') < 1 or data.get('frequency') > 7:
            raise serializers.ValidationError('Периодичность должна быть между 1 и 7 днями.')
        return data