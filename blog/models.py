import uuid
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify 
from django.urls import reverse
from tinymce.models import HTMLField
from django.contrib.auth.models import User


#================================ CATEGORY ========================#
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='author/%Y/%m/%d/', blank=True, null=True)
    designation = models.CharField(verbose_name=_('designation'), 
        help_text=_("ex: django full-stack developer"), 
        max_length=150, 
        blank=True, 
        null=True
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')


#================================ CATEGORY ========================#
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name=_('title'), max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True,verbose_name=_('is active'), blank=True, null=True)

    #Utility fields
    slug = models.SlugField(verbose_name=_('slug'), max_length=250, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(verbose_name=_('created date'), blank=True, null=True)
    last_updated = models.DateTimeField(verbose_name=_('updated date'), blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.slug is None:
            self.slug = slugify(f"{self.title}-{self.id}")

        self.last_updated = timezone.localtime(timezone.now())
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

        
#================================ POST ========================#
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name=_('title'), help_text=_('Only 200 characters allowed') ,max_length=200)
    overview = models.TextField()
    author = models.ForeignKey(Author, verbose_name=_('author'), on_delete=models.CASCADE)
    thumbnail = models.ImageField(verbose_name=_('thumbnail'), upload_to='post/%Y/%m/%d/')
    content = HTMLField(verbose_name=_('content'))
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE, verbose_name=_('category'))
    is_featured = models.BooleanField(verbose_name=_('is featured ?'), default=False)
    is_active = models.BooleanField(verbose_name=_('is active ?'), default=False)
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, null=True, blank=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, null=True, blank=True)

    #Utility fields
    slug = models.SlugField(verbose_name=_('slug'), max_length=250, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(verbose_name=_('created date'), blank=True, null=True)
    last_updated = models.DateTimeField(verbose_name=_('updated date'), blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.slug is None:
            self.slug = slugify(f"{self.title}")

        self.slug = slugify(f"{self.title}")
        self.last_updated = timezone.localtime(timezone.now())
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date_created']
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    @property
    def get_comments(self):
        return self.comments.all().order_by('-date-created')


#================================ COMMENT ========================#
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    #parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-date_created']
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return ""