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
    APPLICATION_NAME = 'kpi'
    DEBUG = 1
    BASE_DIR = BASE_DIR


class ProductionConfig(BaseConfig):
    ENV = "production"
    DEBUG = 1
    PRIORITY_DEBUG_LEVEL = 30
    MULTI_THREADING = "no" # no | "soft" | "hard"
    BOONDMANAGER_API_URL = SECRET_CONFIG_STORE["boondManager_api_url"]
    BOONDMANAGER_API_LOGIN = SECRET_CONFIG_STORE["boondManager_api_login"]
    BOONDMANAGER_API_PASSWORD = SECRET_CONFIG_STORE["boondManager_api_password"]
    DB_CONN_STR = SECRET_CONFIG_STORE["db_conn_str"]
    CRONJOB_EXECUTION = SECRET_CONFIG_STORE["cron_execution"]

class LocalConfig(BaseConfig):
    ENV = "local"
    DEBUG = 0
    PRIORITY_DEBUG_LEVEL = 100
    MULTI_THREADING = "no" # no | "soft" | "hard"
    BOONDMANAGER_API_URL = SECRET_CONFIG_STORE["boondManager_api_url"]
    BOONDMANAGER_API_LOGIN = SECRET_CONFIG_STORE["boondManager_api_login"]
    BOONDMANAGER_API_PASSWORD = SECRET_CONFIG_STORE["boondManager_api_password"]
    DB_CONN_STR = f'sqlite:///{os.path.join(BASE_DIR, "database.db")}'
    CRONJOB_EXECUTION = SECRET_CONFIG_STORE["cron_execution"]

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
