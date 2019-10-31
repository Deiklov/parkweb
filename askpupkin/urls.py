from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.question_list, name="question_list"),
    path('ask', views.ask, name="ask"),
    path('login', TemplateView.as_view(template_name="login.html")),
    path('register', TemplateView.as_view(template_name="signup.html")),
    path('question/<int:number>', views.question, name="question"),
    path('hot', TemplateView.as_view(template_name="index.html")),
    path('tag/<str:tag>', TemplateView.as_view(template_name="index.html")),
]
