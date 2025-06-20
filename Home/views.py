from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import Drinks, Expenses, SoldDrinks, OrderedDrinks, Contact, Dashboard as Dashmodel
from django.views.generic import DetailView, ListView
from django.views.generic.base import ContextMixin
from django.contrib import messages
from .forms import SoldDrinksForm, ExpenseForm, ContactForm
from django.views import View as DjangoView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import pytz
from django.views.generic import View
import random, string

# pdfgen
from django.http import HttpResponse
import weasyprint
from django.template.loader import render_to_string
import base64
from django.conf import settings

from django.template.loader import get_template
from datetime import datetime
from django.contrib.auth.models import User

# automatic reset
from django.db import transaction

# timezone kenya
kenya_timezone = pytz.timezone('Africa/Nairobi')
utc_now = datetime.now(pytz.utc)# Getting the current time in UTC
kenya_time = utc_now.astimezone(kenya_timezone)

class HomeView(LoginRequiredMixin, ListView):
    model = OrderedDrinks
    context_object_name = 'drinks'
    template_name = 'Home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the Dashboard instance, or create one if it doesn't exist
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)

        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        context['expenses'] = Expenses.objects.all()
        return context


class DrinksView(LoginRequiredMixin, ListView):
    model = Drinks
    context_object_name = 'drinks'
    template_name = 'Home/available_drinks.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the Dashboard instance to the context
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)
        context['dashboard'] = dashboard

        return context


class DailySalesView(LoginRequiredMixin, ListView):
    model = Drinks
    context_object_name = 'drinks'
    template_name = 'Home/available_drinks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the Dashboard instance, or create one if it doesn't exist
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)

        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        return context

class SoldDrinksView(LoginRequiredMixin, ListView):
    model = SoldDrinks
    context_object_name = 'drinks'
    template_name = 'Home/sold_drinks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # timezone kenya
        kenya_timezone = pytz.timezone('Africa/Nairobi')
        utc_now = datetime.now(pytz.utc)# Getting the current time in UTC
        kenya_time = utc_now.astimezone(kenya_timezone)
        context['kenya_time'] = kenya_time

        # Retrieve the Dashboard instance, or create one if it doesn't exist
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)

        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        return context

class OrderedDrinksView(LoginRequiredMixin, ListView):
    model = OrderedDrinks
    context_object_name = 'drinks'
    template_name = 'Home/orderd.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the Dashboard instance, or create one if it doesn't exist
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)

        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        return context


class AddedDrinksView(LoginRequiredMixin, ListView):
    model = Drinks
    context_object_name = 'drinks'
    template_name = 'Home/added.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the Dashboard instance, or create one if it doesn't exist
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)

        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        return context


class ExpensesView(LoginRequiredMixin, ListView):
    model = Expenses
    context_object_name = 'expenses'
    template_name = 'Home/expenses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the Dashboard instance, or create one if it doesn't exist
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)

        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        return context

class AddExpenses(DjangoView):
    def get(self, request):
        form = ExpenseForm()
        # Get or create the Dashboard instance
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)
        # Pass dashboard to the context
        return render(request, 'Home/add_expense.html', {'form': form, 'dashboard': dashboard})

    def post(self, request):
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.employee = request.user
            expense.save()
            messages.success(request, 'Expense added successfully')
            return redirect('expenses')

        # Get or create the Dashboard instance
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)
        # Pass dashboard to the context
        return render(request, 'Home/add_expense.html', {'form': form, 'dashboard': dashboard})


class ContactsView(LoginRequiredMixin, ListView):
    model = Contact
    context_object_name = 'contacts'
    template_name = 'Home/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the Dashboard instance, or create one if it doesn't exist
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)
        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        # Add the ContactForm to the context
        context['form'] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacts')

        # If the form is not valid, render the template with the full context
        context = self.get_context_data()
        context['form'] = form  # Pass the invalid form to the context
        return self.render_to_response(context)


class SellDrink(DetailView):
    model = Drinks
    context_object_name = "drink"
    template_name = 'Home/selling_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the Dashboard instance, or create one if it doesn't exist
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)
        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        # Add the SoldDrinksForm to the context
        context['form'] = SoldDrinksForm()
        return context

    def post(self, request, *args, **kwargs):
        drink = self.get_object()  # Get the current drink object
        form = SoldDrinksForm(request.POST)
        if form.is_valid():
            sold_drink = form.save(commit=False)
            sold_drink.drink = drink
            sold_drink.save()
            drink.save()  # Save the drink if necessary
            return redirect('sold_drinks')

        # If the form is not valid, get the full context and pass the form
        context = self.get_context_data()
        context['form'] = form  # Update the context with the invalid form
        return self.render_to_response(context)

