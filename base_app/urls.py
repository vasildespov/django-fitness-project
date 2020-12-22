from base_app.forms import UserUpdateForm
from base_app.views import ArticleDeleteView, ArticleEditView, ArticleDetailView, BlogView, ChangePasswordView, CreateArticleView,  HomePageView, LoginPageView, LogoutPageView, RegisterPageView, SearchArticlesView, UserProfileEditView, UserProfilePicEditView, UserProfileView, calculate, change_password_success, like, register_success
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register/', RegisterPageView.as_view(),name='register'),
    path('register-success/',register_success, name='register success'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('blog/search-results/', SearchArticlesView.as_view(), name='search'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
    path('profile/<slug:slug>/', UserProfileView.as_view(), name='profile page'),
    path('profile/edit/change-password/', ChangePasswordView.as_view(),name='change password'),
    path('profile/edit/change-password-success/',change_password_success, name='change password success'),
    path('profile/edit/change-username/',UserProfileEditView.as_view(), name='profile edit'),
    path('profile/edit/change-profile-picture/', UserProfilePicEditView.as_view(), name='profile pic edit'),
    path('article/create/', CreateArticleView.as_view(), name='create article'),
    path('article/details/<int:pk>-<slug:slug>/', ArticleDetailView.as_view(), name='article detail'),
    path('article/like/<int:pk>/', like, name='like article'),
    path('article/edit/<int:pk>-<slug:slug>/', ArticleEditView.as_view(), name='article edit'),
    path('article/delete/<int:pk>/', ArticleDeleteView.as_view(), name='article delete'),
    path('features/calorie-calculator/',calculate, name='calculator'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)