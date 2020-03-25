from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.models import UserProfile
from apps.teams.builders import SubDomainBuilder
from apps.teams.models import TeamInvitation, Team
from apps.teams.serializers import TeamSerializer
from apps.workspaces.models import Environment
from utils import encodings as base_utils
from django.db import transaction

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True, label="Email Address")
    password = serializers.CharField(required=True, label="Password", style={"input_type": "password"})
    password_2 = serializers.CharField(
        required=True, label="Confirm Password", style={"input_type": "password"}
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    invite_code = serializers.CharField(required=False)

    class Meta(object):
        model = User
        fields = [
            "email",
            "password",
            "password_2",
            "first_name",
            "last_name",
            "invite_code",
        ]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        if len(value) < getattr(settings, "PASSWORD_MIN_LENGTH", 8):
            raise serializers.ValidationError(
                "Password should be atleast %s characters long." % getattr(settings, "PASSWORD_MIN_LENGTH", 8)
            )
        return value

    def validate_password_2(self, value):
        data = self.get_initial()
        password = data.get("password")
        if password != value:
            raise serializers.ValidationError("Passwords doesn't match.")
        return value

    def validate_invite_code(self, value):
        data = self.get_initial()
        email = data.get("email")
        if value:
            self.invitation = TeamInvitation.objects.validate_code(email, value)
            if not self.invitation:
                raise serializers.ValidationError("Invite code is not valid / expired.")
            self.team = self.invitation.team
        return value

    def create(self, validated_data):
        team = getattr(self, "team", None)

        user_data = {
            "email": validated_data.get("email"),
            "password": validated_data.get("password"),
            "first_name": validated_data.get("first_name"),
            "last_name": validated_data.get("last_name"),
        }

        is_active = True if team else False
        with transaction.atomic():

            user = UserProfile.objects.create_user_profile(
                data=user_data,
                is_active=is_active,
                site=get_current_site(self.context["request"]),
                send_email=True,
            )

            if team:
                team.members.add(user)

            if hasattr(self, "invitation"):
                TeamInvitation.objects.accept_invitation(self.invitation)

            TeamInvitation.objects.decline_pending_invitations(email_ids=[validated_data.get("email")])

            personal_team = Team()
            personal_team.name = "Private"
            personal_team.organization = "Personal"
            personal_team.description = "Your private personal team."
            personal_team.owner = user
            personal_team.can_delete = False
            personal_team.is_personal = True
            mail_prefix = user.email.split("@")[0]
            personal_team.sub_domain_url = SubDomainBuilder().build_sub_domain_url(
                personal_team.organization, mail_prefix
            )
            personal_team.members.set([user])
            personal_team.save()

        return validated_data


class PasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        # Not validating email to have data privacy.
        # Otherwise, one can check if an email is already existing in database.
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):

    token_generator = default_token_generator

    def __init__(self, *args, **kwargs):
        context = kwargs["context"]
        uidb64, token = context.get("uidb64"), context.get("token")
        if uidb64 and token:
            uid = base_utils.base36decode(uidb64)
            self.user = self.get_user(uid)
            self.valid_attempt = self.token_generator.check_token(self.user, token)
        super(PasswordResetConfirmSerializer, self).__init__(*args, **kwargs)

    def get_user(self, uid):
        try:
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    new_password = serializers.CharField(
        style={"input_type": "password"}, label="New Password", write_only=True
    )
    new_password_2 = serializers.CharField(
        style={"input_type": "password"}, label="Confirm New Password", write_only=True
    )

    def validate_new_password_2(self, value):
        data = self.get_initial()
        new_password = data.get("new_password")
        if new_password != value:
            raise serializers.ValidationError("Passwords doesn't match.")
        return value

    def validate(self, data):
        if not self.valid_attempt:
            raise serializers.ValidationError("Operation not allowed.")
        return data


class UserSerializer(serializers.ModelSerializer):

    teams = TeamSerializer(many=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "teams"]


class UserProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ["user", "has_email_verified"]


class TokenObtainPairWithUserInfoSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = UserProfileSerializer()
        data["user"] = user.to_representation(self.user.userprofile)
        return data
