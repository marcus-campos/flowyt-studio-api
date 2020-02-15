from django.core.mail import send_mail as core_send_mail
from django.core.mail import EmailMultiAlternatives
import threading
from django.conf import settings


class EmailAsync(threading.Thread):
    def __init__(
        self,
        subject,
        to,
        from_email=settings.DEFAULT_FROM_EMAIL,
        fail_silently=True,
        body="",
        html="",
    ):
        self.subject = subject
        self.body = body
        self.to = to
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def send(self):
        return self.start()

    def run(self):
        msg = EmailMultiAlternatives(
            self.subject, self.body, self.from_email, self.recipient_list
        )
        if self.html:
            msg.attach_alternative(self.html, "text/html")
        msg.send(self.fail_silently)
