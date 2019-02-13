from django import forms

from posts.models import Post

class PostNumerologyForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'tags', )
