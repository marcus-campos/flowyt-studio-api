import json

from django.contrib.postgres.fields import JSONField

from .cryptography import Cryptography


class CustomJSONField(JSONField):
    def db_type(self, connection):
        return "text"


class JSONEncryptedField(CustomJSONField):
    def get_db_prep_save(self, value, connection):
        value = Cryptography().encrypt(json.dumps(value))
        return value

    def from_db_value(self, value, expression, connection, *args):
        parsed_json = ""

        if value:
            value = Cryptography().decrypt(value)

            try:
                parsed_json = json.loads(value)
            except:
                parsed_json = value

        return parsed_json
