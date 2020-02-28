import copy


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

        flow_nodes = flow_data["nodes"]
        flow_links = flow_data["links"]
        flow_nodes_aux = copy.deepcopy(flow_nodes)

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
            for k, val in flow_links.items():
                if val["from"]["nodeId"] == node_id:
                    _links.append(val["to"]["nodeId"])
                    del _aux_flow_links[k]
            flow_links = _aux_flow_links

            # Add links to model
            if _model["action"] in ["request", "validation"]:
                if len(_links) < 2:
                    return False

                _model["data"]["next_action_success"] = _links[0]
                _model["data"]["next_action_fail"] = _links[1]
                _model["next_action"] = "${pipeline.next_action}"

            if _model["action"] in ["if", "switch"]:
                for key, value in _model["data"]["conditions"].items():
                    _model["data"]["conditions"][key]["next_action"] = _links[key]
                _model["data"]["next_action_else"] = _links[len(_links)]

            if _model["action"] in ["response", "jump"]:
                _model["next_action"] = None

            flow["pipeline"].append(_model)

        return flow
