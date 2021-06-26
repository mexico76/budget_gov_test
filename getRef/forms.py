from django import forms

class ReferenceForm(forms.Form):
    reference = forms.CharField(label='Ссылка')