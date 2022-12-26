from django.urls import path
from blog.views import index, postList, postDetails, search, category_view

urlpatterns = [
    path('', index, name='home'),
    path('blog/', postList, name='blog'),
    path('blog/<slug:slug>/', postDetails, name='post-details'),
    path('search/', search, name='search'),
    path('category-detail/<slug:slug>/', category_view, name='category-detail'),

]