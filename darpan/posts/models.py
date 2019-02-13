from django.db import models
from django.conf import settings
from django.utils.text import slugify

from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver

from taggit.managers import TaggableManager



def get_unique_slug(model_instance, slugable_field_name, slug_field_name):
    """
    Takes a model instance, sluggable field name (such as 'title') of that
    model as string, slug field name (such as 'slug') of the model as string;
    returns a unique slug as string.
    """
    slug = slugify(getattr(model_instance, slugable_field_name))
    unique_slug = slug
    extension = 1
    ModelClass = model_instance.__class__
 
    while ModelClass._default_manager.filter(
        **{slug_field_name: unique_slug}
    ).exists():
        unique_slug = '{}-{}'.format(slug, extension)
        extension += 1
 
    return unique_slug


class Post(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    
    
    title = models.CharField(max_length=100, default='', blank=True)
    text = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    
    source = models.URLField(default='', blank=True)

    tags = TaggableManager(blank=True)

    def __str__(self):
        return str(self.owner)
    
    def get_absolute_url(self):
        return reverse('post:detail', args=[str(self.slug)])



@receiver(pre_save, sender=Post)    
def populate_slug(sender, **kwargs):
    post = kwargs["instance"]
    
    if not post.slug:
        post.slug = get_unique_slug(post, 'title', 'slug')
        print(post.slug)
