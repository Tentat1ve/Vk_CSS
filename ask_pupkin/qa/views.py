from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Count, Q
from .models import Question, Answer, Tag, Profile
from .forms import LoginForm, SignUpForm, ProfileEditForm, AskQuestionForm, AnswerForm
from .utils import paginate

def index(request):
    """Главная страница - новые вопросы"""
    questions = Question.objects.all().select_related('author').prefetch_related('tags')
    questions = questions.annotate(answers_count=Count('answers'))
    questions = questions.order_by('-created_at')
    
    page_obj = paginate(questions, request, per_page=20)
    
    context = {
        'page_obj': page_obj,
        'questions': page_obj.object_list,
        'page_title': 'Новые вопросы',
        'description': 'Свежие вопросы от сообщества'
    }
    return render(request, 'index.html', context)

def hot(request):
    """Лучшие вопросы"""
    questions = Question.objects.all().select_related('author').prefetch_related('tags')
    questions = questions.annotate(answers_count=Count('answers'))
    questions = questions.order_by('-votes', '-created_at')
    
    page_obj = paginate(questions, request, per_page=20)
    
    context = {
        'page_obj': page_obj,
        'questions': page_obj.object_list,
        'page_title': 'Лучшие вопросы',
        'description': 'Самые популярные вопросы сообщества'
    }
    return render(request, 'hot.html', context)

def tag(request, tag_name):
    """Вопросы по тегу"""
    tag_obj = get_object_or_404(Tag, name=tag_name)
    questions = Question.objects.filter(tags=tag_obj).select_related('author').prefetch_related('tags')
    questions = questions.annotate(answers_count=Count('answers'))
    questions = questions.order_by('-created_at')
    
    page_obj = paginate(questions, request, per_page=20)
    
    context = {
        'page_obj': page_obj,
        'questions': page_obj.object_list,
        'tag': tag_obj,
        'page_title': f'Вопросы по тегу "{tag_name}"',
        'description': f'Все вопросы с тегом {tag_name}'
    }
    return render(request, 'tag.html', context)

def question(request, question_id):
    """Страница вопроса"""
    question_obj = get_object_or_404(
        Question.objects.select_related('author')
                       .prefetch_related('tags'),
        id=question_id
    )
    
    # Получаем ответы с пагинацией
    answers = question_obj.answers.all().select_related('author')
    page_obj = paginate(answers, request, per_page=10)
    
    # Форма для ответа
    answer_form = AnswerForm()
    
    context = {
        'question': question_obj,
        'answers': page_obj.object_list,
        'page_obj': page_obj,
        'answer_form': answer_form,
        'page_title': question_obj.title,
        'description': question_obj.content[:150]
    }
    return render(request, 'question.html', context)

def login_view(request):
    """Вход в систему"""
    next_url = request.GET.get('next', 'qa:index')
    
    if request.user.is_authenticated:
        return redirect(next_url)
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            
            return redirect(next_url)
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {
        'form': form,
        'next': next_url,
        'page_title': 'Вход в систему'
    })

def signup(request):
    """Регистрация"""
    if request.user.is_authenticated:
        return redirect('qa:index')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('qa:index')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {
        'form': form,
        'page_title': 'Регистрация'
    })

def logout_view(request):
    """Выход из системы"""
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', 'qa:index'))
    logout(request)
    return redirect(next_url)

@login_required
def profile_edit(request):
    """Редактирование профиля"""
    # Безопасное получение профиля
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Если профиль не существует, создаем его
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileEditForm(
            request.POST, 
            request.FILES, 
            instance=profile,
            user=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('qa:profile_edit')
    else:
        form = ProfileEditForm(
            instance=profile,
            user=request.user
        )
    
    return render(request, 'profile_edit.html', {
        'form': form,
        'page_title': 'Редактирование профиля'
    })

@login_required
def ask(request):
    """Задать вопрос"""
    if request.method == 'POST':
        form = AskQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            
            # Обработка тегов
            tags_list = form.cleaned_data['tags']
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)
            
            return redirect('qa:question', question_id=question.id)
    else:
        form = AskQuestionForm()
    
    return render(request, 'ask.html', {
        'form': form,
        'page_title': 'Задать вопрос',
        'description': 'Задайте вопрос сообществу экспертов'
    })

@login_required
def add_answer(request, question_id):
    """Добавление ответа"""
    if request.method == 'POST':
        question_obj = get_object_or_404(Question, id=question_id)
        form = AnswerForm(request.POST)
        
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question_obj
            answer.author = request.user
            answer.save()
            
            return redirect(reverse('qa:question', args=[question_id]) + f'#answer-{answer.id}')
    
    return redirect('qa:question', question_id=question_id)