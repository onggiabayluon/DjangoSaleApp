from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            #  log the user in
            return redirect('home_page')
    if request.method == 'GET':
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {
        'title': 'Signup',
        'form': form
    })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log the user in
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successfully!")
            return redirect('home_page')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {
        'title': 'Signup',
        'form': form
    })


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Log out successfully!")

    return redirect('home_page')
