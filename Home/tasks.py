# # your_app/tasks.py
# from django_q.tasks import schedule
# from django_q.models import Schedule
# from Home.models import Expenses
# from django.utils import timezone
# import pytz

# def reset_expenses():
#     # Set timezone for Kenya
#     kenya_timezone = pytz.timezone('Africa/Nairobi')
#     today = timezone.now().astimezone(kenya_timezone).date()
    
#     # Delete all entries in the Expenses table
#     deleted_count, _ = Expenses.objects.all().delete()
#     print(f"Deleted {deleted_count} expenses at {today}")

#     # Schedule the task (if not already scheduled)
#     Schedule.objects.create(
#         func='your_app.tasks.reset_expenses',  # Path to the reset function
#         schedule_type=Schedule.DAILY,          # Run daily
#         next_run=timezone.now().astimezone(kenya_timezone).replace(hour=7, minute=0, second=0),  # 7:00 AM Kenya time
#     )
