
from django import forms
from .models import Measurement, Post, CustomUser 





class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
        'title', 'image', 'content',]

class MeasurementModelForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ('destination',)