from django import forms


class DoaminName(forms.Form):
    post = forms.CharField(max_length=100)
