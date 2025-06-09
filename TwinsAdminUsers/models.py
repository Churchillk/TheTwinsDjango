from django.db import models
from datetime import datetime
import pytz
from colorama import Fore, Back, Style
import random, string
from django.contrib.auth.models import User
# from Home.email import send_email
from django.core.exceptions import ValidationError

# timezone kenya
kenya_timezone = pytz.timezone('Africa/Nairobi')
utc_now = datetime.now(pytz.utc)# Getting the current time in UTC
kenya_time = utc_now.astimezone(kenya_timezone)

class StoreDrinks(models.Model):
    name = models.CharField("Drink Name", max_length=50, default="")
    wholesale = models.IntegerField(null=True)
    cost = models.IntegerField(default=100)
    opening_stock = models.IntegerField(default=0)
    added_stock = models.IntegerField(default=0)
    sold_stock = models.IntegerField(default=0)
    closing_stock = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Calculate the closing stock
        self.closing_stock = self.opening_stock + self.added_stock - self.sold_stock

        super(StoreDrinks, self).save(*args, **kwargs)

        # After saving, check if the closing stock is low and if an order is necessary
        if self.closing_stock < 10:
            print(f"STORE UPDATE => {Back.RED} {self.name} is running low. Stock left: {self.closing_stock} {Style.RESET_ALL}")

            from .models import StoreOrderedDrinks

            # Check if an order already exists for this drink and is still pending
            existing_order = StoreOrderedDrinks.objects.filter(drink=self, order_status='pending').first()
            if not existing_order:
                # Create an order if no pending order exists
                StoreOrderedDrinks.objects.create(
                    drink=self,
                    product_cost=self.cost,
                    payment_mode='Cash',
                    order_status='pending'
                )
                print(f"{Back.GREEN} Order made successfully {Back.RESET}")

                # Retrieve all superuser accounts
                superusers = User.objects.filter(is_superuser=True)
                superuser_emails = [user.email for user in superusers]
                if superuser_emails:
                    for su_email in superuser_emails:
                        # send_email(
                        #     drink=self.name,
                        #     date=kenya_time,
                        #     email=f'{su_email}'
                        # )
                        print(f"{Back.GREEN} Email sent successfully to {su_email} {Back.RESET}")
                else:
                    print(f'{Back.RED} No email found {Style.RESET_ALL}')

class StoreSoldDrinks(models.Model):
    drink = models.ForeignKey(StoreDrinks, on_delete=models.CASCADE, related_name='sold_drinks')
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=10, default='paid', null=False, choices=(
        ('Paid', 'Paid'),
        ('Debt', 'Debt')
    ))
    total = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    payment_mode = models.CharField(max_length=50, null=True, choices=(
        ('Till', 'Till'),
        ('Cash', 'Cash'),
        ('Debt', 'Debt'),
    ))
    customer = models.CharField(max_length=50, null=False, default='')
    customer_contact = models.CharField(max_length=20, default='+254')

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        # Calculate the total price
        self.total = self.quantity * self.drink.cost

        # Check if there is enough stock available
        available_stock = self.drink.opening_stock + self.drink.added_stock - self.drink.sold_stock
        if self.quantity > available_stock:
            raise ValidationError(f"Cannot sell {self.quantity} of {self.drink.name}. Available stock is only {available_stock}.")

        # Update the drink's sold stock and closing stock
        self.drink.sold_stock += self.quantity
        self.drink.save()  # Save the updated drink instance

        super(StoreSoldDrinks, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.drink.name}"

    class Mete:
        ordering = ['name']


class StoreExpenses(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.CharField(max_length=100, default='', null=False, blank=False)
    price = models.IntegerField(default=100, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        # timezone kenya
        kenya_timezone = pytz.timezone('Africa/Nairobi')
        utc_now = datetime.now(pytz.utc)# Getting the current time in UTC
        kenya_time = utc_now.astimezone(kenya_timezone)
        self.date = kenya_time


class StoreOrderedDrinks(models.Model):
    ORDER_STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]

    PAYMENT_MODE = [
        ('M-pesa', 'M-pesa'),
        ('Cash', 'Cash'),
    ]

    drink = models.ForeignKey(StoreDrinks, on_delete=models.CASCADE, related_name='ordered_drinks')
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    product_cost = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODE)
    start_date = models.DateTimeField('DateTime Ordered', auto_now_add=True)
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()

        # Setting timezone to Kenya
        kenya_timezone = pytz.timezone('Africa/Nairobi')
        utc_now = datetime.now(pytz.utc)
        self.start_date = utc_now.astimezone(kenya_timezone)

        super().save(*args, **kwargs)

    def generate_order_number(self):
        random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"SO->{random_chars}"

    def __str__(self):
        return f"Order {self.order_number} - {self.drink.name}"

    def clean(self):
        if self.product_cost < 0:
            raise ValidationError("Product cost cannot be negative.")
