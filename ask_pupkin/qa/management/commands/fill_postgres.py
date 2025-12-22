from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from qa.models import Question, Tag, Answer, Profile
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Заполняет PostgreSQL базу тестовыми данными'
    
    def handle(self, *args, **options):
        self.stdout.write('🚀 Начинаю заполнение PostgreSQL базы...')
        
        # 1. СОЗДАЕМ ПОЛЬЗОВАТЕЛЕЙ
        users = []
        for i in range(10):
            user = User.objects.create_user(
                username=f'user{i+1}',
                email=f'user{i+1}@example.com',
                password='password123'
            )
            Profile.objects.create(user=user)
            users.append(user)
            self.stdout.write(f'✓ Пользователь user{i+1} создан')
        
        # 2. СОЗДАЕМ ТЕГИ
        tech_tags = [
            'python', 'django', 'javascript', 'react', 'vue', 
            'sql', 'postgresql', 'docker', 'git', 'linux',
            'html', 'css', 'api', 'rest', 'testing'
        ]
        
        tags = []
        for tag_name in tech_tags:
            tag = Tag.objects.create(name=tag_name)
            tags.append(tag)
            self.stdout.write(f'✓ Тег {tag_name} создан')
        
        # 3. СОЗДАЕМ ВОПРОСЫ
        for i in range(50):
            author = random.choice(users)
            num_tags = random.randint(2, 4)
            selected_tags = random.sample(tags, num_tags)
            
            # Создаем вопрос
            question = Question.objects.create(
                title=f'Вопрос #{i+1} о {selected_tags[0].name}',
                content=f'Подробный вопрос о {selected_tags[0].name} и его использовании с {selected_tags[1].name if len(selected_tags) > 1 else "другими технологиями"}.',
                author=author,
                votes=random.randint(0, 30),
                created_at=datetime.now() - timedelta(days=random.randint(0, 100))
            )
            
            # Добавляем теги
            question.tags.add(*selected_tags)
            
            # 4. СОЗДАЕМ ОТВЕТЫ
            for j in range(random.randint(1, 5)):
                answer_author = random.choice([u for u in users if u != author])
                Answer.objects.create(
                    content=f'Это ответ #{j+1} на вопрос о {selected_tags[0].name}.',
                    question=question,
                    author=answer_author,
                    votes=random.randint(0, 15),
                    is_accepted=(j == 0 and random.choice([True, False])),
                    created_at=question.created_at + timedelta(days=random.randint(1, 10))
                )
            
            if (i + 1) % 10 == 0:
                self.stdout.write(f'✓ Создано вопросов: {i + 1}')
        