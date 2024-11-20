from django import forms
from .models import StoreDrinks
from Home.models import Drinks as EmployeeDrinks, Expenses as EExpenses

class AddDrinksStoreForm(forms.ModelForm):
    drink = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Quantity'}))
    added_stock = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Quantity'}))

    
    class Meta:
        model = StoreDrinks
        fields = ['drink', 'added_stock']
        

class DrinksForm(forms.ModelForm):
    class Meta:
        model = EmployeeDrinks
        fields = ['name', 'wholesale', 'cost', 'opening_stock', 'added_stock', 'sold_stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Drink Name'}),
            'wholesale': forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Wholesale Price'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Cost'}),
            'opening_stock': forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Opening Stock'}),
            'added_stock': forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Added Stock'}),
            'sold_stock': forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Sold Stocks'}),
        }

class ExpenseForm(forms.ModelForm):
    expense = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter The Expense'}))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter price'}))
    class Meta:
        model = EExpenses
        fields = ['expense', 'price']