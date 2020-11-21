from base_app.views import ArticleDeleteView, ArticleEditView, ArticleDetailView, BlogView, CreateArticleView, HomePageView, LoginPageView, LogoutPageView, RegisterPageView, UserProfileView, like
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register/', RegisterPageView.as_view(),name='register'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
    path('profile/<slug:slug>/', UserProfileView.as_view(), name='profile page'),
    path('article/create/', CreateArticleView.as_view(), name='create article'),
    path('article/details/<int:pk>-<slug:slug>/', ArticleDetailView.as_view(), name='article detail'),
    path('article/like/<int:pk>/', like, name='like article'),
    path('article/edit/<int:pk>-<slug:slug>/', ArticleEditView.as_view(), name='article edit'),
    path('article/delete/<int:pk>/', ArticleDeleteView.as_view(), name='article delete')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)