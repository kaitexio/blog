from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(), max_length=4000)
    class Meta:
        model = Post
        fields = ('title', 'text', 'origin')


