from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout 
from django.shortcuts import redirect

@login_required 
def posts_view(request):
    return render(request, 'posts/posts.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('menu:menu')