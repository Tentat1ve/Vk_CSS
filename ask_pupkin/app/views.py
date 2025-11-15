from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from .models import Question, Tag, Answer
from .utils import paginate

def index(request):
    """
    Список новых вопросов
    """
    questions = Question.objects.new_questions().select_related('author').prefetch_related('tags')
    page_obj = paginate(questions, request, per_page=20)
    
    return render(request, 'index.html', {
        'page_obj': page_obj,
        'questions': page_obj.object_list,
    })

def hot(request):
    """
    Список лучших вопросов (по голосам)
    """
    questions = Question.objects.best_questions().select_related('author').prefetch_related('tags')
    page_obj = paginate(questions, request, per_page=20)
    
    return render(request, 'hot.html', {
        'page_obj': page_obj,
        'questions': page_obj.object_list,
    })

def tag(request, tag_name):
    """
    Список вопросов по тегу
    """
    tag_obj = get_object_or_404(Tag, name=tag_name)
    questions = Question.objects.questions_by_tag(tag_name).select_related('author').prefetch_related('tags')
    page_obj = paginate(questions, request, per_page=20)
    
    similar_tags = Tag.objects.exclude(name=tag_name)[:10]
    
    return render(request, 'tag.html', {
        'page_obj': page_obj,
        'questions': page_obj.object_list,
        'tag_name': tag_name,
        'similar_tags': similar_tags,
    })

def question(request, question_id):
    """
    Страница вопроса со списком ответов
    """
    question_obj = get_object_or_404(
        Question.objects.select_related('author').prefetch_related('tags'), 
        id=question_id
    )
    
    answers = Answer.objects.filter(question=question_obj).select_related('author')
    page_obj = paginate(answers, request, per_page=10)
    
    similar_questions = Question.objects.filter(
        tags__in=question_obj.tags.all()
    ).exclude(id=question_id).distinct()[:5]
    
    return render(request, 'question.html', {
        'question': question_obj,
        'page_obj': page_obj,
        'answers': page_obj.object_list,
        'similar_questions': similar_questions,
    })

def ask(request):
    """
    Страница задания вопроса (read-only версия)
    """
    return render(request, 'ask.html')

def login_view(request):
    """
    Страница входа (read-only версия)
    """
    return render(request, 'login.html')

def signup(request):
    """
    Страница регистрации (read-only версия)
    """
    return render(request, 'signup.html')

def home(request):
    """
    Домашняя страница с оригинальным контентом
    """
    return render(request, 'home.html')