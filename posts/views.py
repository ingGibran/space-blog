from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required 
def posts_view(request):
    return render(request, 'posts/posts.html')
