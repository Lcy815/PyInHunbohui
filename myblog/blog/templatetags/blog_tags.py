# coding=utf-8
from ..models import Post, Category
from django import template

register = template.Library()


# 最新文章模版标签
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-create_time')[:num]


# 归档模版标签
@register.simple_tag
def get_archives():
    return Post.objects.dates('create_time', 'month', order='DESC')


# 分类模版标签
@register.simple_tag
def get_category():
    return Category.objects.all()


