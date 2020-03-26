from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from . import serializers
from .builders import SubDomainBuilder
from .models import Team, TeamInvitation
from .permissions import IsTeamOwnerPermission
from .serializers import TeamSerializer
from ..accounts.models import UserProfile


class ListCreateTeamAPIView(generics.ListCreateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.TeamCreateSerializer
    queryset = Team.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            team = serializer.save(owner=request.user)
            team.members.add(request.user)

            builder = SubDomainBuilder()
            team.subdomain = builder.build_subdomain_url(team.organization, team.name)
            team.save()

            team_serializer = TeamSerializer(instance=team)

            return Response(team_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return self.queryset.filter(members__in=[self.request.user])


class RetrieveDestroyUpdateTeamAPIView(generics.UpdateAPIView, generics.RetrieveDestroyAPIView):

    permission_classes = (IsTeamOwnerPermission,)
    serializer_class = serializers.TeamSerializer
    queryset = Team.objects.all()

    def perform_destroy(self, instance):
        if not instance.can_delete:
            raise PermissionDenied(detail="The default Personal team cant be removed")
        return super(RetrieveDestroyUpdateTeamAPIView, self).perform_destroy(instance)

    def get(self, request, *args, **kwargs):
        team = self.queryset.get(pk=str(kwargs["pk"]))
        serializer = self.get_serializer(team)
        for index, value in enumerate(team.members.all()):
            member = {
                "id": str(value.id),
                "first_name": value.first_name,
                "last_name": value.last_name,
                "is_owner": True if str(value.id) == str(team.owner.id) else False,
                "email": value.email,
            }
            serializer.data["members"][index] = member
        return Response(serializer.data)


class InviteToTeamAPIView(generics.CreateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.TeamInvitationCreateSerializer
    queryset = TeamInvitation.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user, "team_pk": kwargs["pk"]}
        )
        if serializer.is_valid(raise_exception=True):
            email_ids = serializer.validated_data.get("emails")
            team = Team.objects.get(pk=kwargs["pk"])
            self.create_invitations(email_ids=email_ids, invited_by=request.user, team=team)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_invitations(self, email_ids, invited_by, team):
        invitations = [
            TeamInvitation(email=email_id, invited_by=invited_by, team=team) for email_id in email_ids
        ]
        invitations = TeamInvitation.objects.bulk_create(invitations)
        self.send_email_invites(invitations)

    def send_email_invites(self, invitations):
        # Sending email expected to be done asynchronously in production environment.
        for invitation in invitations:
            invitation.send_email_invite(get_current_site(self.request))


class RemoveFromTeamAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.TeamRemoveMemberSerializer
    queryset = Team.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user, "team_pk": kwargs["pk"]}
        )
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            team = Team.objects.get(pk=kwargs["pk"])
            team = self.remove_member(email, team)
            team_serializer = TeamSerializer(instance=team)
            return Response(team_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def remove_member(self, email, team):
        try:
            profile = UserProfile.objects.get(user__email=email)
            team.members.remove(profile.user)
        except:
            pass

        TeamInvitation.objects.filter(team=team, email=email).update(status=TeamInvitation.REMOVED)
        return team


class SubDomainURLBuilderView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.SubDomainURLBuilderSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)
        builder = SubDomainBuilder()
        url = builder.build_subdomain_url(
            serializer.validated_data["organization"], serializer.validated_data["team"]
        )
        return Response({"url": url}, status=status.HTTP_200_OK)
