from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='',
        max_length=100,
        widget=forms.EmailInput(attrs={'placeholder': 'email', 'class': 'email-form'})
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'password-form'})
    )
