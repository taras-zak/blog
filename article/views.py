from django.shortcuts import render_to_response, redirect
from article.models import Article, Comments
from django.template.loader import get_template
from django.template import Context
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404


# Create your views here
def articles(request):
    return render_to_response('articles.html', {'articles': Article.objects.all()})

def article(request, article_id = 1):
    return render_to_response( 
                                'article.html', 
                                {'article': Article.objects.get(id = article_id), 
                                 'comments': Comments.objects.filter(comments_article_id = article_id)}
                             )

def addLike(request, article_id):
    try:
        article = Article.objects.get(pk = article_id)
        article.article_likes += 1
        article.save()
    except ObjectDoesNotExist:
        raise Http404

    return redirect('/')