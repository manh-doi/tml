import os

from tml.utils.configuration import app_name, ApplicationConfigParser, get_config

if f"{app_name.upper()}_HOME" in os.environ:
    APP_HOME = os.getenv(f"{app_name.upper()}_HOME")
else:
    APP_HOME = None

config = ApplicationConfigParser()
config.read(get_config(APP_HOME))
