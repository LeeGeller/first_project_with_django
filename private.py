import json

from django.core.exceptions import ImproperlyConfigured


class PrivateConfig(object):
    def __init__(self, path):
        self._path = path
        self._check_path()
        self._config = None
        self._read()

    def _check_path(self):
        pass

    def _read(self):
        try:
            with open(self._path) as f:
                self._config = json.loads(f.read())
        except FileNotFoundError:
            raise ImproperlyConfigured(
                "Error opening private config file at '{}'".format(self._path)
            )

    def get(self, key, subkey=None):
        try:
            if subkey is not None:
                return self._config[key][subkey]
            else:
                return self._config[key]
        except KeyError:
            error_msg = "Private JSON-file has not key '{0}'".format(key)
            raise ImproperlyConfigured(error_msg)
