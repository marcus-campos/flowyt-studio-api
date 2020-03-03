from django.forms import ModelForm, TextInput

from apps.workspaces.models import Workspace


class WorkspaceAdminForm(ModelForm):
    class Meta:
        model = Workspace
        fields = "__all__"
        widgets = {
            "workspace_color": TextInput(attrs={"type": "color"}),
        }
