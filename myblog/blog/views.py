# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import markdown
from .models import Category
# Create your views here.
from blog.models import Post, Tag
from comments.forms import CommentForm
# 导入listview
from django.views.generic import ListView
from django.db.models import Q


# def index(request):
#     post_list = Post.objects.all().order_by('-create_time')
#     return render(request, 'blog/index.html', context={
#         'post_list':  post_list,
#     })


# 将index转化为listview视图函数
class IndexViews(ListView):
    '''
        model:将model指定为Post,获取的数据模型是Post
        template_name: 指定视图渲染的模版
        context_object_name: 传递给模版的变量名
        paginate_byk:开启分页功能，每页多少数据
    '''
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def get_context_data(self, **kwargs):

        '''
           在视图函数中（fbv）,使用render返回一个context模版变量render(request,
                                                                     'blog/index.html',
                                                                     context={ 'post_list':  post_list,）
           其中模版变量context是个字典，在类视图中（cbv）可以通过复写get_context_data方法再填入
           我们想用的值

        paginator ，即 Paginator 的实例。
        page_obj ，当前请求页面分页对象。
        is_paginated，是否已分页。只有当分页后页面超过两页时才算已分页。
        object_list，请求页面的对象列表，和 post_list 等价。所以在模板中循环文章列表时可以选 post_list ，也可以选 object_list。

        '''

        # 首先获取父类传递给模版的字典
        context = super(IndexViews, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用pagination_data方法获取相应的数据
        pagination_data = self.pagination_data(paginator, page_obj, is_paginated)

        # 将分类导航数据添加到context中
        context.update(pagination_data)

        return context

    # 获取分页所需要的数据
    @staticmethod
    def pagination_data(paginator, page, is_paginated):

        if not is_paginated:
            return {}
        # 当前页码的左边连续的页码号，初始值为空
        left = []

        # 当前页码的右边连续的页码号，初始值为空
        right = []

        # 标识第一页页码后是否需要显示省略号
        left_has_more = False

        # 标识最后一页页码前是否需要显示省略号
        right_has_more = False

        # 如果当前页左边连续的号码中 包含了第一页，直接显示就好，如果没有第一页也是需要显示的
        first = False

        # 当前页右边连续的号码中 包含了最后一页，直接显示就好，如果没有最后一页也是需要显示
        last = False

        # 当前页码
        page_number = page.number

        # 总页数
        total_pages = paginator.num_pages

        # 获取整个页码列表
        page_range = list(paginator.page_range)

        if page_number == 1:
            '''
            如果当前页面是第一页，那么左边连续号码就是空，右边连续号码取连续2个
            
            '''
            print page_number
            right = page_range[page_number: page_number+2]

            '''
            如果当前页面右边连续号码的最大值比最后一个页码减去1还小，说明最右边页码跟最后
            页码之间还有页码，要显示省略号
            '''
            if right[-1] < total_pages - 1:
                right_has_more = True
            '''
            如果当前页面右边连续号码最大值比最后一个页码小，说明最后页码不在连续号码中，需要显示最后页码
            '''
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            '''
            如果当前页面为最后一页，那右边连续号码就为空，左边连续号码取2个
            '''
            left = page_range[(page_number - 3) if (page_number-3)>0 else 0:page_number-1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            # 如果当前页面既不是第一页，也不是最后一页
            right = page_range[page_number:page_number+2]
            left = page_range[(page_number - 3) if (page_number-3)>0 else 0:page_number-1]

            # 是否显示省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    # post.body = markdown.markdown(post.body, extensions={
    #     'markdown.extensions.extra',
    #     'markdown.extensions.codehilite',
    #     'markdown.extensions.toc',
    # })
    md = markdown.Markdown(extensions={
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        # TocExtension(slugify=slugify),
    })
    post.body = md.convert(post.body)
    post.toc = md.toc
    form = CommentForm()
    comment_list = post.comment_set.all()
    content = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }
    return render(request, 'blog/detail.html', context=content)


# def archives(request, year, month):
#     post_list = Post.objects.filter(create_time__year=year,
#                                     create_time__month=month
#                                     ).order_by('-create_time')
#     return render(request, 'blog/index.html', context={
#         'post_list': post_list
#     })


# 将归档修改为listview函数
class ArchivesViews(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def get_queryset(self):
        return super(ArchivesViews, self).get_queryset().filter(create_time__year=self.kwargs.get('year'),
                                                                create_time__month=self.kwargs.get('month')
                                                                )


def category(request, name):
    cate = get_object_or_404(Category, name=name)
    post_list = Post.objects.filter(category=cate
                                    ).order_by('-create_time')
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })


# 将分类转化为listview函数
class CategoryViews(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def get_queryset(self):
        cate = get_object_or_404(Category, name=self.kwargs.get('name'))
        return super(CategoryViews, self).get_queryset().filter(category=cate)

    def get_context_data(self, **kwargs):
        # 首先获取父类传递给模版的字典
        context = super(CategoryViews, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用pagination_data方法获取相应的数据
        pagination_data = IndexViews().pagination_data(paginator, page_obj, is_paginated)

        # 将分类导航数据添加到context中
        context.update(pagination_data)
        return context


# TagViews
class TagViews(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag_post = get_object_or_404(Tag, tag_name=self.kwargs.get('name'))
        return super(TagViews, self).get_queryset().filter(tags=tag_post)


# 搜索
def search(request):
    q = request.GET.get('q')
    err_message = ''

    if not q:
        err_message = 'please enter a search word'
        return render(request, 'blog/index.html', context={'err_message': err_message})
    post_list = Post.objects.all().filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', context={'post_list': post_list, 'err_message': err_message})


def blog(request):
    return render(request, 'blog/full-width.html')
