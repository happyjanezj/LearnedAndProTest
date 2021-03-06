from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from blog.models import Article, Category,Tag
import markdown2
# Create your views here.

class IndexView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.all()
        for article in article_list:
            article.body = markdown2.markdown(article.body,extras=['fenced-code-blocks'])
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        return super(IndexView,self).get_context_data(**kwargs)

class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/detail.html"
    context_object_name = "article"
    pk_url_kwarg = 'article_id'

    def get_object(self):
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'], )
        return obj

class CategoryView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    def get_queryset(self):
        article_list = Article.objects.filter(category=self.kwargs['cate_id'])
        for article in article_list:
            article.body = markdown2.markdown(article.body,extras=['fenced-code-blocks'])
        return article_list
    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(CategoryView, self).get_context_data(**kwargs)

class TagView(ListView):
    template_name = "blog/index.html"
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list = Article.objects.filter(tags=self.kwargs['tag_id'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'],)
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        return super(TagView, self).get_context_data(**kwargs)

class ArchiveView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list = Article.objects.filter(created_time__year=self.kwargs['year'],created_time__month=self.kwargs['month'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        return super(ArchiveView, self).get_context_data(**kwargs)
