from django import forms

from authentication.models import CustomUser


class UserAdninForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = ('user_permissions',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super(UserAdninForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
