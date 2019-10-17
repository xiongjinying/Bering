import markdown2
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from .models import Article,Category

class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "article_list"
    paginate_by = 5

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.content = markdown2.markdown(article.content, )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['rank_article_list'] = Article.objects.order_by("-rank",'-add_date')[:1]
        return super(IndexView, self).get_context_data(**kwargs)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "detail.html"
    context_object_name = "article"
    pk_url_kwarg = 'article_id'

    def get_object(self):
        # 首先调用父类的方法
        obj = super(ArticleDetailView, self).get_object()
        # 浏览量 +1
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj

class AboutView(TemplateView):
    template_name= "about.html"