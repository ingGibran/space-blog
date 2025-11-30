from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import PostForm
from .models import Post, Like, Comment

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
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_published=True)
    user = request.user
    
    # Try to get existing like
    like, created = Like.objects.get_or_create(user=user, post=post)
    
    if not created:
        # Like already existed, so remove it (unlike)
        like.delete()
        is_liked = False
    else:
        # Like was just created
        is_liked = True
    
    # Get updated like count
    likes_count = post.likes.count()
    
    return JsonResponse({
        'is_liked': is_liked,
        'likes_count': likes_count
    })

@login_required
def get_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_published=True)
    comments = post.comments.select_related('author').order_by('created_at')
    
    comments_data = [{
        'id': comment.id,
        'author': comment.author.username,
        'text': comment.text,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'time_ago': get_time_ago(comment.created_at),
        'can_delete': request.user == comment.author or request.user == post.author
    } for comment in comments]
    
    return JsonResponse({
        'comments': comments_data,
        'count': comments.count()
    })

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_published=True)
    
    import json
    data = json.loads(request.body)
    comment_text = data.get('text', '').strip()
    
    if not comment_text:
        return JsonResponse({'error': 'Comment text is required'}, status=400)
    
    # Create new comment
    comment = Comment.objects.create(
        post=post,
        author=request.user,
        text=comment_text
    )
    
    # Get updated comment count
    comments_count = post.comments.count()
    
    return JsonResponse({
        'success': True,
        'comment': {
            'id': comment.id,
            'author': comment.author.username,
            'text': comment.text,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'time_ago': 'just now'
        },
        'comments_count': comments_count
    })

def get_time_ago(datetime_obj):
    from django.utils import timezone
    from datetime import timedelta
    
    now = timezone.now()
    diff = now - datetime_obj
    
    if diff < timedelta(minutes=1):
        return 'just now'
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() / 60)
        return f'{minutes} minute{"s" if minutes != 1 else ""}'
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        return f'{hours} hour{"s" if hours != 1 else ""}'
    elif diff < timedelta(days=30):
        days = diff.days
        return f'{days} day{"s" if days != 1 else ""}'
    elif diff < timedelta(days=365):
        months = int(diff.days / 30)
        return f'{months} month{"s" if months != 1 else ""}'
    else:
        years = int(diff.days / 365)
        return f'{years} year{"s" if years != 1 else ""}'

@login_required
@require_POST
def delete_comment(request, comment_id):
    """
    AJAX view to delete a comment.
    Only allows deletion if user is comment author OR post author.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    
    # Permission check: user must be comment author OR post author
    if request.user == comment.author or request.user == post.author:
        comment_id = comment.id
        post_id = post.id
        
        # Delete the comment
        comment.delete()
        
        # Get updated comment count
        comments_count = post.comments.count()
        
        return JsonResponse({
            'success': True,
            'comment_id': comment_id,
            'comments_count': comments_count
        })
    else:
        return JsonResponse({
            'success': False,
            'error': 'You do not have permission to delete this comment'
        }, status=403)

@login_required
def logout_view(request):
    logout(request)
    return redirect('menu:menu')