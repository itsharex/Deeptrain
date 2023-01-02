from django import forms
from mdeditor.fields import MDTextFormField


class MarkdownForm(forms.Form):
    title = forms.CharField(max_length=50)
    content = MDTextFormField(label="content", max_length=65535)
    preview = forms.CharField(max_length=120)


