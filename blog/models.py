from django.db import models
import django.utils.timezone as timezone
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField,ImageSpecField
from pilkit.processors import ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField

class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )
    title = models.CharField('标题', max_length=70)
    content=RichTextUploadingField('内容',default="")
    abstract = models.TextField('摘要', max_length=200, blank=True, null=True, help_text="可选，如若为空将摘取正文的前200个字符")
    add_date = models.DateTimeField('保存日期', default=timezone.now)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    views = models.PositiveIntegerField('浏览量', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    rank=models.PositiveIntegerField('头条', default=0)
    category = models.ForeignKey('Category', verbose_name='分类',
                                 null=True,
                                 on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag',  verbose_name='标签',blank=True)
    author= models.ForeignKey(User, verbose_name='作者',on_delete=models.CASCADE)
    image_raw= models.ImageField('图片', upload_to='article/%Y%m%d', blank=True, null=True)
    image=ImageSpecField(source="image_raw",
                        processors=[ResizeToFill(200, 170)],
                        format='JPEG',
                        options={'quality': 60})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-add_date']


class Category(models.Model):
    name = models.CharField('类名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField('标签', max_length=20)

    def __str__(self):
        return self.name