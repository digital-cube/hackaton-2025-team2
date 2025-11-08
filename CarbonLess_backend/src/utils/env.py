from dotenv import find_dotenv, load_dotenv
import os

try:
    env_path = find_dotenv()
    load_dotenv(env_path)
except Exception as e:
    raise RuntimeError(f"Failed to load env + {e}")


class EnvNotSetError(Exception):
    pass


class EnvMeta(type):
    def __getattribute__(cls, name):
        value = super().__getattribute__(name)

        if name.isupper() and not name.startswith("_"):
            prefix = ""
            if hasattr(cls, "Config") and hasattr(cls.Config, "prefix"):
                prefix = cls.Config.prefix

            env_var_name = f"{prefix}{name}"

            value = os.getenv(env_var_name)
            if value is None or value == "":
                raise EnvNotSetError(f"Environment variable '{name}' is not set or loaded")

        return value


class BaseEnv(metaclass=EnvMeta):
    pass

# ----------------------------------------------------------------------------------------------------------------------------------------------------- database
class DB(BaseEnv):
    USERNAME: str = None
    PASSWORD: str = None
    NAME: str = None
    HOST: str = None
    PORT: str = None

    class Config:
        prefix = "DB_"

class ENV(BaseEnv):
    JWT_SECRET: str = None

    class Config:
        prefix = "ENV_"