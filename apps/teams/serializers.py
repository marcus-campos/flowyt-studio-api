from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.hosts.serializers import HostSerializer
from apps.teams.models import Team, TeamInvitation

User = get_user_model()


class TeamSerializer(serializers.ModelSerializer):
    team_hosts = HostSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "owner",
            "members",
            "can_delete",
            "subdomain",
            "team_hosts",
            "is_personal",
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        all_members = [{"email": instance.owner.email, "status": TeamInvitation.ACCEPTED_TEXT}]
        invitations = instance.teaminvitation_set.all().values("email", "status")
        members_mail = instance.members.all().values_list("email", flat=True)

        for invitation in invitations:
            if not invitation["status"] == TeamInvitation.ACCEPTED or invitation["email"] in members_mail:
                all_members.append(
                    {"email": invitation["email"], "status": TeamInvitation.STATUS_DICT[invitation["status"]]}
                )

        ret["all_members"] = all_members

        return ret


class TeamCreateSerializer(TeamSerializer):
    class Meta:
        model = Team
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "owner",
            "members",
            "subdomain",
            "can_delete",
            "team_hosts",
            "is_personal",
        )

    def validate(self, data):
        user = self.context.get("user", None)
        if not user:
            raise serializers.ValidationError("User not found.")
        if not Team.objects.has_create_permission(user):
            raise serializers.ValidationError("User not allowed to create team.")
        return data


class TeamInvitationCreateSerializer(serializers.Serializer):
    MAXIMUM_EMAILS_ALLOWED = 1000

    emails = serializers.ListField(write_only=True)

    def validate(self, data):
        emails = data.get("emails")
        if len(emails) > self.MAXIMUM_EMAILS_ALLOWED:
            raise serializers.ValidationError(
                "Not more than %s email ID's are allowed." % self.MAXIMUM_EMAILS_ALLOWED
            )

        team_pk = self.context.get("team_pk")
        user = self.context.get("user")

        try:
            team = Team.objects.get(pk=team_pk)
        except Team.DoesNotExist:
            raise serializers.ValidationError("Team does not exist.")

        if team.has_invite_permissions(user):
            return data

        raise serializers.ValidationError("Operation not allowed.")


class TeamRemoveMemberSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get("email")
        team_pk = self.context.get("team_pk")
        user = self.context.get("user")

        try:
            team = Team.objects.get(pk=team_pk)
        except Team.DoesNotExist:
            raise serializers.ValidationError("Team does not exist.")

        if team.has_invite_permissions(user):
            if team.owner.email == email:
                raise serializers.ValidationError("You cant remove owner from members list")
            return data

        raise serializers.ValidationError("Operation not allowed.")


class SubDomainURLBuilderSerializer(serializers.Serializer):
    organization = serializers.CharField()
    team = serializers.CharField()
