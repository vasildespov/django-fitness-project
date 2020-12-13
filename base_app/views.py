from django.contrib.auth.models import User
from django.db.models import Q
from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from base_app.models import Article, Like, Profile
from django.urls.base import reverse, reverse_lazy
from base_app.forms import (
    ChangePasswordForm,
    CreateArticleForm,
    LoginForm,
    ProfilePicForm,
    RegisterForm,
    UserDataForm,
    UserUpdateForm,
)
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import math


class HomePageView(TemplateView):
    template_name = "index.html"


class RegisterPageView(CreateView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("login")

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("home"))
        return super().dispatch(*args, **kwargs)


class BlogView(ListView):
    template_name = "blog.html"
    model = Article
    ordering = ["-date"]
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            liked = Like.objects.all().filter(user=self.request.user)
            titles = []
            for item in liked:
                titles.append(item.article.title)
            context["titles"] = titles
        return context

class LoginPageView(LoginView):
    template_name = "login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class LogoutPageView(LoginRequiredMixin, LogoutView):
    pass


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile.html"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liked"] = Like.objects.all().filter(user=self.request.user)
        context["userprofile"] = Profile.objects.get(user=self.request.user)
        context["created"] = Article.objects.all().filter(author=self.request.user)
        return context


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "profile-edit.html"
    form_class = UserUpdateForm

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy("profile page"))


class UserProfilePicEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "profile-pic-edit.html"
    form_class = ProfilePicForm

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy("profile page"))


class CreateArticleView(LoginRequiredMixin, CreateView):
    form_class = CreateArticleForm
    template_name = "create-article.html"

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = User.objects.get(username=self.request.user)
        article.save()

        return HttpResponseRedirect(reverse_lazy("blog"))


class ArticleDetailView(DetailView):
    model = Article
    template_name = "article-page.html"
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            liked = Like.objects.all().filter(user=self.request.user)
            titles = []
            for item in liked:
                titles.append(item.article.title)
            context["titles"] = titles
        return context

class ArticleEditView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = CreateArticleForm
    template_name = "article-edit.html"
    query_pk_and_slug = True

    def get_object(self):
        return get_object_or_404(
            Article, pk=self.kwargs["pk"], slug=self.kwargs["slug"]
        )

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = User.objects.get(username=self.request.user)
        article.save()
        return HttpResponseRedirect(reverse_lazy("blog"))

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            if self.request.user != self.get_object().author:
                return HttpResponseForbidden("You are not the author of this article.")
        return super().dispatch(self.request, *args, **kwargs)


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("blog")


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = "change-password.html"
    success_url = reverse_lazy("profile page")


@login_required
def like(request, pk):
    user = request.user
    article = get_object_or_404(Article, pk=request.POST.get("article_pk"))
    try:
        like = Like.objects.get(user=user, article=article)
        like.delete()
    except Like.DoesNotExist:
        like = Like(user=user, article=article)
        like.save()
    return HttpResponseRedirect(reverse_lazy("blog"))


@login_required
def calculate(request):

    if request.method == "POST":
        form = UserDataForm(request.POST)
        if form.is_valid():
            bmr_male = (
                66
                + (13.7 * form.cleaned_data["weight_in_kg"])
                + (5 * form.cleaned_data["height_in_cm"])
                - (6.8 * form.cleaned_data["age"])
            )
            bmr_female = (
                655
                + (9.6 * form.cleaned_data["weight_in_kg"])
                + (1.8 * form.cleaned_data["height_in_cm"])
                - (4.7 * form.cleaned_data["age"])
            )
            gain = 0
            maintain = 0
            lose = 0
            if form.cleaned_data["sex"] == "Male":
                if form.cleaned_data["activity"] == "Sedentary":
                    maintain = bmr_male * 1.2
                    gain = maintain + 300
                    lose = maintain - 300
                elif form.cleaned_data["activity"] == "Moderately Active":
                    maintain = bmr_male * 1.55
                    gain = maintain + 300
                    lose = maintain - 300
                elif form.cleaned_data["activity"] == "Very Active":
                    maintain = bmr_male * 1.725
                    gain = maintain + 300
                    lose = maintain - 300
            elif form.cleaned_data["sex"] == "Female":
                if form.cleaned_data["activity"] == "Sedentary":
                    maintain = bmr_female * 1.2
                    gain = maintain + 300
                    lose = maintain - 300
                elif form.cleaned_data["activity"] == "Moderately Active":
                    maintain = bmr_female * 1.55
                    gain = maintain + 300
                    lose = maintain - 300
                elif form.cleaned_data["activity"] == "Very Active":
                    maintain = bmr_female * 1.725
                    gain = maintain + 300
                    lose = maintain - 300

            return render(
                request,
                "calorie-calc.html",
                context={
                    "form": form,
                    "result": {
                        "lose": math.floor(lose),
                        "maintain": math.floor(maintain),
                        "gain": math.floor(gain),
                    },
                },
            )
    else:
        form = UserDataForm()

    return render(request, "calorie-calc.html", context={"form": form})


class SearchArticlesView(ListView):
    template_name = "searched-blog.html"
    model = Article
    ordering = ["-date"]
    context_object_name = "search_results"
    paginate_by = 4

    def get_queryset(self):
        result = super(SearchArticlesView, self).get_queryset()
        query = self.request.GET.get("search")
        if len(query) > 0:
            found_articles = Article.objects.filter(
                Q(title__icontains=query)
            )
            result = found_articles
        return result

    def get_context_data(self, **kwargs):
        context = super(SearchArticlesView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get("search")
        if not self.request.user.is_anonymous:
            liked = Like.objects.all().filter(user=self.request.user)
            titles = []
            for item in liked:
                titles.append(item.article.title)
            context["titles"] = titles
        return context
