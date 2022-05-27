from django.forms import ModelForm
from .models import User,SparePartGood, SparePartOutRecord
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username','email', 'password1','password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username','email', 'bio']


class ManageForm(ModelForm):
    class Meta:
        model = SparePartGood
        fields = '__all__'

class ManageFormOuT(ModelForm):
    class Meta:
        model = SparePartOutRecord
        fields = '__all__'