from fernet_fields import EncryptedField

from django.contrib.postgres.fields import JSONField


class CustomJSONField(JSONField):
    def db_type(self, connection):
        return 'text'


class JSONEncryptedField(EncryptedField, CustomJSONField):
    pass
