# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from blog.models import Post
from django.shortcuts import get_object_or_404, render, redirect
from forms import CommentForm
# Create your views here.


def post_comment(request, pk):
    post = get_object_or_404(
        Post, pk=pk
    )
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            content = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            return render(request, 'blog/detail.html', context=content)
    return redirect(post)