class Debts(ListView):
    model = SoldDrinks
    context_object_name = 'debtors'
    template_name = 'Home/debts.html'

    def get_queryset(self):
        # Filter to only include debts
        return super().get_queryset().filter(status='Debt')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the Dashboard instance, or create one if it doesn't exist
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)

        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        return context

class DailyReportView(View):
    def get(self, request, *args, **kwargs):
        today = kenya_time

        # Fetch data for the report
        dashboard = Dashmodel.objects.first()
        sold_drinks = SoldDrinks.objects.filter(date__date=today)
        expenses = Expenses.objects.filter(date__date=today)
        drinks = Drinks.objects.all()
        debts = SoldDrinks.objects.filter(status='Debt')

        # Calculate totals
        total_sales = sum(drink.total for drink in sold_drinks)
        total_expenses = sum(expense.price for expense in expenses)
        stocks_added = sum(drink.added_stock for drink in drinks)
        stocks_sold = sum(drink.sold_stock for drink in drinks)

        # Encode logo as Base64
        logo_path = settings.BASE_DIR / 'Home/static/assets/images/logo.png'
        with open(logo_path, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        # Prepare the data for the preview
        context = {
            'dashboard': dashboard,
            'drinks': drinks,
            'total_sales': total_sales,
            'total_expenses': total_expenses,
            'stocks_added': stocks_added,
            'stocks_sold': stocks_sold,
            'sold_drinks': sold_drinks,
            'expenses': expenses,
            'today': today,
            'debts': debts,
            'logo_base64': logo_base64,
        }
        return render(request, 'Email/report.html', context)

    def post(self, request, *args, **kwargs):
        today = kenya_time

        # Fetch data for the report
        dashboard = Dashmodel.objects.first()
        sold_drinks = SoldDrinks.objects.filter(date__date=today)
        expenses = Expenses.objects.filter(date__date=today)
        drinks = Drinks.objects.all()
        debts = SoldDrinks.objects.filter(status='Debt')

        # Calculate totals
        total_sales = sum(drink.total for drink in sold_drinks)
        total_expenses = sum(expense.price for expense in expenses)
        stocks_added = sum(drink.added_stock for drink in drinks)
        stocks_sold = sum(drink.sold_stock for drink in drinks)

        # Encode logo as Base64
        logo_path = settings.BASE_DIR / 'Home/static/assets/images/logo.png'
        with open(logo_path, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        # Prepare the context for the PDF
        context = {
            'dashboard': dashboard,
            'debts': debts,
            'drinks': drinks,
            'total_sales': total_sales,
            'total_expenses': total_expenses,
            'stocks_added': stocks_added,
            'stocks_sold': stocks_sold,
            'sold_drinks': sold_drinks,
            'expenses': expenses,
            'today': today,
            'report_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),
            'logo_base64': logo_base64,
        }

        # Render the HTML template to a string
        html_content = render_to_string('Email/post_report.html', context)

        # Create the PDF from HTML using WeasyPrint
        pdf_file = weasyprint.HTML(string=html_content).write_pdf()

        # Create an HTTP response with the PDF content
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{today}-report.pdf"'

        # Update and reset models after report generation
        with transaction.atomic():  # Ensure all updates happen in a single transaction
            # Update `Drinks` model
            for drink in Drinks.objects.all():
                drink.opening_stock = drink.closing_stock  # Set opening stock to closing stock
                drink.added_stock = 0  # Reset added stock
                drink.sold_stock = 0  # Reset sold stock
                drink.save()

            # Delete today's SoldDrinks records
            SoldDrinks.objects.filter(date__date=today).delete()

            # Reset Expenses for today
            Expenses.objects.filter(date__date=today).delete()

            # Reset debtors
            SoldDrinks.objects.filter(status='Debt').delete()

            #reset Expenses
            Expenses.objects.filter(date__date=today).delete()

            #reset Order
            OrderedDrinks.objects.filter(start_date__date=today).delete()

        return response