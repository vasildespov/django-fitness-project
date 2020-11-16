from base_app.views import HomePageView, LoginPageView, LogoutPageView, RegisterPageView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("register/", RegisterPageView.as_view(), name="register"),
    path("login/", LoginPageView.as_view(), name="login"),
    path('logout/', LogoutPageView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
