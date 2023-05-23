from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from accounts.models import Profile


class RegisterView(TemplateView):
    template_name = "frontend/signUp.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            name = request.POST.get("name")
            username = request.POST.get("login")
            password = request.POST.get("password")
            User.objects.create_user(username=username, password=password, is_superuser=False, is_staff=False, is_active=True)
            user = authenticate(self.request, username=username, password=password)
            login(request=self.request, user=user)
            Profile.objects.create(user=user, name=name)
            return render(request, "frontend/index.html")
        else:
            return render(request, "frontend/signUp.html")


class MyLoginView(TemplateView):

    template_name = "frontend/signIn.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            username = request.POST.get("login")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, "frontend/index.html")
            else:
                return HttpResponse(status=500)
        return render(request, "frontend/signIn.html")