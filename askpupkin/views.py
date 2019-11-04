from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import *
import re


def question_list(request, tag=None):
    path = request.path
    if path == '/hot':
        question_list = Question.objects.best_questions()
    elif re.match(r'^/tag/.+$', path):  # tag select
        question_list = Question.objects.filter(tag__tag_word=tag)
    else:
        question_list = Question.objects.newest_questions()
    question_list, paginator, page = paginate(question_list, request)
    tags = Tag.objects.all()
    return render(request, 'index.html', {'questions': question_list, 'tags': tags, 'page': page})


def question(request, number):
    answers = Answer.objects.filter(question=number)
    question = Question.objects.filter(id=number)
    return render(request, 'question.html', {'answers': answers, 'questions': question})


def ask(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request, 'ask.html', context=context)


def login(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request, 'login.html', context=context)


def signup(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request, 'signup.html', context=context)


def paginate(object_list, request):
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page', 1)
    item = paginator.page(page)
    return item.object_list, paginator, page
