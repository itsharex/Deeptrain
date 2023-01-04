from django import forms
from mdeditor.fields import MDTextFormField


class BlogForm(forms.Form):
    title = forms.CharField(label="title", max_length=50)
    content = MDTextFormField(label="content", max_length=65535)
    preview = forms.CharField(label="preview", max_length=120)
