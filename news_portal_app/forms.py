from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['heading', 'category', 'text_article', 'author']

    def clean(self):
        cleaned_data = super().clean()
        text_article = cleaned_data.get("text_article")
        heading = self.cleaned_data["heading"]

        if heading[0].islower():
            raise ValidationError(
                "Заголовок должен начинаться с заглавной буквы"
            )

        if text_article is not None and len(text_article) < 40:
            raise ValidationError({
                "text_article": "Текст статьи не может быть менее 40 символов."
            })

        return cleaned_data