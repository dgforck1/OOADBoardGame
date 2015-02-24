from django import forms
from TTT.models import scripts

class UploadFileForm(forms.Form):
    title = forms.CharField(label="Script Name", max_length = 50)
    file = forms.FileField()
    
class SelectAI(forms.Form):
    ai1 = forms.ModelChoiceField(label = "AI 1", queryset=scripts.objects.all())
    ai2 = forms.ModelChoiceField(label = "AI 2", queryset=scripts.objects.all())
    
class HumanGame(forms.Form):
    ai1 = forms.ModelChoiceField(label = "AI 1", queryset=scripts.objects.all(), required=False, empty_label=None)
    ai2 = forms.ModelChoiceField(label = "AI 2", queryset=scripts.objects.all(), required=False, empty_label=None)