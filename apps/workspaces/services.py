import copy
import io
import json
import os
import shutil
from operator import itemgetter

from django.utils.text import slugify

from apps.workspaces.actions import ACTIONS
from flowyt_api.settings import BASE_DIR, WORKSPACE_PUBLISH_MODE
from utils.zipdir import zipdir


class ReleaseBuilder:
    def make(self, validated_data, release, workspace, flows, routes, integrations, function_files):
        projects_to_publish = self._load_projects(
            validated_data, release, workspace, flows, routes, integrations, function_files
        )

        if WORKSPACE_PUBLISH_MODE == "upload":
            return self._create_and_zip(projects_to_publish)

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
            projects_to_publish.append(
                {"name": slug, "subdomain": workspace.release.workspace.team.subdomain, "data": project}
            )

        return projects_to_publish

    def _settings(self, project, release, workspace, environment, integrations):
        config_settings = ConfigTranslation().settings_translate(
            release, workspace, environment, integrations
        )

        project["config"].append(
            {
                "name": "settings",
                "data": json.dumps(config_settings, ensure_ascii=False),
            }
        )

        return project

    def _flows(self, project, flows):
        flows_list = []
        for flow in flows:
            slug = slugify(flow.name)
            translated_flow = FlowTranslation().translate(flow)

            flows_list.append(
                {
                    "name": slug,
                    "data": json.dumps(translated_flow, ensure_ascii=False),
                }
            )

        project["flows"] = flows_list

        return project

    def _routes(self, project, routes):
        for route in routes:
            project["routes"].append(
                {
                    "path": route.path,
                    "method": route.method,
                    "flow": slugify(route.flow_release.name),
                }
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

            zipfile = io.open("{0}.zip".format(project_folder), "rb")
            projects_zips.append({"name": project["name"], "file": zipfile})

        return {"projects_zips": projects_zips, "projects": projects}

    def _create_project_file(self, project, project_folder, key, extension):
        if key == "routes":
            file = io.open("{0}/{1}.{2}".format(project_folder, key, extension), "w+", encoding="utf8")
            file.write(json.dumps(project["data"]["routes"], ensure_ascii=False))
            file.close()
            return

        if os.path.exists(project_folder + "/{0}".format(key)):
            shutil.rmtree(project_folder + "/{0}".format(key))
        os.makedirs(project_folder + "/{0}".format(key))

        for item in project["data"][key]:
            file = open(
                "{0}/{1}/{2}.{3}".format(project_folder, key, item["name"], extension), "w+", encoding="utf8"
            )
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

        safe_mode = environment.environment.safe_mode if environment.environment.safe_mode else "{}"
        environment_variables = (
            environment.environment.environment_variables
            if environment.environment.environment_variables
            else "{}"
        )

        settings["id"] = str(workspace.id)
        settings["name"] = workspace.name
        settings["debug"] = environment.environment.debug
        settings["safe_mode"] = json.loads(safe_mode)
        settings["development_language"] = workspace.language.language if workspace.language else "python"
        settings["release"]["id"] = str(release.id)
        settings["release"]["name"] = release.name
        settings["env"] = json.loads(environment_variables)

        for integration in integrations:
            settings["integrations"][
                integration.integration.integration_list.integration_key
            ] = integration.integration_variables

        return settings


class FlowTranslation:
    flow_model = {"id": "", "name": "", "pipeline": []}

    def translate(self, flow_queryset):
        flow_data = flow_queryset.flow_layout if flow_queryset.flow_layout else {}
        flow_node_data = flow_queryset.flow_data if flow_queryset.flow_data else {}

        flow = copy.deepcopy(self.flow_model)
        flow["id"] = str(flow_queryset.id)
        flow["name"] = flow_queryset.name

        flow_nodes = flow_data["nodes"] if flow_data else {}
        flow_links = flow_data["links"] if flow_data else {}

        for key, value in flow_nodes.items():
            node_id = key

            # Get data
            action_data = self._get_data(node_id, flow_node_data)

            # Get action
            action_name = value["properties"]["name"]
            action = ACTIONS[action_name](action_data)
            action.id = node_id

            # Get links
            flow_links, links = self._get_links(node_id, flow_links)

            # Add links to action
            flow = self._set_links(action, flow, links)

        return flow

    def _get_data(self, node_id, flow_node_data):
        data = {}
        for index in range(len(flow_node_data)):
            if flow_node_data[index]["id"] == node_id:
                for key, value in flow_node_data[index]["data"].items():
                    try:
                        data[key] = json.loads(flow_node_data[index]["data"][key])
                    except:
                        data[key] = flow_node_data[index]["data"][key]

                del flow_node_data[index]
                break

        return data

    def _get_links(self, node_id, flow_links):
        links = []
        aux_flow_links = copy.deepcopy(flow_links)

        for key, value in flow_links.items():
            if value["from"]["nodeId"] == node_id:
                links.append({"node_id": value["to"]["nodeId"], "port_id": value["from"]["portId"]})
                del aux_flow_links[key]
        flow_links = aux_flow_links
        links = sorted(links, key=itemgetter("port_id"))

        return flow_links, links

    def _set_links(self, action, flow, links):
        if not links:
            action.next_action = None
            flow["pipeline"].append(action.__dict__)
            return flow

        if action.action in ["request", "validation"]:
            if len(links) < 2:
                raise "Action {0} needs at least 2 links".format(action.action)

            action.data["next_action_success"] = links[0]["node_id"]
            action.data["next_action_fail"] = links[1]["node_id"]
            action.next_action = "${pipeline.next_action}"

        elif action.action in ["if", "switch"]:
            if len(links) < 2:
                raise "Action {0} needs at least 2 links".format(action.action)

            for key, value in enumerate(action.data["conditions"]):
                action.data["conditions"][key]["next_action"] = links[key]["node_id"]
            action.data["next_action_else"] = links[(len(links) - 1)]["node_id"]
            action.next_action = "${pipeline.next_action}"

        elif action.action in ["response", "jump"]:
            action.next_action = None

        else:
            action.next_action = links[0]["node_id"]

        flow["pipeline"].append(action.__dict__)

        return flow
