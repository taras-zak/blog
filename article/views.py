from django.shortcuts import render_to_response, redirect
from article.models import Article, Comments
from django.template.loader import get_template
from django.template import Context
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from forms import CommentForm
from django.template.context_processors import csrf
from django.contrib import auth
from django.core.paginator import Paginator


# Create your views here
def articles(request, page_number = 1):
    all_articles = Article.objects.all()
    curr_page = Paginator(all_articles, 2)
    return render_to_response('articles.html', {'articles': curr_page.page(page_number), 
                                                'username': auth.get_user(request).username}
                            )

def article(request, article_id = 1):
    comment_form = CommentForm
    args = {'article': Article.objects.get(id = article_id), 
            'comments': Comments.objects.filter(comments_article_id = article_id),
            'form': comment_form,
            'username': auth.get_user(request).username,
            }
    args.update(csrf(request))
    return render_to_response('article.html', args)

def addLike(request, article_id):
    try:
        if article_id in request.COOKIES:
            redirect('/')
        else:            
            article = Article.objects.get(pk = article_id)
            article.article_likes += 1
            article.save()
            response = redirect('/')
            response.set_cookie(article_id, 'test')
            return response
    except ObjectDoesNotExist:
        raise Http404

    return redirect('/')

def addComment(request, article_id):
    if request.POST and ("pause" not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.comments_article = Article.objects.get(id = article_id)
            form.save()
            request.session.set_expiry(60)
            request.session['pause'] = True
    return redirect('/get/%s' % article_id)


