import markdown
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Post, About


def index(request):
    """主页."""

    post_list = Post.objects.all()
    paginator = Paginator(post_list, 8)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html', {'post_list':post_list})


def category(request, pk):
    """分类."""

    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    paginator = Paginator(post_list, 8)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/category.html', context={
        'post_list': post_list, 
        'category': cate,
    })


def archives(request):
    """归档."""
    
    date_list = Post.objects.dates('created_time', 'month', order='DESC')
    archives = list()
    for date in date_list:
        post_list = Post.objects.filter(
            created_time__year=date.year,
            created_time__month=date.month
        )
        archives.append((date, post_list))

    start = archives[-1][0]
    end = archives[0][0]
    how_long = '{}年{}月 - {}年{}月'.format(start.year, start.month, end.year, end.month)

    return render(request, 'blog/archives.html', context={
        'archives': archives,
        'how_long': how_long,
    })


def about(request):
    """关于."""

    about = get_object_or_404(About, pk=1)
    about.body = markdown.markdown(about.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    return render(request, 'blog/about.html', {'about':about})


def search(request):
    """搜索."""

    q = request.GET.get('q')
    if q:
        post_list = Post.objects.filter(title__icontains=q)
        return render(request, 'blog/search.html', {'post_list':post_list})
    return HttpResponseRedirect('/')


def detail(request, pk):
    """文章内容."""

    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    comment_list = post.comment_set.all()
    # paginator = Paginator(comment_list, 5)
    # page = request.GET.get('page')
    # try:
    #     comment_list = paginator.page(page)
    # except PageNotAnInteger:
    #     comment_list = paginator.page(1)
    # except EmptyPage:
    #     comment_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/detail.html', context={
        'post': post, 
        'comment_list': comment_list,
    })


# def like(request):
#     """接收提交的点赞."""

#     pk = request.POST.get('pk')
#     post = get_object_or_404(Post, pk=pk)
#     post_liked = 'post_liked_' + pk
#     if request.session.get(post_liked, False):
#         return JsonResponse({'status':0})
#     post.increase_likes()
#     request.session[post_liked] = True
#     return JsonResponse({'status':1, 'likes':post.likes})


# def like(request):
#     """测试session."""

#     pk = request.POST.get('pk')
#     post = get_object_or_404(Post, pk=pk)
#     # request.session.setdefault('post_liked', {})
#     # if pk not in request.session['post_liked']:
#     #     request.session['post_liked'][pk] = True 
#     return JsonResponse({'status':0, 'likes':dict(request.session)})


def like(request):
    """处理提交的点赞."""

    pk = request.POST.get('pk')
    post = get_object_or_404(Post, pk=pk)
    post.increase_likes()
    return HttpResponse(post.likes)