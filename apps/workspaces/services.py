import copy
import json
import os
import shutil

from django.utils.text import slugify
from orchestryzi_api.settings import BASE_DIR
from utils.zipdir import zipdir


class ReleaseBuilder:
    def make(self, validated_data, release, workspace, flows, routes, integrations, function_files):
        projects_to_publish = self._load_projects(
            validated_data, release, workspace, flows, routes, integrations, function_files
        )
        projects_to_publish = self._create_and_zip(projects_to_publish)
        return projects_to_publish

    def _load_projects(self, validated_data, release, workspace, flows, routes, integrations, function_files):
        environments_to_publish = validated_data["environments"]

        project_structure = {"config": [], "flows": [], "functions": [], "routes": []}
        projects_to_publish = []

        for environment in environments_to_publish:
            project = copy.deepcopy(project_structure)

            # Config
            project = self._settings(project, release, workspace, environment, integrations)
            # Flows and Routes
            project = self._flows(project, flows)
            # Routes
            project = self._routes(project, routes)
            # Functions
            project = self._functions(project, function_files)

            # Add project to list
            slug = slugify("{0}-{1}".format(workspace.name, environment.name))
            projects_to_publish.append({"name": slug, "data": project})

        return projects_to_publish

    def _settings(self, project, release, workspace, environment, integrations):
        config_settings = ConfigTranslation().settings_translate(
            release, workspace, environment, integrations
        )

        project["config"].append(
            {"name": "settings", "data": json.dumps(config_settings),}
        )

        return project

    def _flows(self, project, flows):
        flows_list = []
        for flow in flows:
            slug = slugify(flow.name)
            translated_flow = FlowTranslation().translate(flow)

            flows_list.append(
                {"name": slug, "data": json.dumps(translated_flow),}
            )

        project["flows"] = flows_list

        return project

    def _routes(self, project, routes):
        for route in routes:
            project["routes"].append(
                {"path": route.path, "method": route.method, "flow": slugify(route.flow_release.name),}
            )

        return project

    def _functions(self, project, function_files):
        for function in function_files:
            project["functions"].append({"name": function.name.lower(), "data": function.function_data})

        return project

    def _create_and_zip(self, projects):
        projects_zips = []

        for index, project in enumerate(projects):
            WORKSPACE_DIR = BASE_DIR + "/storage/tmp/workspaces/"
            project_folder = WORKSPACE_DIR + project["name"]

            self._create_project_file(project, project_folder, "config", "json")
            self._create_project_file(project, project_folder, "flows", "json")
            self._create_project_file(project, project_folder, "functions", "py")
            self._create_project_file(project, project_folder, "routes", "json")

            # Zip
            zipdir("{0}".format(project_folder))

            projects[index]["project_folder"] = project_folder

            zipfile = open("{0}.zip".format(project_folder), "rb")
            projects_zips.append({"name": project["name"], "file": zipfile})

        return {"projects_zips": projects_zips, "projects": projects}

    def _create_project_file(self, project, project_folder, key, extension):
        if key == "routes":
            file = open("{0}/{1}.{2}".format(project_folder, key, extension), "w+")
            file.write(json.dumps(project["data"]["routes"]))
            file.close()
            return

        if os.path.exists(project_folder + "/{0}".format(key)):
            shutil.rmtree(project_folder + "/{0}".format(key))
        os.makedirs(project_folder + "/{0}".format(key))

        for item in project["data"][key]:
            file = open("{0}/{1}/{2}.{3}".format(project_folder, key, item["name"], extension), "w+",)
            file.write(item["data"])
            file.close()


class ConfigTranslation:
    settings_model = {
        "id": "",
        "name": "",
        "debug": True,
        "release": {"id": "", "name": ""},
        "integrations": {},
        "env": {},
    }

    def settings_translate(self, release, workspace, environment, integrations):
        settings = copy.deepcopy(self.settings_model)

        settings["id"] = str(workspace.id)
        settings["name"] = workspace.name
        settings["debug"] = True
        settings["release"]["id"] = str(release.id)
        settings["release"]["name"] = release.name
        settings["env"] = environment.environment_variables

        for integration in integrations:
            settings["integrations"][integration.name] = integration.integration_variables

        return settings


class FlowTranslation:
    flow_model = {"id": "", "name": "", "pipeline": []}
    action_model = {"id": "", "action": "", "data": {}, "next_action": ""}

    def translate(self, flow_queryset):
        flow_data = flow_queryset.flow_layout
        flow_node_data = flow_queryset.flow_data

        flow = copy.deepcopy(self.flow_model)
        flow["id"] = str(flow_queryset.id)
        flow["name"] = flow_queryset.name

        flow_nodes = flow_data["nodes"] if flow_data else {}
        flow_links = flow_data["links"] if flow_data else {}

        for key, value in flow_nodes.items():
            node_id = key

            _model = copy.deepcopy(self.action_model)
            _model["id"] = node_id
            _model["action"] = value["properties"]["name"]

            # Get data
            for index in range(len(flow_node_data)):
                if flow_node_data[index]["id"] == node_id:
                    _model["data"] = flow_node_data[index]["data"]
                    del flow_node_data[index]
                    break

            # Get links
            _links = []
            _aux_flow_links = copy.deepcopy(flow_links)
            for key, value in flow_links.items():
                if value["from"]["nodeId"] == node_id:
                    _links.append(value["to"]["nodeId"])
                    del _aux_flow_links[key]
            flow_links = _aux_flow_links

            # Add links to model
            if _model["action"] in ["request", "validation"]:
                if len(_links) < 2:
                    return False
                _model["data"]["next_action_success"] = _links[0]
                _model["data"]["next_action_fail"] = _links[1]
                _model["next_action"] = "${pipeline.next_action}"
            elif _model["action"] in ["if", "switch"]:
                for key, value in _model["data"]["conditions"].items():
                    _model["data"]["conditions"][key]["next_action"] = _links[key]
                _model["data"]["next_action_else"] = _links[len(_links)]
            elif _model["action"] in ["response", "jump"]:
                _model["next_action"] = None
            else:
                _model["next_action"] = _links[0]

            flow["pipeline"].append(_model)

        return flow
