from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django import forms

from .models import Author, Category, Post, Comment


#================================ AUTHOR ========================#
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    def profile_picture(self, object):
        return format_html('<img src={} width="50" height="50" style="border-radius: 50%; objects-fit: cover" />'.format(object.avatar.url))

    list_display = ('profile_picture', 'designation')
    list_display_links = ('profile_picture',)
    search_fields = ('email',)
    list_per_page = 10


#================================ CATEGORY ========================#
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


#================================ POST ========================#
class PostForm(forms.ModelForm):
    class Meta:
        widgets = {
            'title': forms.TextInput(attrs={'size':'80'}),
            'slug': forms.TextInput(attrs={'size':'80'}),
        }

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def post_thumbnail(self, object):
        return format_html('<img src={} width="40" height="30" style="border-radius: 8px" />'.format(object.thumbnail.url))

    list_display = ('post_thumbnail', 'title', 'author', 'is_active', 'is_featured', 'date_created')
    list_display_links = ('post_thumbnail', 'title')
    list_filter = ('is_active', 'author', 'date_created')
    search_fields = ('title', 'author')
    date_hierarchy = 'date_created'
    list_per_page = 10

    form = PostForm

    actions = ['active_comment', 'unactive_comment']

    def active_comment(self, request, queryset):
        queryset.update(is_active=True)

    def unactive_comment(self, request, queryset):
        queryset.update(is_active=False)

    fieldsets = (
        (_('Title & overview'), {
            'fields': ('title', 'overview')
        }),
        (_('Author & thumbnail'), {
            'fields': (('author', 'thumbnail'),)
        }),
        (_('Content'), {
            'fields': ('content',)
        }),
        (_('Category & Tags'), {
            'fields': (('category',),)
        }),
        (('Activate or Not | Featured or Not'), {
            'fields': (('is_active', 'is_featured'),)
        }),
        (('Previous Post | Next Post'), {
            'fields': (('previous_post', 'next_post'),)
        }),
        (_('Utilities fileds (Not required). These fields will be automaticaly fulfilled'), {
            'fields': (
                'slug',
                ('date_created', 'last_updated')
                ),
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_active', 'date_created')
    list_display_links = ('name', 'email')

    actions = ['active_comment', 'desactive_comment']

    def active_comment(self, request, queryset):
        queryset.update(is_active=True)

    def desactive_comment(self, request, queryset):
        queryset.update(is_active=False)
