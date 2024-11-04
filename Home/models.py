from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
import random, string
from colorama import Fore, Style, Back
import pytz
from .email import send_email
from django.contrib import messages

# timezone kenya
kenya_timezone = pytz.timezone('Africa/Nairobi')
utc_now = datetime.now(pytz.utc)# Getting the current time in UTC
kenya_time = utc_now.astimezone(kenya_timezone)

class Dashboard(models.Model):
    cash_at_hand = models.IntegerField(default=0, null=True)
    cash_at_bank = models.IntegerField(default=0, null=True)
    expenses = models.IntegerField(default=0, null=True)
    total_sales = models.IntegerField(default=0, null=True)
    debt = models.IntegerField(default=0, null=True)

    def __str__(self):
        return "Dashboard Overview"


class Drinks(models.Model):
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

        # Check if the closing stock is below the threshold of 6
        print(f"Closing stock for {self.name}: {self.closing_stock}")
        if self.closing_stock < 6:
            print(f"{Back.CYAN} {self.name} is running low. Stock left: {self.closing_stock} {Style.RESET_ALL}")

            # Check if an order already exists for this drink and is still pending
            from .models import OrderedDrinks
            existing_order = OrderedDrinks.objects.filter(drink=self, order_status='pending').first()

            if not existing_order:
                # Create an order if no pending order exists
                OrderedDrinks.objects.create(
                    drink=self,
                    product_cost=self.cost,
                    payment_mode='Cash',  # Default payment mode, can be changed as needed
                    order_status='pending'
                )
                print(f"{Back.GREEN} order made successfuly {Back.RESET}")
                send_email(
                    drink=self.name,
                    date=kenya_time,
                    email='churchilkodhiambo@gmail.com'
                )
                print(f"{Back.RED} Email Sent successfuly {Back.RESET}")

        super(Drinks, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class SoldDrinks(models.Model):
    drink = models.ForeignKey(Drinks, on_delete=models.CASCADE, related_name='sold_drinks')
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

        super(SoldDrinks, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.drink.name}"


class Expenses(models.Model):
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

        super(Expenses, self).save(*args, **kwargs)

class OrderedDrinks(models.Model):
    ORDER_STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]
    
    PAYMENT_MODE = [
        ('M-pesa', 'M-pesa'),
        ('Cash', 'Cash'),
    ]
    
    drink = models.ForeignKey('Drinks', on_delete=models.CASCADE, related_name='ordered_drinks')
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    product_cost = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODE)
    start_date = models.DateTimeField('DateTime Ordered', auto_now_add=True)
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES)

    def save(self, *args, **kwargs):
        # Generate a unique order number if it hasn't been set yet
        if not self.order_number:
            self.order_number = self.generate_order_number()
        
        # timezone kenya
        kenya_timezone = pytz.timezone('Africa/Nairobi')
        utc_now = datetime.now(pytz.utc)# Getting the current time in UTC
        kenya_time = utc_now.astimezone(kenya_timezone)
        self.start_date = kenya_time
        
        super().save(*args, **kwargs)
        

    def generate_order_number(self):
        # Generate a random string of 6 characters (letters and digits)
        random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"ORD-{random_chars}"

    def __str__(self):
        return f"Order {self.order_number} - {self.drink.name}"

    def clean(self):
        # Custom validation logic can be added here
        if self.product_cost < 0:
            raise ValidationError("Product cost cannot be negative.")
        
class Contact(models.Model):
    name = models.CharField(max_length=50, default="")
    contact = models.CharField(max_length=20, default='+254')
    role = models.CharField(max_length=50, default='Supplier')
    location = models.CharField(max_length=50, default='Nairobi')
    picture = models.ImageField(upload_to='Contact', null=True, default='Contact/default.png')
    
    def __str__(self):
        return f"{self.name} -> {self.role}"
    

class MessageUser(models.Model):
    name = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)
    message = models.TextField(null=True)
    