from django import forms

from posts.models import Post

class PostNumerologyForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'source', 'tags', )

        widgets = {
          'text': forms.Textarea(attrs={'rows':10, 'cols':60}),
        }
