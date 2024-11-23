from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from Home import models as HomeModels
from .models import Profile

class UserReg(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control p_input', 'placeholder': 'Confirm Password'}))
    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': "form-check-input", 'type': "checkbox"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_superuser']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['is_superuser']:
            user.is_superuser = True
            user.is_staff = True  # Superusers are also staff members
        if commit:
            user.save()
        return user
    
class UserChange(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Password'}), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control p_input', 'placeholder': 'Confirm Password'}), required=False)
    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': "form-check-input", 'type': "checkbox"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_superuser']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['is_superuser']:
            user.is_superuser = True
            user.is_staff = True  # Superusers are also staff members
        if commit:
            user.save()
        return user
    
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Remove labels and add placeholders for username and password fields
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs.update({
            'class': 'form-control p_input',
            'placeholder': 'Enter Username'
        })
        
        self.fields['password'].label = ''
        self.fields['password'].widget.attrs.update({
            'class': 'form-control p_input',
            'placeholder': 'Enter Password'
        })
       
class ContactForm(forms.Form):
    Name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    Email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    Title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title'}))
    Description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Comment', 'rows': 4}))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        
        # Remove labels for all fields
        self.fields['Name'].label = ''
        self.fields['Email'].label = ''
        self.fields['Title'].label = ''
        self.fields['Description'].label = ''

class ProfileForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control p-4', 'placeholder': 'Enter Name'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control p-4', 'placeholder': 'Enter Bio'}))
    birthday = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control p-4', 'type': 'date', 'placeholder': 'Select Birthday'}))
    degree = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control p-4', 'placeholder': 'Enter Degree'}))
    experience = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control p-4', 'placeholder': 'Enter Years of Experience'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control p-4', 'placeholder': 'Enter Phone Number'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control p-4', 'placeholder': 'Enter Email Address'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control p-4', 'placeholder': 'Enter Address'}))
    picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control p-4'}))
    institution = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control p-4', 'placeholder': 'Enter Institution'}))

    class Meta:
        model = Profile
        fields = ['name', 'bio', 'birthday', 'degree', 'experience', 'phone', 'email', 'address', 'institution', 'picture']