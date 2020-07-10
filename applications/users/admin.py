from .models import User
from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserCreationForm(forms.ModelForm):
    password_field = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
    password_field_repeat = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def validate_password(self):
        password_field = self.cleaned_data.get('password_field')
        password_field_repeat = self.cleaned_data.get('password_field_repeat')
        if password_field and password_field_repeat and password_field != password_field_repeat:
            raise forms.ValidationError('Passwords don`t match')
        return password_field_repeat

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password_field'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean_password(self):
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_active')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff',)}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',)
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
# Register your models here.
