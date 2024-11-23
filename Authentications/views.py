from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader
from django.views.generic import *
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from .forms import *
from django.utils import timezone

from django.contrib import messages
from . import models as UserModels
from Home import models as HomeModels

#registration login libraries
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
import random

@login_required
def register(request):
    pass
    if request.method == "POST":
        form = UserReg(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get("username")
            form.save()
            messages.success(request, f"account created for {user} successfuly")
            return redirect("login")
        else:
            messages.error(request, "account not created")
    else:
        form = UserReg()
            
    template = loader.get_template("Auth/register.html")
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))

class CustomLoginView(LoginView):
    template_name = "Auth/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        userv = self.request.user
        attacheev, created = UserModels.Profile.objects.get_or_create(user=userv)
        if userv.is_authenticated:
            try:
                profile = userv.profile
                if not self.is_profile_complete(attacheev):
                    return reverse_lazy('profile_update')
            except HomeModels.Profile.DoesNotExist:
                return reverse_lazy('profile_update')
        return reverse_lazy('home')
    
    def is_profile_complete(self, profile):
        # Define the criteria for an incomplete profile
        return all([
            profile.name and profile.birthday and profile.degree and profile.experience and profile.phone and profile.email and profile.address
        ])
    
class Profile(LoginRequiredMixin, DetailView):
    model = UserModels.Profile
    template_name = "Auth/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        # Fetch the Profile object for the currently logged-in user
        return get_object_or_404(UserModels.Profile, user=self.request.user)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserModels.Profile
    form_class = ProfileForm
    template_name = "Auth/profile_edit.html"
    success_url = reverse_lazy('profile')  # Make sure this URL is defined in your urls.py

    def get_object(self, queryset=None):
        return get_object_or_404(UserModels.Profile, user=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return super().get_success_url()


class MainLogoutView(LoginRequiredMixin, LogoutView):
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.request.method == 'GET':
            request.session.flush()
            auth_logout(request)
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class AdminLogoutView(LoginRequiredMixin, LogoutView):
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.request.method == 'GET':
            request.session.flush()
            auth_logout(request)
            return redirect('admin_login')
        return super().dispatch(request, *args, **kwargs)

@login_required
def Contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
             # Extract form data
            user = form.cleaned_data['Name']
            user_email = form.cleaned_data['Email']
            user_title = form.cleaned_data['Title']
            user_description = form.cleaned_data['Description']
            
            # Create a new Book instance
            UserComment = HomeModels.ContactModel(Name=user, Email=user_email,   Title=user_title, Description=user_description, Date=timezone.now().strftime("%Y-%m-%d %H:%M"))
            UserComment.save()
            messages.success(request, "Comment submitted Successful")
            return redirect ('home')
        else:
            messages.error(request, "Comment Failled")
    else:
        form = ContactForm()
            
    template = loader.get_template("Home/contact.html")
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))