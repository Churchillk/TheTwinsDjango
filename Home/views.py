from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import Drinks, Expenses, SoldDrinks, OrderedDrinks, Contact, Dashboard as Dashmodel
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib import messages
from .forms import SoldDrinksForm, ExpenseForm, ContactForm
from django.views import View as DjangoView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import pytz
from datetime import datetime

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
        return context


class DrinksView(LoginRequiredMixin, ListView):
    model = Drinks
    context_object_name = 'drinks'
    template_name = 'Home/available_drinks.html'
    
class DailySalesView(LoginRequiredMixin, ListView):
    model = Drinks
    context_object_name = 'drinks'
    template_name = 'Home/available_drinks.html'

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
        return context

class OrderedDrinksView(LoginRequiredMixin, ListView):
    model = OrderedDrinks
    context_object_name = 'drinks'
    template_name = 'Home/orderd.html'

class AddedDrinksView(LoginRequiredMixin, ListView):
    model = Drinks
    context_object_name = 'drinks'
    template_name = 'Home/added.html'

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
        return render(request, 'Home/add_expense.html', {'form': form})

    def post(self, request):
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.employee = request.user
            expense.save()
            messages.success(request, 'Expense added successfuly')
            return redirect('expenses')
        
        return render(request, 'Home/add_expense.html', {'form': form})

class ContactsView(LoginRequiredMixin, ListView):
    model = Contact
    context_object_name = 'contacts'
    template_name = 'Home/contacts.html'
    
    def get(self, request, *args, **kwargs):
        contacts = Contact.objects.all()
        form = ContactForm()
        return render(request, self.template_name, {'form': form, 'contacts': contacts})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        contacts = Contact.objects.all()
        if form.is_valid():
            form.save()
            
            return redirect('contacts')

        return render(request, self.template_name, {"form": form, "contacts": contacts})

class SellDrink(DetailView):
    model = Drinks
    context_object_name = "drink"
    template_name = 'Home/selling_form.html'

    def get(self, request, *args, **kwargs):
        drink = self.get_object()  # Get the current drink object
        form = SoldDrinksForm()
        return render(request, self.template_name, {"form": form, "drink": drink})

    def post(self, request, *args, **kwargs):
        drink = self.get_object()  # Get the current drink object
        form = SoldDrinksForm(request.POST)
        if form.is_valid():
            sold_drink = form.save(commit=False)
            sold_drink.drink = drink
            sold_drink.save()

            drink.save()

            return redirect('sold_drinks')

        return render(request, self.template_name, {"form": form, "drink": drink})
    
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