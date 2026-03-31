from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone

# === Профиль пользователя ===
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.CharField(max_length=2, default='US')
    
    def __str__(self):
        return f"Profile of {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.avatar:
            # Генерируем аватар из имени пользователя
            username = self.user.username
            if len(username) >= 2:
                self.avatar = username[:2].upper()
            else:
                self.avatar = 'US'
        super().save(*args, **kwargs)

# === Тег ===
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('tag', args=[self.name])

# === Менеджер вопросов ===
class QuestionManager(models.Manager):
    def new_questions(self):
        """Новые вопросы (по дате создания)"""
        return self.get_queryset().order_by('-created_at')
    
    def best_questions(self):
        """Лучшие вопросы (по количеству голосов)"""
        return self.get_queryset().order_by('-votes', '-created_at')
    
    def questions_by_tag(self, tag_name):
        """Вопросы по конкретному тегу"""
        return self.get_queryset().filter(tags__name=tag_name).order_by('-created_at')

# === Вопрос ===
class Question(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField(Tag, related_name='questions')
    created_at = models.DateTimeField(default=timezone.now)
    votes = models.IntegerField(default=0)
    
    objects = QuestionManager()
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['votes']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('question', args=[self.id])
    
    def answers_count(self):
        return self.answers.count()
    
    def get_author_initials(self):
        username = self.author.username
        return username[:2].upper() if len(username) >= 2 else 'US'
    
    def update_votes(self):
        """Обновляет счетчик голосов на основе лайков"""
        from django.db.models import Sum
        result = self.likes.aggregate(total=Sum('value'))
        self.votes = result['total'] or 0
        self.save()

# === Ответ ===
class Answer(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(default=timezone.now)
    votes = models.IntegerField(default=0)
    is_accepted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-is_accepted', '-votes', '-created_at']
    
    def __str__(self):
        return f"Answer to {self.question.title}"
    
    def get_author_initials(self):
        username = self.author.username
        return username[:2].upper() if len(username) >= 2 else 'US'
    
    def update_votes(self):
        """Обновляет счетчик голосов на основе лайков"""
        from django.db.models import Sum
        result = self.likes.aggregate(total=Sum('value'))
        self.votes = result['total'] or 0
        self.save()

# === Лайк вопроса ===
class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_likes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')
    value = models.SmallIntegerField()  # +1 или -1
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['user', 'question']
        constraints = [
            models.CheckConstraint(
                check=models.Q(value__in=[-1, 1]),
                name='question_like_value_check'
            )
        ]
    
    def save(self, *args, **kwargs):
        if self.value not in [1, -1]:
            raise ValidationError("Value must be 1 or -1")
        super().save(*args, **kwargs)
        self.question.update_votes()
    
    def delete(self, *args, **kwargs):
        question = self.question
        super().delete(*args, **kwargs)
        question.update_votes()

# === Лайк ответа ===
class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_likes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')
    value = models.SmallIntegerField()  # +1 или -1
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['user', 'answer']
        constraints = [
            models.CheckConstraint(
                check=models.Q(value__in=[-1, 1]),
                name='answer_like_value_check'
            )
        ]
    
    def save(self, *args, **kwargs):
        if self.value not in [1, -1]:
            raise ValidationError("Value must be 1 or -1")
        super().save(*args, **kwargs)
        self.answer.update_votes()
    
    def delete(self, *args, **kwargs):
        answer = self.answer
        super().delete(*args, **kwargs)
        answer.update_votes()