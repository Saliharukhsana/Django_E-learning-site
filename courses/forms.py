from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Quiz

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture', 'is_trainer']



class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))



class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = []
    
    def __init__(self, *args, **kwargs):
        quiz = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        
        if quiz:
            options = quiz.options
            self.fields['selected_option'] = forms.ChoiceField(
                choices=[(key, value) for key, value in options.items()],
                widget=forms.RadioSelect
            )