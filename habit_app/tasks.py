from celery import shared_task
from telegram import Bot
from .models import Habit
from django.utils import timezone

bot = Bot(token='7385121860:AAGnUxXPsx0RE6O3_tce_ox7Pg03mkpxWbA')

@shared_task
def send_habit_reminder(habit_id):
    habit = Habit.objects.get(id=habit_id)
    user = habit.user
    message = f'Напоминание: {habit.action} в {habit.time} в {habit.place}.'
    bot.send_message(chat_id=user.profile.telegram_chat_id, text=message)

def schedule_habit_reminders():
    habits = Habit.objects.filter(time=timezone.now().time())
    for habit in habits:
        send_habit_reminder.apply_async(args=[habit.id], eta=habit.time)