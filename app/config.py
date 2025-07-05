from dataclasses import dataclass

from environs import Env


@dataclass
class DataBaseConfig:
    database_url: str


@dataclass
class Config:
    db: DataBaseConfig
    secret_key: str
    debug: bool


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env()

    return Config(
        db=DataBaseConfig(database_url=env.str("DATABASE_URL")),
        secret_key=env.str("SECRET_KEY"),
        debug=env.bool("DEBUG", default=False),
    )
