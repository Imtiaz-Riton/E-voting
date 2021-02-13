from django import forms

class SignInForm(forms.Form):
    voter_id = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)