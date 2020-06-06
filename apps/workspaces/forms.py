from django.forms import ModelForm, TextInput
from django_ace import AceWidget

from apps.workspaces.models import (Environment, Flow, FunctionFile,
                                    Integration, IntegrationList, Monitor,
                                    Workspace)


class WorkspaceAdminForm(ModelForm):
    class Meta:
        model = Workspace
        fields = "__all__"
        widgets = {
            "workspace_color": TextInput(attrs={"type": "color"}),
        }


class EnvironmentAdminForm(ModelForm):
    class Meta:
        model = Environment
        fields = "__all__"
        widgets = {
            "environment_variables": AceWidget(
                mode="json",
                theme="twilight",
                width="900px",
                height="500px",
                wordwrap=False,
                showprintmargin=False,
            )
        }


class IntegrationAdminForm(ModelForm):
    class Meta:
        model = Integration
        fields = "__all__"
        widgets = {
            "integration_variables": AceWidget(
                mode="json",
                theme="twilight",
                width="900px",
                height="500px",
                wordwrap=False,
                showprintmargin=False,
            )
        }


class MonitorAdminForm(ModelForm):
    class Meta:
        model = Monitor
        fields = "__all__"
        widgets = {
            "monitor_variables": AceWidget(
                mode="json",
                theme="twilight",
                width="900px",
                height="500px",
                wordwrap=False,
                showprintmargin=False,
            )
        }


class IntegrationListAdminForm(ModelForm):
    class Meta:
        model = IntegrationList
        fields = "__all__"
        widgets = {
            "integration_variables": AceWidget(
                mode="json",
                theme="twilight",
                width="900px",
                height="500px",
                wordwrap=False,
                showprintmargin=False,
            )
        }


class FunctionFileAdminForm(ModelForm):
    class Meta:
        model = FunctionFile
        fields = "__all__"
        widgets = {
            "function_data": AceWidget(
                mode="python",
                theme="twilight",
                width="900px",
                height="500px",
                wordwrap=False,
                showprintmargin=False,
            )
        }


class FlowAdminForm(ModelForm):
    class Meta:
        model = Flow
        fields = "__all__"
        widgets = {
            "flow_layout": AceWidget(
                mode="json",
                theme="twilight",
                width="900px",
                height="500px",
                wordwrap=False,
                showprintmargin=False,
            ),
            "flow_data": AceWidget(
                mode="json",
                theme="twilight",
                width="900px",
                height="500px",
                wordwrap=False,
                showprintmargin=False,
            ),
        }
