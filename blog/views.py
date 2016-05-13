from django.utils import timezone
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse,HttpResponse
from .forms import PostForm
from .models import *
from .user import *


def index(request):
    user = get_user(request)
    if user:
        return render(request, "blog/index.html")
    else:
        return render(request, "login/signin.html")


def post_list(request):
    user = get_user(request)
    if user:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return render(request, 'blog/post_list.html', {'posts': posts})
    else:
        return HttpResponse("<a href='/'>login to continue</a>")




def post_detail(request, pk):
    user = get_user(request)
    if user:
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})
    else:
        return HttpResponse("<a href='/'>login to continue</a>")



def post_new(request):
    user = get_user(request)
    if user:
        userdata = UserData.objects.get(author=user.username)
        if(userdata.user_type == "blogger" or request.user.is_superuser):
            if request.method == "POST":
                form = PostForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.author = user
                    post.user = post.author.username
                    post.published_date = timezone.now()
                    post.save()
                    return redirect('post_detail', pk=post.pk)
            else:
                form = PostForm()
            return render(request, 'blog/post_edit.html', {'form': form})
        else:
            return HttpResponse("not blogger")
    else:
         return HttpResponse("<a href='/'>login to continue</a>")


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = get_user(request)
    if user:
        userdata = UserData.objects.get(author=user.username)
        if(userdata.user_type == "blogger" and user.username == post.user):
            if request.method == "POST":
                form = PostForm(request.POST, instance=post)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.author = post.author
                    post.username = post.author.username
                    post.published_date = timezone.now()
                    post.save()
                    return redirect('post_detail', pk=post.pk)
            else:
                form = PostForm(instance=post)
            return render(request, 'blog/post_edit.html', {'form': form})
        elif userdata.user_type == "blogger":
            return HttpResponse("You are not same author")
        else:
            return HttpResponse("You are not a blogger")
    else:
         return HttpResponse("<a href='/'>login to continue</a>")

