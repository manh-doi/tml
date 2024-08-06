import os
from configparser import ConfigParser

app_name = "tml"


def get_config(app_home=None):
    if app_home:
        return os.path.join(app_home, f"{app_name}.cfg")
    return os.path.join("./", f"{app_name}.cfg")


def overwrite_by_env_vars(func):
    def wrap_func(obj, filenames, **kwargs):
        def update_dict(d, ds):
            d.update(ds)
            return d

        def get_env_var(section, key):
            try:
                env_var_name = env_var_pattern.format(S=section, K=key).upper()
                return env_vars[env_var_name]
            except KeyError:
                return None

        def update_conf(config, s, k, v):
            config[s][k] = v
            return config

        from functools import reduce
        env_var_pattern = app_name.upper() + "__{S}__{K}"
        env_vars = reduce(lambda r, y: update_dict(r, y),
                          map(lambda k: {k: os.environ[k]},
                              filter(lambda x: x.startswith(app_name.upper()), os.environ.keys())),
                          {})

        func(obj, filenames, **kwargs)
        section_keys = [(section, key) for section in obj.sections() for key in obj[section]]
        updated_keys = filter(lambda x: x is not None,
                              map(lambda sk: (*sk, get_env_var(*sk)) if get_env_var(*sk) else None, section_keys))
        reduce(lambda r, uk: update_conf(r, *uk), updated_keys, obj)

    return wrap_func


class ApplicationConfigParser(ConfigParser):
    @overwrite_by_env_vars
    def read(self, filenames, **kwargs):
        super(ApplicationConfigParser, self).read(filenames, **kwargs)
