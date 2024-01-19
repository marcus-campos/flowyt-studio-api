import datetime
import hashlib
import re
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.crypto import get_random_string

from utils.email import EmailAsync
from utils.models import AutoCreatedUpdatedMixin

User = get_user_model()

token_generator = default_token_generator

SHA1_RE = re.compile("^[a-f0-9]{40}$")


class Verification(models.Model):
    has_email_verified = models.BooleanField(default=False)

    class Meta:
        abstract = True


class UserProfileRegistrationManager(models.Manager):
    @transaction.atomic
    def create_user_profile(self, data, is_active=False, site=None, send_email=True):
        password = data.pop("password")
        user = User(**data)
        user.is_active = is_active
        user.set_password(password)
        user.save()

        user_profile = self.create_profile(user)

        if send_email:
            user_profile.send_activation_email(site)

        return user

    def create_profile(self, user):
        username = str(getattr(user, User.USERNAME_FIELD))
        hash_input = (get_random_string(5) + username).encode("utf-8")
        verification_key = hashlib.sha1(hash_input).hexdigest()

        profile = self.create(user=user, verification_key=verification_key)

        return profile

    def activate_user(self, verification_key):
        if SHA1_RE.search(verification_key.lower()):
            try:
                user_profile = self.get(verification_key=verification_key)
            except ObjectDoesNotExist:
                return None
            if not user_profile.verification_key_expired():
                user = user_profile.user
                user.is_active = True
                user.save()
                user_profile.verification_key = UserProfile.ACTIVATED
                user_profile.has_email_verified = True
                user_profile.save()
                return user
        return None

    def expired(self):
        now = timezone.now() if settings.USE_TZ else datetime.datetime.now()

        return self.exclude(
            models.Q(user__is_active=True) | models.Q(verification_key=UserProfile.ACTIVATED)
        ).filter(
            user__date_joined__lt=now
            - datetime.timedelta(getattr(settings, "VERIFICATION_KEY_EXPIRY_DAYS", 4))
        )

    @transaction.atomic
    def delete_expired_users(self):
        for profile in self.expired():
            user = profile.user
            profile.delete()
            user.delete()


class UserProfile(AutoCreatedUpdatedMixin, Verification):
    ACTIVATED = "ALREADY ACTIVATED"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    verification_key = models.CharField(max_length=40)
    objects = UserProfileRegistrationManager()

    class Meta:
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"

    def __str__(self):
        return str(self.user)

    def verification_key_expired(self):
        expiration_date = datetime.timedelta(days=getattr(settings, "VERIFICATION_KEY_EXPIRY_DAYS", 4))

        return self.verification_key == self.ACTIVATED or (
            self.user.date_joined + expiration_date <= timezone.now()
        )

    def send_activation_email(self, site):
        context = {
            "verification_key": self.verification_key,
            "expiration_days": getattr(settings, "VERIFICATION_KEY_EXPIRY_DAYS", 4),
            "user": self.user,
            "site": getattr(settings, "STUDIO_BASE_DOMAIN_URL", None),
            "site_name": getattr(settings, "SITE_NAME", None),
        }

        subject = render_to_string("registration/activation_email_subject.txt", context)
        subject = "".join(subject.splitlines())
        message = render_to_string("registration/activation_email_content.txt", context)
        EmailAsync(subject=subject, to=[self.user.email], html=message).send()

    def send_password_reset_email(self, site):
        context = {
            "email": self.user.email,
            "site": getattr(settings, "STUDIO_BASE_DOMAIN_URL", None),
            "site_name": getattr(settings, "SITE_NAME", None),
            "uid": str(uuid.uuid4()),
            "user": self.user,
            "token": token_generator.make_token(self.user),
        }
        subject = render_to_string("password_reset/password_reset_email_subject.txt", context)
        subject = "".join(subject.splitlines())
        message = render_to_string("password_reset/password_reset_email_content.txt", context)
        EmailAsync(subject=subject, to=[self.user.email], html=message).send()
