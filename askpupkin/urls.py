from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.question_list, name="question_list"),
    path('ask', views.ask, name="ask"),
    path('logout', auth_views.LogoutView, name="logout"),
    path('signup', views.signup, name="signup"),
    path('login', auth_views.LoginView.as_view(template_name="login.html")),
    path('question/<int:number>', views.question, name="question"),
    path('hot', views.question_list, name="hot"),
    path('tag/<str:tag>', views.question_list, name="tag"),
    path('cabinet', TemplateView.as_view(template_name="cabinet.html"), name="settings")
]
