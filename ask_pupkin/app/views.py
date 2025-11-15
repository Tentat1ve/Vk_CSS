from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return page_obj

def get_questions():
    questions = []
    for i in range(1, 30):
        questions.append({
            'id': i,
            'title': f'С чего начать знакомство с трэш-металом? {i}',
            'content': f'Хочу погрузиться в трэш-метал, но не знаю с каких альбомов начать. Какие группы и альбомы считаются must-listen для новичка? {i}',
            'votes': i * 3,
            'answers_count': i % 10,
            'tags': ['трэш-метал', 'новичкам', 'рекомендации'],
            'author': {'username': f'user{i}', 'avatar': 'ИП'},
            'created_at': '2 часа назад'
        })
    return questions

def get_hot_questions():
    hot_questions_data = [
        {
            'id': 101,
            'title': 'Какой альбом Metallica самый важный для трэш-метала?',
            'content': 'Обсуждение влияния Master of Puppets на развитие жанра и его значение для всей метал-сцены 80-х годов.',
            'votes': 247,
            'answers_count': 156,
            'tags': ['Metallica', 'классика', 'история'],
            'author': {'username': 'metal_expert', 'avatar': 'МЭ'},
            'created_at': '2 дня назад'
        },
        {
            'id': 102, 
            'title': 'Почему Reign in Blood считается эталоном трэш-метала?',
            'content': 'Анализ музыкальных особенностей и влияния альбома Slayer на последующие поколения.',
            'votes': 189,
            'answers_count': 89,
            'tags': ['Slayer', 'трэш-метал', 'классика'],
            'author': {'username': 'thrash_lover', 'avatar': 'ТЛ'},
            'created_at': '5 дней назад'
        },
    ]
    return hot_questions_data

def get_tag_questions(tag_name):
    questions = []
    for i in range(1, 15):
        questions.append({
            'id': i + 200,  # Другие ID
            'title': f'Вопрос о {tag_name} #{i}',
            'content': f'Это специфический вопрос о {tag_name}. Здесь обсуждаются особенности этого направления.',
            'votes': 20 + i * 2,
            'answers_count': 3 + i,
            'tags': [tag_name, 'обсуждение'],
            'author': {'username': f'fan_{tag_name}_{i}', 'avatar': 'ТГ'},
            'created_at': f'{i * 2} часов назад'
        })
    return questions

def test_view(request):
    return render(request, 'test.html')

def index(request):
    questions = get_questions()
    page_obj = paginate(questions, request, 10)
    return render(request, 'index.html', {
        'page_obj': page_obj,
        'questions': page_obj.object_list
    })

def hot_questions(request):
    questions = get_hot_questions() 
    page_obj = paginate(questions, request, 10)
    return render(request, 'hot.html', {
        'page_obj': page_obj,
        'questions': page_obj.object_list 
    })
    
def tag_questions(request, tag_name):
    questions = get_tag_questions(tag_name)
    page_obj = paginate(questions, request, 10)
    return render(request, 'tag.html', {
        'page_obj': page_obj,
        'questions': page_obj.object_list,
        'tag_name': tag_name
    })

def question_detail(request, question_id):
    questions = get_questions() + get_hot_questions() + get_tag_questions('трэш-метал')
    question = next((q for q in questions if q['id'] == question_id), None)
    
    if not question:
        raise Http404("Вопрос не найден")
    
    answers = []
    for i in range(1, 6):
        answers.append({
            'id': i,
            'content': f'Начни с классики "Большой четверки трэша": Metallica, Slayer, Megadeth, Anthrax. {i}',
            'votes': i * 2,
            'author': {'username': f'expert{i}', 'avatar': 'АС'},
            'created_at': f'{i} часа назад',
            'is_accepted': i == 1
        })
    
    return render(request, 'question.html', {
        'question': question,
        'answers': answers
    })

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def ask_view(request):
    return render(request, 'ask.html')

def profile_edit(request):
    return render(request, 'profile_edit.html')