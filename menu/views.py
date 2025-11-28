from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from .forms import SignupForm, LoginForm
from .models import CustomUser
from django.contrib.auth import authenticate, login

# Menu
def menu_view(request):
    return render(request, 'menu/menu.html')


# Menu Signup
def menu_signup_view(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False) 
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            
            messages.success(request, 'Successful registration! You can now log in.')
            return redirect('menu')
        
    else:
        form = SignupForm()

    context = {'form': form}
    return render(request, 'menu/menu_signup.html', context)


# Menu Login
def menu_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST) 
        
        if form.is_valid():
            identification = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password')

            user = authenticate(
                request, 
                username=identification, 
                password=password
            )

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('posts:posts')
            else:
                messages.error(request, 'Invalid username/email or password.')
                
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'menu/menu_login.html', context)
