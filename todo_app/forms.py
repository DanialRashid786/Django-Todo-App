from django import forms
from .models import *
# Reordering Form and View


class PositionForm(forms.Form):
    position = forms.CharField()





class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'complete']
