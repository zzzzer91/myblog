from django import template
from django.db.models.aggregates import Count

from ..models import Category, Post

register = template.Library()


@register.simple_tag
def get_recent_posts():
    r'''获取最近发表的5篇文章'''

    return Post.objects.all()[:5]


# @register.simple_tag
# def get_archives():
#     r'''获取归档
    
#     已在myblo.views中实现, 所以忽略.
#     '''

#     date_list = Post.objects.dates('created_time', 'month', order='DESC')
#     archives = []
#     for date in date_list:
#         post_list = Post.objects.filter(
#             created_time__year=date.year,
#             created_time__month=date.month
#         )
#         archives.append((date, post_list))
#     return archives


@register.simple_tag
def get_categories():
    r'''获取分类下文章数量'''

    return Category.objects.annotate(num=Count('post'))
