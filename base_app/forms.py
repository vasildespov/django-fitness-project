from django.forms.widgets import ChoiceWidget, NumberInput, TextInput
from base_app.models import Article, Profile
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from base_app.validators import UsernameMinMaxLengthValidator, WeightHeightNegativeNumberValidator


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
            }
        ),
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
            }
        ),
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
            }
        ),
        validators=(UsernameMinMaxLengthValidator,),
    )
    email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Email Address"})
    )
    password1 = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password2 = forms.CharField(
        label="Repeat Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Repeat Password"}),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.pop("autofocus", None)

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise ValidationError("- Password must be between 8 and 20 symbols.")
        else:
            return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("- Passwords must match.")
        return password2

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError("- This username is already in use.")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise ValidationError("- This email address is already in use.")


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )

    class Meta:
        model = User
        fields = ("username", "password")

    def clean_username(self):
        data = self.cleaned_data["username"]
        if User.objects.filter(username=data).exists():
            return data
        raise ValidationError("- Invalid Username.")

    def clean_password(self):
        password = self.cleaned_data.get("password")
        username = self.cleaned_data.get("username")
        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise ValidationError("- Invalid Password")
            return password


class UserUpdateForm(UserChangeForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
            }
        ),
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
            }
        ),
    )
    username = forms.CharField(
        error_messages={"unique": "- This username is already in use."},
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
            }
        ),
        validators=(UsernameMinMaxLengthValidator,),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
        ]


class ProfilePicForm(forms.ModelForm):
    class Meta:

        model = Profile
        fields = ["profile_pic"]
        widgets = {
            "profile_pic": forms.FileInput(attrs={"onchange": "previewFunc(this)"})
        }


class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ["author", "date", "slug"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Title",
                }
            ),
            "subtitle": forms.TextInput(attrs={"placeholder": "Subtitle"}),
            "category": forms.TextInput(attrs={"placeholder": "Category"}),
            "cover": forms.FileInput(attrs={"placeholder": ""}),
        }
        labels = {
            "title": "",
            "subtitle": "",
            "category": "",
            "content": "",
        }


class UserDataForm(forms.Form):
    sex_options = (
        ("","-"),
        ("Male", "Male"),
        ("Female", "Female"),
    )
    activity_options = (
        ("","-"),
        ("Sedentary", "Sedentary (0 workouts per week)"),
        ("Moderately Active", "Moderately Active (2-4 workouts per week)"),
        ("Very Active", "Very Active (5-7 workouts per week)"),
    )
    goal_options = (
        ("","-"),
        ("Maintain", "Maintain Weight"),
        ("Gain", "Gain Weight"),
        ("Lose", "Lose Weight"),
    )
    sex = forms.ChoiceField(choices=sex_options,required=True)
    age = forms.IntegerField(required=True,widget=NumberInput(attrs={'placeholder':'Age'}),validators=(WeightHeightNegativeNumberValidator,))
    weight_in_kg = forms.IntegerField(required=True,widget=NumberInput(attrs={'placeholder':'Weight'}),validators=(WeightHeightNegativeNumberValidator,))
    height_in_cm = forms.IntegerField(required=True,widget=NumberInput(attrs={'placeholder':'Height'}),validators=(WeightHeightNegativeNumberValidator,))
    activity = forms.ChoiceField(choices=activity_options,required=True,initial=activity_options[0])
    goal = forms.ChoiceField(choices=goal_options,required=True,initial=goal_options[0])