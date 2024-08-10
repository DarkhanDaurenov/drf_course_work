from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Habit
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from django.urls import reverse
from unittest.mock import patch
from .tasks import send_habit_reminder


# Тесты для моделей
class HabitModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')

    def test_create_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Park",
            time="12:00:00",
            action="Run",
            pleasantness=False,
            frequency=1,
            reward="Ice Cream",
            duration=2,
            public=True
        )
        self.assertEqual(str(habit), f'Habit: {habit.action} at {habit.time} in {habit.place}')
        self.assertEqual(habit.user, self.user)


# Тесты для валидации модели
class HabitModelValidationTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')

    def test_invalid_habit_duration(self):
        habit = Habit(
            user=self.user,
            place="Park",
            time="12:00:00",
            action="Run",
            pleasantness=False,
            frequency=1,
            reward="Ice Cream",
            duration=3,  # Должно выдать ошибку, так как больше 2 минут
            public=True
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()


# Тесты для API эндпоинтов
class HabitAPITest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_create_habit(self):
        url = reverse('habit-list')
        data = {
            "place": "Gym",
            "time": "07:00:00",
            "action": "Workout",
            "pleasantness": False,
            "frequency": 1,
            "reward": "Protein Shake",
            "duration": 2,
            "public": True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_habit_list(self):
        url = reverse('habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


# Тесты для напоминаний через Telegram
class HabitReminderTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.habit = Habit.objects.create(
            user=self.user,
            place="Home",
            time="08:00:00",
            action="Drink Water",
            pleasantness=False,
            frequency=1,
            duration=2,
            public=True
        )

    @patch('your_app.tasks.Bot.send_message')
    def test_send_habit_reminder(self, mock_send_message):
        send_habit_reminder(self.habit.id)
        mock_send_message.assert_called_once_with(
            chat_id=self.user.profile.telegram_chat_id,
            text=f'Напоминание: {self.habit.action} в {self.habit.time} в {self.habit.place}.'
        )
