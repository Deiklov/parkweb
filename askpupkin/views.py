from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import *
from django.shortcuts import redirect
from django.contrib.auth.forms import *
from django.contrib.auth import *
import re
from .forms import *
from django.http import Http404


def question_list(request, tag=None):
    path = request.path
    if path == '/hot':
        question_list = Question.objects.best_questions()
    elif re.match(r'^/tag/.+$', path):  # tag select
        question_list = Question.objects.filter(tag__tag_word=tag)
    else:
        question_list = Question.objects.newest_questions()
    page = paginate(question_list, request)
    paginator = page.paginator
    tags = Tag.objects.all()
    context = {'questions': page.object_list, 'tags': tags,
               'page': page, 'paginator': paginator}
    return render(request, 'index.html', context=context)


def question(request, number):
    answers = Answer.objects.filter(question=number)
    if request.method == "POST":
        answerform = AnswerForm(request.POST)
        if answerform.is_valid():
            form = answerform.save(commit=False)
            form.author = request.user
            form.question = Question.objects.get(pk=number)
            form.save()
            return redirect('question', number=number)
    answerform = AnswerForm()
    question = Question.objects.filter(id=number)
    return render(request, 'question.html', {'answers': answers, 'questions': question, 'form': answerform})


def ask(request):
    tags = Tag.objects.all()
    questionform = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
    context = {'tags': tags, 'form': questionform}
    return render(request, 'ask.html', context=context)


def logout_view(request):
    logout(request)
    if 'next' in request.GET:
        return redirect(request.GET.get('next'))
    return redirect('/')


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        else:
            return redirect("/")
    form = LoginForm()
    context = {'form': form}
    return render(request, 'login.html', context=context)


def cabinet(request):
    if request.method == "POST":
        form = ExtnedsUserChangeForm(request.POST, instance=request.user)
        form_profile = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and form_profile.is_valid():
            form.save()
            form_profile.save()
            redirect("/profile/edit")
    user_form = ExtnedsUserChangeForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'cabinet.html', {'user_form': user_form, 'profile_form': profile_form})


def signup(request):
    tags = Tag.objects.all()
    profileform = ProfileForm()
    userform = ExtendsUserCreationForm()
    if request.method == "POST":
        user_form = ExtendsUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('/')
    context = {'tags': tags, 'formprofile': profileform, 'formuser': userform}
    return render(request, 'signup.html', context=context)


def paginate(object_list, request):
    try:
        limit = int(request.GET.get('limit', 5))
    except ValueError:
        limit = 5
    if limit > 100:
        limit = 5
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(object_list, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page
