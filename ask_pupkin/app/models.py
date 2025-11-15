from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=2, default='US', help_text="Инициалы пользователя")
    
    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if not self.avatar:
            username = self.user.username
            if len(username) >= 2:
                self.avatar = username[:2].upper()
            else:
                self.avatar = 'US'
        super().save(*args, **kwargs)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('app:tag', args=[self.name])

class QuestionManager(models.Manager):
    def new_questions(self):
        """Новые вопросы (сортировка по дате создания)"""
        return self.order_by('-created_at')
    
    def best_questions(self):
        """Лучшие вопросы (сортировка по голосам)"""
        return self.order_by('-votes')
    
    def questions_by_tag(self, tag_name):
        """Вопросы по конкретному тегу"""
        return self.filter(tags__name=tag_name).order_by('-created_at')
    
    def with_answers_count(self):
        """Annotate questions with answers count"""
        from django.db.models import Count
        return self.annotate(answers_count=Count('answer'))

class Question(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)
    
    objects = QuestionManager()
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('app:question', args=[self.id])
    
    def answers_count(self):
        return self.answer_set.count()
    
    def get_author_initials(self):
        username = self.author.username
        if len(username) >= 2:
            return username[:2].upper()
        return 'US'
    
    def update_votes(self):
        """Обновляет счетчик голосов на основе лайков"""
        from django.db.models import Sum
        result = self.questionlike_set.aggregate(total=Sum('value'))
        self.votes = result['total'] or 0
        self.save()
    
    @property
    def update_dt(self):
        return self.updated_at
    
    @property
    def created_dt(self):
        return self.created_at

class Answer(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)
    is_accepted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-is_accepted', '-votes', '-created_at']
    
    def __str__(self):
        return f"Answer to {self.question.title}"
    
    def get_author_initials(self):
        username = self.author.username
        if len(username) >= 2:
            return username[:2].upper()
        return 'US'
    
    def update_votes(self):
        """Обновляет счетчик голосов на основе лайков"""
        from django.db.models import Sum
        result = self.answerlike_set.aggregate(total=Sum('value'))
        self.votes = result['total'] or 0
        self.save()
    
    @property
    def update_dt(self):
        return self.updated_at
    
    @property
    def created_dt(self):
        return self.created_at

class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.SmallIntegerField() 
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'question']
    
    def save(self, *args, **kwargs):
        if self.value not in [1, -1]:
            raise ValidationError("Value must be 1 or -1")
        super().save(*args, **kwargs)
        self.question.update_votes()
    
    def delete(self, *args, **kwargs):
        question = self.question
        super().delete(*args, **kwargs)
        question.update_votes()
    
    @property
    def created_dt(self):
        return self.created_at

class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    value = models.SmallIntegerField() 
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'answer']
    
    def save(self, *args, **kwargs):
        if self.value not in [1, -1]:
            raise ValidationError("Value must be 1 or -1")
        super().save(*args, **kwargs)
        self.answer.update_votes()
    
    def delete(self, *args, **kwargs):
        answer = self.answer
        super().delete(*args, **kwargs)
        answer.update_votes()
    
    @property
    def created_dt(self):
        return self.created_at