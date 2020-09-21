from django import forms


class DoaminName(forms.Form):
    post = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'url',
                                                                   'id': 'urladres', 'name': 'url',
                                                                   'placeholder': 'Add your website url'}))
