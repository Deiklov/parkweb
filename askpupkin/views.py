from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import *


def question_list(request):
    # questions = []
    # for i in range(1, 30):
    #     questions.append({
    #         'title': 'title' + str(i),
    #         'id': i,
    #         'text': 'text ' + str(i) + ' Lorem ipsum dolor sit amet, consectetur'
    #     })
    # paginator = Paginator(questions, 5)
    # page_number = request.GET.get('page', 1)
    # page = paginator.get_page(page_number)
    question_list = Question.objects.newest_questions()
    return render(request, 'index.html', {'questions': question_list})


def question(request, number):
    answers = Answer.objects.filter(question=number)
    question = Question.objects.filter(id=number)
    return render(request, 'question.html', {'answers': answers, 'questions': question})


def ask(request):
    return render(request, 'ask.html', {})
