from django.shortcuts import render_to_response, redirect
from article.models import Article, Comments
from django.template.loader import get_template
from django.template import Context
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from forms import CommentForm
from django.template.context_processors import csrf


# Create your views here
def articles(request):
    return render_to_response('articles.html', {'articles': Article.objects.all()})

def article(request, article_id = 1):
    comment_form = CommentForm
    args = {'article': Article.objects.get(id = article_id), 
            'comments': Comments.objects.filter(comments_article_id = article_id),
            'form': comment_form,
            }
    args.update(csrf(request))
    return render_to_response('article.html', args)

def addLike(request, article_id):
    try:
        article = Article.objects.get(pk = article_id)
        article.article_likes += 1
        article.save()
    except ObjectDoesNotExist:
        raise Http404

    return redirect('/')

def addComment(request, article_id):
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.comments_article = Article.objects.get(id = article_id)
            form.save()
    return redirect('/get/%s' % article_id)


