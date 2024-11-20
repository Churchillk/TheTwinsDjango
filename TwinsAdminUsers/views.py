from django.views.generic import ListView, CreateView, View as DjangoView, UpdateView
from .models import StoreDrinks, StoreSoldDrinks, StoreExpenses, StoreOrderedDrinks
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from Home.models import (
    OrderedDrinks, Dashboard as Dashmodel, 
    Drinks as EmployeeDrinks, 
    SoldDrinks as TwinsSoldDrinks, 
    AddedDrinks, Expenses as EmployeeExpenses
    )
from django.urls import reverse_lazy
from .forms import DrinksForm, ExpenseForm
from django.shortcuts import get_object_or_404, redirect, render
from Authentications.forms import UserReg
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from Home.views import kenya_time
from django.contrib.auth import authenticate, login


def custom_admin_login(request):
    # If the user is already logged in, redirect to the admin dashboard (or home page)
    if request.user.is_authenticated:
        return redirect('admin_dash')  # Change this to whatever view you want

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_superuser:  # Check if the user is a superuser
                login(request, user)  # Log the user in
                return redirect('admin_dash')  # Redirect to the admin dashboard after login
            else:
                messages.error(request, "You must be a superuser to access the admin panel.")
                return redirect('admin_login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('admin_login')
    
    return render(request, 'Store/admin_login.html')

class DashView(LoginRequiredMixin, ListView):
    model = OrderedDrinks
    context_object_name = 'drinks'
    template_name = 'Store/dash.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve the Dashboard instance, or create one if it doesn't exist
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)
        dashdata = [dashboard.total_sales, dashboard.cash_at_hand, dashboard.cash_at_bank, dashboard.expenses, dashboard.debt]

        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        context['dashdata'] = dashdata
        context['drinksB20'] = [drink.abv for index, drink in enumerate(EmployeeDrinks.objects.all()) if drink.closing_stock <= 10 and index <= 9]
        context['drinksidB20'] = [drink.closing_stock for index, drink in enumerate(EmployeeDrinks.objects.all()) if drink.closing_stock <= 10 and index <= 9]
        return context
    

class TwinsDrinksListView(ListView):
    model = EmployeeDrinks
    template_name = 'Store/drinks.html'
    context_object_name = 'drinks'
    paginate_by = 10  # Adjust pagination as needed
    

class TwinsSoldDrinksListView(ListView):
    model = TwinsSoldDrinks
    template_name = 'Store/twins_soldrinks.html'
    context_object_name = 'store_sold_drinks'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kenya_time'] = kenya_time
        return context
    
class TwinsAddedDrinksListView(ListView):
    model = AddedDrinks
    template_name = 'Store/twins_addedrinks.html'
    context_object_name = 'drinks'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kenya_time'] = kenya_time
        return context

class TwinsOrderedDrinksListView(ListView):
    model = StoreOrderedDrinks
    template_name = 'Store/orderd.html'
    context_object_name = 'drinks'
    paginate_by = 10

class AddDrink(CreateView):
    model = EmployeeDrinks
    form_class = DrinksForm
    template_name = 'Store/add_drink.html'
    success_url = reverse_lazy('twins_drinks_list')
    

class DeleteDrink(DjangoView):
    def get(self, request, pk):
        drink = get_object_or_404(EmployeeDrinks, pk=pk)
        drink.delete()
        return redirect('twins_drinks_list') 

class UpdateDrink(UpdateView):
    model = EmployeeDrinks
    form_class = DrinksForm
    template_name = 'Store/update_drink.html'
    success_url = reverse_lazy('twins_drinks_list')
    
class TwinsExpensesListView(ListView):
    model = EmployeeExpenses
    template_name = 'Store/expenses.html'
    context_object_name = 'expenses'
    paginate_by = 10
    
class AddExpenses(DjangoView):
    def get(self, request):
        form = ExpenseForm()
        # Get or create the Dashboard instance
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)
        # Pass dashboard to the context
        return render(request, 'Store/add_expense.html', {'form': form, 'dashboard': dashboard})

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
        return render(request, 'Store/add_expense.html', {'form': form, 'dashboard': dashboard})

class AllUsers(ListView):
    model = User
    template_name = 'Store/users.html'
    context_object_name = 'users'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heads'] = [field.name for field in User._meta.get_fields()]
        context['usernames'] = [user.username for user in User.objects.all()]
        context['userids'] = [user.id for user in User.objects.all()]
        context['admins'] = [user.username for user in User.objects.all() if user.is_superuser]
        context['adminsid'] = [user.id for user in User.objects.all() if user.is_superuser]
        return context
    

def add_user(request):
    pass
    if request.method == "POST":
        form = UserReg(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get("username")
            form.save()
            messages.success(request, f"account created for {user} successfuly")
            return redirect("users")
        else:
            messages.warning(request, "account not created")
    else:
        form = UserReg()
            
    template = loader.get_template("Store/add_user.html")
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))

class DeleteUser(DjangoView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect('users') 

class Debts(ListView):
    model = TwinsSoldDrinks
    context_object_name = 'debtors'
    template_name = 'Store/debts.html'
    
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

