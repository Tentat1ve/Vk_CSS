from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from qa.models import Question, Tag, Answer, Profile
import random
from faker import Faker

class Command(BaseCommand):
    help = 'Fill database with test data'
    
    def handle(self, *args, **options):
        fake = Faker()
        
        users = []
        for i in range(10):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='testpass123'
            )
            Profile.objects.get_or_create(user=user)
            users.append(user)
            self.stdout.write(f'Created user: {user.username}')
        
        tags = []
        tech_tags = ['python', 'django', 'javascript', 'react', 'vue', 'sql', 
                    'postgresql', 'docker', 'kubernetes', 'aws', 'git', 
                    'linux', 'nginx', 'redis', 'celery', 'rest', 'graphql',
                    'testing', 'deployment', 'security']
        
        for tag_name in tech_tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
        
        for i in range(100):
            question = Question.objects.create(
                title=fake.sentence(nb_words=8),
                content=fake.text(max_nb_chars=500),
                author=random.choice(users),
                votes=random.randint(0, 50)
            )
            
            question_tags = random.sample(tags, random.randint(2, 4))
            question.tags.add(*question_tags)
            
            for j in range(random.randint(1, 5)):
                Answer.objects.create(
                    content=fake.text(max_nb_chars=300),
                    question=question,
                    author=random.choice(users),
                    votes=random.randint(0, 30),
                    is_accepted=(j == 0 and random.choice([True, False]))
                )
            
            if i % 10 == 0:
                self.stdout.write(f'Created {i} questions...')
        
        self.stdout.write(self.style.SUCCESS('Successfully filled database!'))