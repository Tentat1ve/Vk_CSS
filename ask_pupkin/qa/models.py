# qa/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse

# === Модель Профиля ===
class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    avatar = models.ImageField(
        upload_to='avatars/', 
        null=True, 
        blank=True
    )
    nickname = models.CharField(
        max_length=50, 
        blank=True
    )
    
    def __str__(self):
        return f"Профиль: {self.user.username}"
    
    def get_avatar_display(self):
        """Возвращает инициалы, если нет аватарки"""
        if self.avatar:
            return self.avatar.url
        return self.user.username[:2].upper() if self.user.username else '??'
    
    def get_display_name(self):
        """Возвращает никнейм или имя пользователя"""
        return self.nickname if self.nickname else self.user.username

# Сигналы для автоматического создания профиля
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)

# === Модель Тега ===
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

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

# === Модель Вопроса ===
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
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('qa:question', args=[self.id])
    
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

# === Модель Ответа ===
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
        return f"Ответ на: {self.question.title[:50]}..."
    
    def get_author_initials(self):
        username = self.author.username
        return username[:2].upper() if len(username) >= 2 else 'US'
    
    def update_votes(self):
        """Обновляет счетчик голосов на основе лайков"""
        from django.db.models import Sum
        result = self.likes.aggregate(total=Sum('value'))
        self.votes = result['total'] or 0
        self.save()

# === Модель Лайка вопроса ===
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

# === Модель Лайка ответа ===
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