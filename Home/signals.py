# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import SoldDrinks, Expenses, Dashboard
from django.db.models import Sum

def update_dashboard(expense_amount=0, is_expense_deleted=False):
    # Get or create the dashboard instance (assuming a single dashboard entry)
    dashboard, created = Dashboard.objects.get_or_create(pk=1)

    # Calculate cash at hand: Total of all sold drinks paid by Cash
    cash_sales = SoldDrinks.objects.filter(payment_mode='Cash').aggregate(total_cash=Sum('total'))
    dashboard.cash_at_hand = cash_sales['total_cash'] or 0

    # Calculate cash at bank: Total of all sold drinks paid by Till
    bank_sales = SoldDrinks.objects.filter(payment_mode='Till').aggregate(total_bank=Sum('total'))
    dashboard.cash_at_bank = bank_sales['total_bank'] or 0

    # Calculate debt: Total of all sold drinks with payment_mode 'Debt'
    debt_sales = SoldDrinks.objects.filter(payment_mode='Debt').aggregate(total_debt=Sum('total'))
    dashboard.debt = debt_sales['total_debt'] or 0

    # Calculate total expenses: Sum of all expenses
    total_expenses = Expenses.objects.aggregate(total_expenses=Sum('price'))
    dashboard.expenses = total_expenses['total_expenses'] or 0

    # Adjust cash at hand based on expenses
    if is_expense_deleted:
        # If an expense was deleted, add back the expense amount
        dashboard.cash_at_hand += expense_amount
    else:
        # If an expense was added, subtract the expense amount
        dashboard.cash_at_hand -= expense_amount

    # Calculate total sales: Sum of all sales (Cash + Till)
    dashboard.total_sales = dashboard.cash_at_hand + dashboard.cash_at_bank

    # Save the updated dashboard
    dashboard.save()

@receiver(post_save, sender=SoldDrinks)
@receiver(post_delete, sender=SoldDrinks)
def update_dashboard_on_sold_drinks(sender, instance, **kwargs):
    update_dashboard()

@receiver(post_save, sender=Expenses)
def update_dashboard_on_expenses(sender, instance, **kwargs):
    update_dashboard(expense_amount=instance.price, is_expense_deleted=False)

@receiver(post_delete, sender=Expenses)
def update_dashboard_on_expenses_delete(sender, instance, **kwargs):
    update_dashboard(expense_amount=instance.price, is_expense_deleted=True)
