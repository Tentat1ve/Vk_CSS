from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Tag, Question, Answer

class Command(BaseCommand):
    help = 'Initialize with simple test data'
    
    def handle(self, *args, **options):
        # Очищаем старые данные (опционально)
        Question.objects.all().delete()
        Tag.objects.all().delete()
        User.objects.filter(username='testuser').delete()
        
        # Создаем тестового пользователя
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        Profile.objects.create(user=user, avatar='TU')
        
        # Создаем базовые теги
        tag1 = Tag.objects.create(name='трэш-метал')
        tag2 = Tag.objects.create(name='дэт-метал') 
        tag3 = Tag.objects.create(name='металлика')
        
        # Создаем простой вопрос
        question = Question.objects.create(
            title='Тестовый вопрос о трэш-метале',
            content='Это тестовый вопрос для проверки работы сайта.',
            author=user,
            votes=10
        )
        question.tags.add(tag1, tag3)
        
        Answer.objects.create(
            content='Это тестовый ответ на вопрос.',
            question=question,
            author=user,
            votes=5
        )
        
        self.stdout.write(self.style.SUCCESS('Simple test data created!'))