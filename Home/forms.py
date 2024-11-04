from django import forms
from .models import SoldDrinks, Expenses, MessageUser, Contact

class SoldDrinksForm(forms.ModelForm):
    quantity = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Quantity'}))
    status = forms.ChoiceField(
        choices=(
            ('Paid', 'Paid'),
            ('Debt', 'Debt')
        ),
        widget=forms.Select(attrs={'class': 'form-control p_input'})
    )
    payment_mode = forms.ChoiceField(
        choices=(
            ('Till', 'Till'),
            ('Cash', 'Cash'),
            ('Debt', 'Debt')
        ),
        widget=forms.Select(attrs={'class': 'form-control p_input'})
    )
    customer = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control p_input', 'placeholder': 'Customer Name'}))
    customer_contact = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control p_input', 'placeholder': 'Customer Number 0712345678'}))
    
    class Meta:
        model = SoldDrinks
        fields = ['quantity', 'status', 'customer', 'customer_contact', 'payment_mode']
        
class ExpenseForm(forms.ModelForm):
    expense = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter The Expense'}))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter price'}))
    class Meta:
        model = Expenses
        fields = ['expense', 'price']
        
        
class ContactForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Message'}))
    name = forms.ModelChoiceField(
        queryset=Contact.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control p_input'}),
        empty_label="Select User"
    )

    class Meta:
        model = MessageUser
        fields = ['message', 'name']
        