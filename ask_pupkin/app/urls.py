from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('questions/', views.index, name='index'),  # Новые вопросы
    path('hot/', views.hot, name='hot'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
]