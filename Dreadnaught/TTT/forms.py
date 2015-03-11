from django import forms
from TTT.models import scripts

class UploadFileForm(forms.Form):
    title = forms.CharField(label="Script Name", max_length = 50)
    file = forms.FileField()
    

class SelectGame(forms.Form):
    player1 = forms.ModelChoiceField(label = "Player 1", queryset=scripts.objects.all(), \
                                 required=False, empty_label='None')
    player2 = forms.ModelChoiceField(label = "Player 2", queryset=scripts.objects.all(), \
                                 required=False, empty_label='None')
    

class PlayGame(forms.Form):
    move = forms.IntegerField(label = "Move",  max_value = 8, min_value = 0)


class Login(forms.Form):
    username = forms.CharField(label="User Name", max_length = 20)
    password = forms.CharField(widget=forms.PasswordInput)


class Signup(forms.Form):
    username = forms.CharField(label="User Name", max_length = 20)
    email = forms.EmailField(label = "Email", max_length = 50)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, \
                               max_length = 50)
    confirm_pass = forms.CharField(label = "Confirm Password", \
                                   widget=forms.PasswordInput, max_length = 50)


class Change_Pass(forms.Form):
    prev_password = forms.CharField(label="Confirm Previous Password", \
                               widget=forms.PasswordInput, max_length = 50)
    new_password = forms.CharField(label="New Password", \
                              widget=forms.PasswordInput, max_length = 50)
    
