from base_app.forms import LoginForm, RegisterForm
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView


class HomePageView(TemplateView):
    template_name = "index.html"


class RegisterPageView(CreateView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = "/login/"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(*args, **kwargs)


class LoginPageView(LoginView):
    template_name = "login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True