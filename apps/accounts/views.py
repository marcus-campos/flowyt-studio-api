from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from . import serializers
from .models import UserProfile

User = get_user_model()


class UserRegistrationAPIView(generics.CreateAPIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserRegistrationSerializer
    queryset = User.objects.all()


class UserEmailVerificationAPIView(views.APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request, verification_key):
        activated_user = self.activate(verification_key)
        if activated_user:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def activate(self, verification_key):
        return UserProfile.objects.activate_user(verification_key)


class PasswordResetAPIView(views.APIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.PasswordResetSerializer

    def post(self, request):
        user_profile = self.get_user_profile(request.data.get("email"))
        if user_profile:
            user_profile.send_password_reset_email(site=get_current_site(request))
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)

    def get_user_profile(self, email):
        try:
            user_profile = UserProfile.objects.get(user__email=email)
        except:
            return None
        return user_profile


class PasswordResetConfirmView(views.APIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data, context={"uidb64": kwargs["uidb64"], "token": kwargs["token"]},
        )

        if serializer.is_valid(raise_exception=True):
            new_password = serializer.validated_data.get("new_password")
            user = serializer.user
            user.set_password(new_password)
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(generics.RetrieveAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserProfileSerializer

    def get_object(self):
        return self.request.user.userprofile


class TokenObtainPairWithUserInfoView(TokenViewBase):
    serializer_class = serializers.TokenObtainPairWithUserInfoSerializer
