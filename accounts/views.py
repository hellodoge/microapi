from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            login(
                request,
                authenticate(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password1')
                )
            )
            return redirect('manager-home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('login')
