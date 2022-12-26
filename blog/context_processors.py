from .models import Post, Category



def recent_posts(request):
    recent_posts = Post.objects.filter(is_active=True).order_by('-date_created')[:3]

    return { 'recent_posts': recent_posts }

def category_links(request):
    categories = Category.objects.filter(is_active=True).order_by().distinct()[:6]

    return {'categories': categories}