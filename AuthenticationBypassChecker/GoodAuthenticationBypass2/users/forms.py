from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .models import User, UserManager, SecurityQuestionsInter

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        ## fields 지정해주는 것이 안전 (whitelisting)
        # fields = ('email', 'nickname', 'user_questions', 'user_answer')
        ## exclude 취약함 (blacklisting)
        ''' 
        결론적으로 'is_superuser'를 exclude에 포함안시키면 intercept해서 mass assignment attack이 가능함 단, exclude에 포함시키면 문제가 되지 않으나,
        만약 exclude에 포함안시키면 template에서 {{ form }}으로 하면 렌더링이 되서 보여서 괜찮은데(그렇게 사용하진 않겠지만), 
        만약 bootstrap을 사용하여 form을 렌더링할때 <div class="form group">안에 table로 class="form-control"로 항목을 추가하면 
        선택해서 렌더링 가능하기 때문에 취약점이 될 수 있음. 그래서 fields=(,)를 쓰는 것이 더 나음 (사용자가 수정할 수 있는 것만 정하고 나머지는 다 수정불가능)
        '''
        exclude = ['date_joined', 'groups',
                   'user_permissions', 'password', 'last_login', 'is_active', 'salt']

    password1 = forms.CharField(
        label=_('Password'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password'),
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password confirmation'),
                'required': 'True',
            }
        )
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_('Password')
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial['password']

class FindPasswordForm(forms.ModelForm):
    class Meta:
        model = SecurityQuestionsInter
        fields = ('user', 'security_questions', 'answer',)
