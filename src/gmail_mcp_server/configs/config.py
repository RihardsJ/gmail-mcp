from pathlib import Path

from dynaconf import Dynaconf

# Get the directory where this config file is located
_config_dir = Path(__file__).parent
_base_dir = Path(__file__).parent.parent.parent.parent

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

configs.client_secrets_file = _base_dir / "credentials" / "client_secrets.json"
configs.token_file = _base_dir / "credentials" / "token.json"

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
