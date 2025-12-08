from pathlib import Path

from dynaconf import Dynaconf

# Get the directory where this config file is located
_config_dir = Path(__file__).parent

configs = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[
        str(_config_dir / "settings.toml"),
        str(_config_dir / ".secrets.toml"),
    ],
    environments=True,
    load_dotenv=True,
    env_switcher="ENV_FOR_DYNACONF",
    merge_enabled=True,
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
