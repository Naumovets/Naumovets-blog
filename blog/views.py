from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from taggit.models import Tag

from blog.forms import CommentForm, NewsletterForm
from blog.models import Post, Newsletter


class PostList(ListView):

    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag_slug', None)
        return context

    def get_queryset(self):
        if self.kwargs.get('tag_slug', None):
            tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
            return Post.published.filter(tags__in=[tag]).order_by('-publish')
        return Post.published.all().order_by('-publish')


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'
    context_object_name = 'post'

    def get_object(self):
        return get_object_or_404(Post,
                                 publish__year=self.kwargs.get('year'),
                                 publish__month=self.kwargs.get('month'),
                                 publish__day=self.kwargs.get('day'),
                                 slug=self.kwargs.get('post_slug'))


class TagList(ListView):
    queryset = Tag.objects.all().order_by('name')
    template_name = 'blog/tag_list.html'
    context_object_name = 'tags'
    paginate_by = 5


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post.publish.year, post.publish.month, post.publish.day, post.slug)


@require_POST
def newsletter(request):
    exist = Newsletter.objects.filter(email__iexact=request.POST.get('email').lower()).exists()
    success = False
    if not exist:
        form = NewsletterForm(data=request.POST)
        if form.is_valid():
            form.save()
            success = True

    return render(request, template_name='blog/newsletter.html', context={'email': request.POST.get('email'),
                                                                          'url': request.GET.get('url'),
                                                                          'success': success,
                                                                          'exist': exist})

