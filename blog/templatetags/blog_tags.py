from django import template

from django.db.models import Count
from taggit.models import Tag

from blog.models import Post

register = template.Library()


@register.inclusion_tag('blog/tags/pagination_numbers.html')
def show_pagination_numbers(page):
    if page.number > 3 and page.paginator.num_pages > 5 and page.number+2 < page.paginator.num_pages:
        numbers = [i for i in range(page.number-2, page.number+3)]
    elif page.number < 4:
        numbers = [i for i in range(1, min(page.paginator.num_pages+1, 6))]
    else:
        numbers = [i for i in range(page.paginator.num_pages-4, page.paginator.num_pages+1)]
    return {'numbers': numbers, 'active': page.number}


@register.inclusion_tag('blog/tags/popular_posts.html')
def show_popular_post():
    posts = Post.published.annotate(count_comments=Count('comments')).order_by('-count_comments')[:5]
    return {'posts': posts}


@register.inclusion_tag('blog/tags/popular_tags.html')
def show_popular_tags():
    tags = Tag.objects.annotate(count_posts=Count('taggit_taggeditem_items')).order_by('-count_posts')[:10]
    return {'tags': tags}
