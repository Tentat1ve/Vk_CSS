# qa/urls.py
from django.urls import path
from . import views

app_name = 'qa'

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('question/<int:question_id>/', views.question, name='question'),
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    path('ask/', views.ask, name='ask'),
    path('question/<int:question_id>/answer/', views.add_answer, name='add_answer'),
]