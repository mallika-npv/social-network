
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("count/<int:id>", views.count, name="count"),
    path("uncount/<int:id>", views.uncount, name="uncount"),
    path("f_page", views.f_page, name="f_page"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("alike/<int:id>", views.alike, name="alike"),
    path("rlike/<int:id>", views.rlike, name="rlike"),
]
