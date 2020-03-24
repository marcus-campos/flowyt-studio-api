import redis as red
from orchestryzi_api.settings import REDIS

redis = red.Redis(host=REDIS["HOST"], port=REDIS["PORT"], password=REDIS["PASSWORD"], db=REDIS["DB"])
