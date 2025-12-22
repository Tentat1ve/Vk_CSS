# qa/forms.py - СОЗДАТЬ НОВЫЙ ФАЙЛ
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Question, Answer, Tag, Profile

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Имя пользователя'
        }),
        label='Имя пользователя'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Пароль'
        }),
        label='Пароль'
    )
    
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox'}),
        label='Запомнить меня'
    )

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email'
        }),
        label='Email',
        required=True
    )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Получаем или создаем профиль
            profile, created = Profile.objects.get_or_create(user=user)
            profile.nickname = self.cleaned_data.get('nickname', '')
            profile.save()
        
        return user
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Имя пользователя'
        }),
        label='Имя пользователя',
        help_text='Не более 150 символов. Только буквы, цифры и @/./+/-/_'
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Пароль'
        }),
        label='Пароль',
        help_text='Минимум 8 символов'
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Подтверждение пароля'
        }),
        label='Подтверждение пароля'
    )
    
    nickname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Отображаемое имя'
        }),
        label='Никнейм',
        required=False,
        max_length=50
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'nickname')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Сохраняем никнейм в профиль
            profile = user.profile
            profile.nickname = self.cleaned_data.get('nickname', '')
            profile.save()
        
        return user

class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email'
        }),
        label='Email',
        required=True
    )
    
    nickname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Отображаемое имя'
        }),
        label='Никнейм',
        required=False,
        max_length=50
    )
    
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-input',
            'accept': 'image/*'
        }),
        label='Аватар',
        required=False
    )
    
    class Meta:
        model = Profile
        fields = ('nickname', 'avatar')
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['email'].initial = user.email
            self.fields['nickname'].initial = user.profile.nickname
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            profile.save()
        
        return profile

class AskQuestionForm(forms.ModelForm):
    tags = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Теги через запятую (python, django, web)'
        }),
        label='Теги',
        help_text='Введите теги через запятую'
    )
    
    class Meta:
        model = Question
        fields = ('title', 'content', 'tags')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Заголовок вопроса'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Подробное описание вопроса',
                'rows': 8
            }),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Текст вопроса',
        }
    
    def clean_tags(self):
        tags_str = self.cleaned_data['tags']
        tags_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        
        if len(tags_list) > 5:
            raise forms.ValidationError('Максимум 5 тегов')
        
        if len(tags_list) < 1:
            raise forms.ValidationError('Укажите хотя бы один тег')
        
        return tags_list

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Ваш ответ на вопрос',
                'rows': 6,
                'id': 'answer-content'
            }),
        }
        labels = {
            'content': 'Ваш ответ',
        }