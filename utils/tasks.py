from DjangoWebsite import app
from typing import Union
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from . import text
from django.core.cache import cache
from django.template import loader


@shared_task(ignore_result=True)
def base_mail_sending(subject: str, message: str, recipe: Union[str, list], html_msg=""):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER, [recipe] if isinstance(recipe, (str, bytes)) else recipe,
        html_message=html_msg,
        fail_silently=True,
    )


@app.task
def mail_verify_sending(recipe: str):
    """
    Async sending mail verification code.
    Expiration: 10 minutes.

    e.g.
    >>> from utils import tasks
    >>> tasks.mail_verify("zmh13054618081@dingtalk.com")
    >>>

    """

    code = text.generate_ncode(6)

    base_mail_sending.delay(
        "Deeptrain | Mail Verify",
        "Your verification code is %s" % code,
        recipe,
        loader.render_to_string("mail.html", {"code": code}),
    )

    cache.set("mail-refresh", 1, 60, version=recipe)
    cache.set("mail-verify", code, 600, version=recipe)


def mail_verify(recipe: str) -> bool:
    if cache.get("mail-refresh", version=recipe):
        return False
    mail_verify_sending.delay(recipe)
    return True


def mail_validate(recipe: str, code: str) -> bool:
    return cache.get("mail-verify", version=recipe) == str(code)
