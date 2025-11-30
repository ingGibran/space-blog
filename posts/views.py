from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout 
from django.shortcuts import redirect
from .forms import PostForm

@login_required 
def posts_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:posts')
    else:
        form = PostForm()

    # Get all published posts
    from .models import Post
    posts = Post.objects.filter(is_published=True).order_by('-created_at')

    context = {
        'form': form,
        'posts': posts
    }
    
    return render(request, 'posts/posts.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('menu:menu')