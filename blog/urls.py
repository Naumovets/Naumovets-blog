from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    # path('archive/', PostArchiveList.as_view(), name='archive_list'),
    path('tags/', TagList.as_view(), name='tag_list'),
    path('tags/<slug:tag_slug>/', PostList.as_view(), name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post_slug>/', PostDetail.as_view(), name='post_detail'),
    path('<int:post_id>/post_comment/', post_comment, name='post_comment'),
    path('newsletter/', newsletter, name='newsletter'),
]
