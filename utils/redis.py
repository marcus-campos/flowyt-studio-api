import redis as red

from flowyt_api.settings import REDIS

redis_workspace = red.Redis(
    host=REDIS["WORKSPACES"]["HOST"],
    port=REDIS["WORKSPACES"]["PORT"],
    password=REDIS["WORKSPACES"]["PASSWORD"],
    db=REDIS["WORKSPACES"]["DB"],
)

redis_plan = red.Redis(
    host=REDIS["PLAN"]["HOST"],
    port=REDIS["PLAN"]["PORT"],
    password=REDIS["PLAN"]["PASSWORD"],
    db=REDIS["PLAN"]["DB"],
)

redis_monitor = red.Redis(
    host=REDIS["MONITOR"]["HOST"],
    port=REDIS["MONITOR"]["PORT"],
    password=REDIS["MONITOR"]["PASSWORD"],
    db=REDIS["MONITOR"]["DB"],
)
