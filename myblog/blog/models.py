# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.


# 文章分类
class Category(models.Model):
    """
        Django 要求模型必须继承 models.Model 类。
        Category 只需要一个简单的分类名 name 就可以了。
        CharField 指定了分类名 name 的数据类型，CharField 是字符型，
        CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
        当然 Django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
        Django 内置的全部类型可查看文档：
        https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    """
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


# 文章标签
class Tag(models.Model):
    tag_name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.tag_name


# 文章主体
class Post(models.Model):
    # 浏览量
    views = models.PositiveIntegerField(default=0)

    # 新增自定义方法
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 标题
    title = models.CharField(max_length=70)

    # 正文
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
    body = models.TextField()

    # 创建时间，最后修改时间
    create_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 摘要，可以没有摘要，因此要设置可以为空
    excerpt = models.CharField(max_length=200, blank=True)

    # 复写save方法，在存入数据库前先从body中截取多少字存为摘要
    def save(self, *args, **kwargs):
        if not self.excerpt:
            # 因为我们的文章主体使用了支持markdown语法，所以先实例化一个markdown实例
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将markdown文本渲染成html格式，再用strip去除所有html标签，取前54个字符
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        # 调用父类的方法 保存到数据库
        super(Post, self).save(*args, **kwargs)


    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    # https://docs.djangoproject.com/en/1.10/topics/db/models/#relationships
    category = models.ForeignKey(Category, verbose_name=u'分类')
    tags = models.ManyToManyField(Tag, verbose_name=u'标签', blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    author = models.ForeignKey(User)

    # 定义一个生成文章详情的url
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-create_time']




