from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.utils import timezone
from .forms import PostForm

@csrf_exempt
def addBlogs(request):

	#Post request handling
	if request.method == 'POST':
		title = request.POST.get("title", "")
		data = request.POST.get("data", "")

		#getting token from header
		token = str(request.META.get('HTTP_AUTHORIZATION', '')).split(" ")[1]

		#getting token object to identify user
		token_object = Token.objects.get(key=token)

		#saving post to database
		q = Post(author=token_object.user , title=title , text=data , published_date=timezone.now() , user=str(token_object.user))
		q.save()
		
		return JsonResponse({'status':'ok','result':{'response':'post saved successfully'}})

	#other request handling except POST
	else:
		return JsonResponse({'status':'ok','result':{'response':'invalid request!!'}})

@csrf_exempt
def index(request):
	all_post = Posts.objects.order_by('pub_date')
	return render(request, "posts.html", {'data' : all_post})

def post_list(request):
    # if()
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})