from django.conf.urls import include, url,patterns


urlpatterns = [
    url(r'^all', 'article.views.articles'),
    url(r'^get/(?P<article_id>\d+)', 'article.views.article'),
    url(r'^addLike/(?P<article_id>\d+)', 'article.views.addLike'),
    url(r'^', 'article.views.articles'),
]
