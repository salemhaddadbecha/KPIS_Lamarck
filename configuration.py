import json
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SECRET_FILE_PATH = 'secrets.json'
SECRET_CONFIG_STORE = {}

try:
    with open(SECRET_FILE_PATH) as config:
        SECRET_CONFIG_STORE = json.load(config)
except FileNotFoundError:
    try:
        with open(os.path.join(BASE_DIR, 'secrets.json')) as config:
            SECRET_CONFIG_STORE = json.load(config)
    except Exception:
        raise


class BaseConfig(object):
    APPLICATION_NAME = 'kpis'
    DEBUG = 1
    BASE_DIR = BASE_DIR


class ProductionConfig(BaseConfig):
    ENV = "production"
    DEBUG = 1
    PRIORITY_DEBUG_LEVEL = 10
    MULTI_THREADING = "no"# no | "soft" | "hard"
    BOONDMANAGER_API_URL = SECRET_CONFIG_STORE["boondManager_api_url"]
    BOONDMANAGER_API_LOGIN = SECRET_CONFIG_STORE["boondManager_api_login"]
    BOONDMANAGER_API_PASSWORD = SECRET_CONFIG_STORE["boondManager_api_password"]
    DB_CONN_STR = SECRET_CONFIG_STORE["db_conn_str"]
    CRONJOB_EXECUTION = "jour_precedent" # "test_period" | "jour_precedent"

class LocalConfig(BaseConfig):
    ENV = "local"
    DEBUG = 1
    PRIORITY_DEBUG_LEVEL = 10
    MULTI_THREADING = "no" # no | "soft" | "hard"
    BOONDMANAGER_API_URL = SECRET_CONFIG_STORE["boondManager_api_url"]
    BOONDMANAGER_API_LOGIN = SECRET_CONFIG_STORE["boondManager_api_login"]
    BOONDMANAGER_API_PASSWORD = SECRET_CONFIG_STORE["boondManager_api_password"]
    DB_CONN_STR = f'sqlite:///{os.path.join(BASE_DIR, "database.db")}'
    CRONJOB_EXECUTION = "test_period" # "test_period" | "jour_precedent"

class ConfigurationException(Exception):
    pass


class Configuration(dict):
    def __init__(self, *args, **kwargs):
        if not os.environ.get('ENV'):
            raise ConfigurationException(
                "Please set 'ENV' environment variable"
            )

        super(Configuration, self).__init__(*args, **kwargs)

        self["ENV"] = os.environ['ENV']
        self.__dict__ = self

    def from_object(self, obj):
        for attr in dir(obj):

            if not attr.isupper():
                continue

            self[attr] = getattr(obj, attr)

        self.__dict__ = self


APP_CONFIG = Configuration()

if APP_CONFIG.get('ENV') == 'production':
    APP_CONFIG.from_object(ProductionConfig)
elif APP_CONFIG.get('ENV') == 'local':
    APP_CONFIG.from_object(LocalConfig)
else:
    APP_CONFIG.from_object(ConfigurationException)
