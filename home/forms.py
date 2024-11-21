from django import forms


class SignUpForm(forms.Form):
    email = forms.EmailField(required=True)
    username = forms.CharField(min_length=5, max_length=30, required=True)
    password = forms.CharField(required=True)
    code = forms.CharField(min_length=5, max_length=5, required=False)


class LoginForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=30, required=True)
    password = forms.CharField(required=True)


class SendMessageForm(forms.Form):
    message = forms.CharField(max_length=2048, required=True)
    room = forms.CharField(max_length=36, required=True)
    reply_id = forms.IntegerField(required=False)
