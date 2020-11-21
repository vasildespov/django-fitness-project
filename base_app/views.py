from django.contrib.auth.models import User
from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from base_app.models import Article, Like
from django.urls.base import reverse_lazy
from base_app.forms import CreateArticleForm, LoginForm, RegisterForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


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
    paginate_by = 6

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
    slug_field = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liked"] = Like.objects.all().filter(user=self.request.user)
        context["created"] = Article.objects.all().filter(author=self.request.user)
        return context


class UserProfileEditView(LoginRequiredMixin, DetailView):
    pass


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


class ArticleEditView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = CreateArticleForm
    template_name = "article-edit.html"

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
        if self.request.user != self.get_object().author:
            return HttpResponseForbidden("You are not the author of this article.")
        return super().dispatch(self.request, *args, **kwargs)


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("blog")


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
