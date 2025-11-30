from django.forms import ModelForm
from django import forms
from .models import Post, Comment

class PostForm(ModelForm):
    class Meta:
        model = Post 
        fields = ['title', 'description', 'image', 'topics', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter post title...',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Write your post content...',
                'rows': 5,
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-file-input',
            }),
            'topics': forms.CheckboxSelectMultiple(attrs={
                'class': 'topic-checkbox',
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
        }

    def clean_topics(self):
        topics = self.cleaned_data.get('topics')
        if topics and topics.count() > 3:
            raise forms.ValidationError("You can select at most 3 topics.")
        return topics