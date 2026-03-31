# qa/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Question, Answer, Tag
from .utils import paginate

def index(request):
    questions = Question.objects.new_questions()
    questions = Question.objects.all().select_related('author').prefetch_related('tags')
    page_obj = paginate(questions, request, per_page=20)
    
    context = {
        'page_obj': page_obj,
        'questions': page_obj.object_list,
        'page_title': 'Новые вопросы',
        'description': 'Свежие вопросы от сообщества'
    }
    return render(request, 'index.html', context)

def hot(request):
    questions = Question.objects.best_questions()
    questions = Question.objects.all().order_by('-votes', '-created_at')
    page_obj = paginate(questions, request, per_page=20)
    
    context = {
        'page_obj': page_obj,
        'questions': page_obj.object_list,
        'page_title': 'Лучшие вопросы',
        'description': 'Самые популярные вопросы сообщества'
    }
    return render(request, 'hot.html', context)

def tag(request, tag_name):
    questions = Question.objects.questions_by_tag(tag_name)
    questions = Question.objects.filter(tags__name=tag_name)
    page_obj = paginate(questions, request, per_page=20)
    
    context = {
        'page_obj': page_obj,
        'questions': page_obj.object_list,
        'tag_name': tag_name,
        'page_title': f'Вопросы по тегу "{tag_name}"',
        'description': f'Все вопросы с тегом {tag_name}'
    }
    return render(request, 'tag.html', context)

def question(request, question_id):
    """Страница вопроса"""
    question_obj = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question_obj)
    
    context = {
        'question': question_obj,
        'answers': answers,
        'page_title': question_obj.title,
        'description': question_obj.content[:150]
    }
    return render(request, 'question.html', context)

@login_required
def ask(request):
    """Задать вопрос"""
    return render(request, 'ask.html', {
        'page_title': 'Задать вопрос',
        'description': 'Задайте вопрос сообществу экспертов'
    })

# Аутентификация
def login_view(request):
    """Вход в систему"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('qa:index')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {
        'form': form,
        'page_title': 'Вход в систему'
    })

def logout_view(request):
    """Выход из системы"""
    logout(request)
    return redirect('qa:index')

def signup(request):
    """Регистрация"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('qa:index')
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {
        'form': form,
        'page_title': 'Регистрация'
    })