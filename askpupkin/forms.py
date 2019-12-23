from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': "form-control"}))


class ExtendsUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=60)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user


class ExtnedsUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # self.fields['user'].widget = forms.HiddenInput()


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'content', 'tag')

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = "Enter title"
        self.fields['content'].widget.attrs['placeholder'] = "Enter question content"
        self.fields['tag'].widget.attrs['placeholder'] = "Enter tags"


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("content",)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
