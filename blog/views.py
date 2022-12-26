from django.shortcuts import render, HttpResponse, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages

from blog.models import *



# ========== import for file upload with Tinymce Editor ===============
import os
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

# ========== Configuration for file upload with Tinymce Editor =============
@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        file_obj = request.FILES['file']
        file_name_suffix = file_obj.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
            return JsonResponse({"message": "Wrong file format"})

        upload_time = timezone.now()
        path = os.path.join(
            settings.MEDIA_ROOT,
            'tinymce',
            str(upload_time.year),
            str(upload_time.month),
            str(upload_time.day)
        )
        # If there is no such path, create
        if not os.path.exists(path):
            os.makedirs(path)

        file_path = os.path.join(path, file_obj.name)

        file_url = f'{settings.MEDIA_URL}tinymce/{upload_time.year}/{upload_time.month}/{upload_time.day}/{file_obj.name}'

        if os.path.exists(file_path):
            return JsonResponse({
                "message": "file already exist",
                'location': file_url
            })

        with open(file_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        return JsonResponse({
            'message': 'Image uploaded successfully',
            'location': file_url
        })
    return JsonResponse({'detail': "Wrong request"})
# ========== End Configuration for file upload with Tinymce Editor =============


def search(request):
    template_name = 'pages/blog/search.html'
    posts = Post.objects.filter(is_active=True)
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()

    return render(request, template_name, {'posts': posts})

    

# ================================   HOME PAGE VIEW  ==========================
def index(request):
    featured_posts = Post.objects.filter(is_active=True ,is_featured=True).order_by('-date_created')[:3]
    latest_posts = Post.objects.filter(is_active=True).order_by('-date_created')[:3]

    context = {
        'featured_posts': featured_posts,
        'latest_posts': latest_posts
    }
    return render(request, 'pages/index.html', context)


# ================================   HOME PAGE VIEW  ==========================
def postList(request):
    template_name = 'pages/blog/blog.html'
    posts = Post.objects.filter(is_active=True)

    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    paged_queryset = paginator.get_page(page)
    
    context = {
        'posts': paged_queryset,
    }
    return render(request, template_name, context)


# ================================   HOME PAGE VIEW  ==========================

def postDetails(request, slug):
    template_name = 'pages/blog/post_details.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(is_active=True).order_by('-date_created')

    context = {
        'post': post,
        'comments': comments,
    }
    
    # Get method
    if request.method == 'GET':

        return render(request, template_name, context)

    # Post method
    if request.method == 'POST':
        
        comment = Comment(
            post = post,
            name = request.POST['username'],
            email = request.POST['useremail'],
            content = request.POST['usercomment']
        )
        comment.save()
        messages.success(request, '✅ Your comment has been submitted successfully 👍!')
        
        return render(request, template_name, context)   


# ================================   CATIGORY POSTS PAGE VIEW  ==========================
def category_view(request, slug):
    template_name = 'pages/blog/categoy_posts.html'
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.prefetch_related().filter(category=category, is_active=True).order_by('-date_created')

    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    paged_queryset = paginator.get_page(page)

    context = {
        'category': category,
        'posts': paged_queryset,
    }
    return render(request, template_name, context)

# ========== 404 PAGE VIEW ================
def page_not_found_view(request, exception):
    return render(request, 'pages/404.html', {}, status=404)

def server_error(request, exception):
    return render(request, 'pages/500.html', {}, status=500)