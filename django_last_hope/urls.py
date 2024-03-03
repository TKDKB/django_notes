"""
URL configuration for django_last_hope project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import serve
from django.conf import settings
from django.urls import path, include, re_path
from django.contrib.auth.views import LoginView
from notes.views import home_page_view, create_note_view, show_note_view, greetings_page_view, edit_note_view,\
    about_us_page_view, filter_notes_view, author_notes_view, edit_user, HistoryShowView
from registration.views import change_password_receiver, send_email

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include("django.contrib.auth.urls")),
    # path('login', LoginView.as_view(), name="login"),
    # path('register', register, name="register"),
    path('accounts/register/', include("registration.urls")),

    path('main', home_page_view, name="home"),
    path('', greetings_page_view, name="greeting"),
    path('about_us', about_us_page_view, name="about-us"),
    path('create', create_note_view, name="new-note"),
    path('note/<note_uuid>', show_note_view, name="show-note"),
    path('edit/<note_uuid>', edit_note_view, name="edit-note"),
    path('filter', filter_notes_view, name="filter-notes"),
    path('user/<username>/posts', author_notes_view, name="author-notes"),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    path("__debug__/", include("debug_toolbar.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('profile/<username>', edit_user, name="profile"),
    path('send_reset_email', send_email, name='send-email'),
    path('profile/change_password/<uidb>/<token>/', change_password_receiver, name='change-password-reciever'),
    # path('profile/change_password_form/<uidb>/<token>/', actually_change_password, name='actually-change-password'),
    path('api/', include("notes.api.urls")),
    path('history/', HistoryShowView.as_view(), name='history'),
]
