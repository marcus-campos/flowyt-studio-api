class BaseAction():
    id = "",
    action = ""
    data = {}
    next_action = ""

class Start(BaseAction):
    def __init__(self, data):
        self.action = "start"
        self.data = data

class Action(BaseAction):
    def __init__(self, data):
        self.action = "action"
        self.data = data

class FlowVar(BaseAction):
    def __init__(self, data):
        self.data = data

class WorkspaceVar(BaseAction):
    def __init__(self, data):
        self.action = "workspace_var"
        self.data = data

class Request(BaseAction):
    def __init__(self, data):
        self.action = "request"
        self.data = {
            "url": data.get("url", ""),
            "method": data.get("method", "get"),
            "headers": data.get("headers", {}) if type(data.get("headers", {})) is dict else {},
            "data": data.get("data", {}) if type(data.get("data", {})) is dict else {},
            "next_action_success": data.get("next_action_success", ""),
            "next_action_fail": data.get("next_action_fail", "")
        }

class Response(BaseAction):
    def __init__(self, data):
        self.action = "response"
        self.data = {
            "status": int(data.get("status", 200)),
            "headers": data.get("headers", {}) if type(data.get("headers", {})) is dict else {},
            "data": data.get("data", {}) if type(data.get("data", {})) is dict else {}
        }

class Jump(BaseAction):
    def __init__(self, data):
        self.action = "jump"
        self.data = {
            "next_flow": data.get("next_flow", "")
        }

class Switch(BaseAction):
    def __init__(self, data):
        self.action = "switch"
        self.data = {
            "conditions": data.get("conditions", {}) if type(data.get("conditions", {})) is dict else {},
            "next_action_else": data.get("next_action_else", "")
        }

class If(Switch):
    pass

class Validation(BaseAction):
    def __init__(self, data):
        self.action = "validation"
        self.data = {
            "schema": data.get("schema", {}) if type(data.get("schema", {})) is dict else {},
            "next_action_success": data.get("next_action_success", ""),
            "next_action_fail": data.get("next_action_fail", "")
        }

class SqlDatabase(BaseAction):
    def __init__(self, data):
        self.action = "sql_db"
        self.data = {
            "sql": data.get("sql", "")
        }

class Loop(BaseAction):
    def __init__(self, data):
        self.action = "loop"
        self.data = {
            "type": data.get("type", "range"),
            "data": data.get("data", "1"),
            "action": data.get("action", "${}")
        }

ACTIONS = {
    "start": Start,
    "flow_var": FlowVar,
    "workspace_var": WorkspaceVar,
    "request": Request,
    "switch": Switch,
    "if": If,
    "response": Response,
    "validation": Validation,
    "jump": Jump,
    "sql_db": SqlDatabase,
    "loop": Loop,
    "action": Action,
}