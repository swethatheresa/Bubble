from django.forms import ModelForm,ModelMultipleChoiceField,CheckboxSelectMultiple
from django.contrib.auth.forms import UserCreationForm
from .models import *


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','email','college','city']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


# class UserForm(ModelForm):
#     the_choices = ModelMultipleChoiceField(queryset=Topic.objects.all(), required=False, widget=CheckboxSelectMultiple)
#     class Meta:
#         model = User
#         fields = '__all__'
        