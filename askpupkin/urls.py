from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.question_list, name="question_list"),
    path('ask', views.ask, name="ask"),
    path('logout', views.logout_view, name="logout"),
    path('signup', views.signup, name="signup"),
    path('login', views.login_view, name="login"),
    path('question/<int:number>', views.question, name="question"),
    path('hot', views.question_list, name="hot"),
    path('tag/<str:tag>', views.question_list, name="tag"),
    path('cabinet', views.cabinet, name="settings"),
    path('profile/edit', views.cabinet, name="cabinet")
]
