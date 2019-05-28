from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.core.exceptions import ValidationError


class RegisterFrom(Form):
    userinfo_name = fields.CharField(
        widget=widgets.TextInput(attrs={
            "class": 'form-control',
            "placeholder": "Name"
        })
    )
    userinfo_password = fields.CharField(
        widget=widgets.PasswordInput(attrs={
            "class": 'form-control',
            "placeholder": "Password"
        })
    )
    userinfo_password2 = fields.CharField(
        widget=widgets.PasswordInput(attrs={
            "class": 'form-control',
            "placeholder": "Password Confirmed"
        })
    )
    userinfo_email = fields.CharField(
        widget=widgets.EmailInput(attrs={
            "class": 'form-control',
            "placeholder": "Email"
        })
    )
    userinfo_avatar = fields.FileField(
        required=False,
        widget=widgets.FileInput(attrs={
            "id": "imgSelect",
            "style": "position: absolute;height:80px;width: 80px;top:0; left: 0;opacity: 0;"
        })
    )
    code = fields.CharField(
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'style': 'display: inline-block; width: 170px',
            'placeholder': 'Check Code'
        })
    )

    def __init__(self, request, *args, **kwargs):
        super(RegisterFrom, self).__init__(*args, **kwargs)
        self.request = request

    def clean_code(self):
        input_code = self.cleaned_data['code']
        session_code = self.request.session.get('code')
        if input_code.upper() == session_code.upper():
            return input_code
        raise ValidationError('验证码错误')

    def clean(self):
        p1 = self.cleaned_data.get('userinfo_password')
        p2 = self.cleaned_data.get('userinfo_password2')
        if p1 == p2:
            return self.cleaned_data
        self.add_error("userinfo_password2", ValidationError('密码不一致'))