from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from .models import Post, Comment

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def post_list(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(is_private=False)

    return render(request, 'post_list.html', {'posts': posts})


@login_required
def post_create(request):
    if request.method == 'POST':
        Post.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            author=request.user,
            is_private=request.POST.get('is_private') == 'on',
            file=request.FILES.get('file')
        )
        return redirect('post_list')

    return render(request, 'post_create.html')

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать это сообщение")

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.is_private = request.POST.get('is_private') == 'on'
        post.save()
        return redirect('post_detail', post_id=post.id)

    return render(request, 'post_edit.html', {'post': post})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 🔐 Проверка приватности
    if post.is_private and not request.user.is_authenticated:
        return HttpResponseForbidden("Этот пост доступен только зарегистрированным")

    comments = post.comments.all().order_by('created_at')

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments
    })

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        Comment.objects.create(
            post=post,
            author=request.user,
            text=request.POST['text'],
            file=request.FILES.get('file')
        )

    return redirect('post_detail', post_id=post.id)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать этот комментарий")

    if request.method == 'POST':
        comment.text = request.POST.get('text')
        comment.save()
        return redirect('post_detail', post_id=comment.post.id)

    return render(request, 'edit_comment.html', {'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот комментарий")

    if request.method == 'POST':
        post_id = comment.post.id
        comment.delete()
        return redirect('post_detail', post_id=post_id)

    return render(request, 'delete_comment.html', {'comment': comment})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот пост")

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'delete_post.html', {'post': post})

