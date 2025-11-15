import os
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike

class Command(BaseCommand):
    help = 'Fill database with test data'
    
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio for data generation')
    
    def handle(self, *args, **options):
        ratio = options['ratio']
        
        self.stdout.write(f'Generating data with ratio {ratio}...')
        
        num_users = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_tags = ratio
        num_question_likes = ratio * 100
        num_answer_likes = ratio * 100
        
        self.stdout.write('Cleaning old data...')
        QuestionLike.objects.all().delete()
        AnswerLike.objects.all().delete()
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Tag.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
        
        self.stdout.write(f'Generating {num_users} users...')
        users = []
        for i in range(num_users):
            user = User.objects.create_user(
                username=f'user_{i}',
                email=f'user_{i}@example.com',
                password='password123',
                first_name=f'User{i}',
                last_name=f'Testov'
            )
            profile = Profile.objects.create(user=user)
            users.append(user)
            if i % 1000 == 0:
                self.stdout.write(f'  Created {i} users...')
        
        self.stdout.write(f'Generating {num_tags} tags...')
        metal_genres = [
            'thrash-metal', 'death-metal', 'black-metal', 'heavy-metal', 
            'power-metal', 'doom-metal', 'progressive-metal', 'folk-metal',
            'symphonic-metal', 'industrial-metal', 'nu-metal', 'metalcore',
            'deathcore', 'grindcore', 'hardcore', 'sludge-metal'
        ]
        
        bands = [
            'metallica', 'slayer', 'megadeth', 'anthrax', 'iron-maiden', 
            'judas-priest', 'black-sabbath', 'motorhead', 'pantera', 
            'sepultura', 'kreator', 'sodom', 'destruction', 'tankard',
            'death', 'cannibal-corpse', 'morbid-angel', 'deicide',
            'mayhem', 'burzum', 'darkthrone', 'emperor',
            'opeth', 'gojira', 'meshuggah', 'tool', 'system-of-a-down'
        ]
        
        all_tag_names = metal_genres + bands
        tags = []
        for i in range(min(num_tags, len(all_tag_names))):
            tag_name = f"{all_tag_names[i % len(all_tag_names)]}-{i}"
            tag = Tag.objects.create(name=tag_name)
            tags.append(tag)
            if i % 100 == 0:
                self.stdout.write(f'  Created {i} tags...')
        
        self.stdout.write(f'Generating {num_questions} questions...')
        questions = []
        question_titles = [
            "Как начать слушать {tag}?",
            "Лучшие альбомы в жанре {tag}",
            "История развития {tag}",
            "Современные представители {tag}",
            "В чем особенности {tag}?",
            "Классические работы {tag}",
            "Технические аспекты {tag}",
            "Влияние {tag} на метал сцену",
            "Рекомендации по {tag}",
            "Разбор композиций {tag}"
        ]
        
        for i in range(num_questions):
            author = random.choice(users)
            tag_sample = random.choice(tags)
            title_template = random.choice(question_titles)
            title = title_template.format(tag=tag_sample.name)
            
            question = Question.objects.create(
                title=title,
                content=self.generate_question_content(tag_sample.name),
                author=author,
                votes=random.randint(0, 50)
            )
            
            question_tags = random.sample(tags, min(3, len(tags)))
            question.tags.set(question_tags)
            questions.append(question)
            
            if i % 1000 == 0:
                self.stdout.write(f'  Created {i} questions...')
        
        self.stdout.write(f'Generating {num_answers} answers...')
        answers = []
        for i in range(num_answers):
            question = random.choice(questions)
            author = random.choice(users)
            
            answer = Answer.objects.create(
                content=self.generate_answer_content(question),
                question=question,
                author=author,
                votes=random.randint(0, 20),
                is_accepted=random.choice([True, False]) if random.random() < 0.1 else False
            )
            answers.append(answer)
            
            if i % 10000 == 0:
                self.stdout.write(f'  Created {i} answers...')
        
        self.stdout.write(f'Generating {num_question_likes} question likes...')
        question_likes_created = 0
        while question_likes_created < num_question_likes:
            user = random.choice(users)
            question = random.choice(questions)
            try:
                QuestionLike.objects.create(
                    user=user,
                    question=question,
                    value=random.choice([1, -1])
                )
                question_likes_created += 1
                if question_likes_created % 10000 == 0:
                    self.stdout.write(f'  Created {question_likes_created} question likes...')
            except:
                pass  
        self.stdout.write(f'Generating {num_answer_likes} answer likes...')
        answer_likes_created = 0
        while answer_likes_created < num_answer_likes:
            user = random.choice(users)
            answer = random.choice(answers)
            try:
                AnswerLike.objects.create(
                    user=user,
                    answer=answer,
                    value=random.choice([1, -1])
                )
                answer_likes_created += 1
                if answer_likes_created % 10000 == 0:
                    self.stdout.write(f'  Created {answer_likes_created} answer likes...')
            except:
                pass 
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully generated:\n'
                f'- Users: {User.objects.count()}\n'
                f'- Tags: {Tag.objects.count()}\n'
                f'- Questions: {Question.objects.count()}\n'
                f'- Answers: {Answer.objects.count()}\n'
                f'- Question likes: {QuestionLike.objects.count()}\n'
                f'- Answer likes: {AnswerLike.objects.count()}'
            )
        )
    
    def generate_question_content(self, tag_name):
        contents = [
            f"Я недавно открыл для себя {tag_name} и хочу глубже погрузиться в этот жанр. "
            f"С чего лучше начать знакомство? Какие альбомы считаются обязательными к прослушиванию? "
            f"Также интересно узнать о современных представителях этого направления.",
            
            f"Изучаю историю развития {tag_name} и хочу понять ключевые моменты становления жанра. "
            f"Какие группы были pioneers? Как менялось звучание со временем? "
            f"Какое влияние оказал этот стиль на метал в целом?",
            
            f"Ищу рекомендации по {tag_name}. Уже знаком с базовыми вещами, но хочу открыть для себя "
            f"что-то новое. Какие малоизвестные, но достойные группы можно посоветовать? "
            f"Есть ли какие-то скрытые жемчужины в этом жанре?",
            
            f"Анализирую музыкальные особенности {tag_name}. Что характеризует этот стиль? "
            f"Какие техники игры, вокала, построения композиций typical для этого направления? "
            f"Как отличить {tag_name} от смежных жанров?",
        ]
        return random.choice(contents)
    
    def generate_answer_content(self, question):
        contents = [
            f"Отличный вопрос! На мой взгляд, стоит начать с классических работ. "
            f"В контексте {question.tags.first().name if question.tags.exists() else 'этого жанра'} "
            f"рекомендую обратить внимание на следующие альбомы...",
            
            f"Исходя из моего опыта, ключевыми моментами в развитии этого направления были... "
            f"Особенно стоит отметить влияние следующих групп и музыкантов.",
            
            f"Если вы уже familiar с основами, советую обратить внимание на менее mainstream проекты. "
            f"Вот несколько recommendations, которые могут вас заинтересовать...",
            
            f"С технической точки зрения, этот стиль характеризуется... "
            f"Особенности включают в себя специфические приемы игры, вокала и аранжировок.",
        ]
        return random.choice(contents)