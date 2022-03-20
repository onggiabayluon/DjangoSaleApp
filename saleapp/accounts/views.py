from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


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
    return redirect('home_page')
