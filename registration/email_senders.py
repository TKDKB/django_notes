from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class BasicEmailSender:
    template_name = None
    id_field = "pk"
    subject = None

    def __init__(self, request: WSGIRequest, user: AbstractUser):
        self._request = request
        self._user = user

    def get_template_name(self):
        if not self.template_name:
            raise NotImplemented("укажите название шаблона")
        return self.template_name

    def get_subject(self):
        if not self.subject:
            raise NotImplemented("укажите тему письма")
        return self.subject

    def get_domain(self):
        return str(get_current_site(self._request))

    def get_token(self):
        return default_token_generator.make_token(self._user)

    def get_user_base_64(self):
        return urlsafe_base64_encode(force_bytes(getattr(self._user, self.id_field)))

    def get_mail_body(self):
        context = {
            "user": self._user,
            "domain": self.get_domain(),
            "token": self.get_token(),
            "uidb64": self.get_user_base_64(),
        }
        return render_to_string(self.get_template_name(), context)

    def send_mail(self):
        mail = EmailMultiAlternatives(
            subject=self.get_subject() + "на сайте" + self.get_domain(),
            to=[self._user.email]
        )
        mail.attach_alternative(self.get_mail_body(), "text/html")
        mail.send()


class PasswordResetEmailSender(BasicEmailSender):
    template_name = "registration/password-reset.html"
    subject = "Password Reset"
    id_field = "id"


