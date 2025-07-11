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
    salt: str


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env()

    return Config(
        db=DataBaseConfig(database_url=env.str("DATABASE_URL")),
        secret_key=env.str("SECRET_KEY"),
        debug=env.bool("DEBUG", default=False),
        salt=env.str("SALT"),
    )


config = load_config()

fake_db = [
    {"user_id": "b6b8770e-2afd-4630-a777-fbe11de97baa", "username": "PP", "password": "12345", "session_token": None},
    {"user_id": "8ba44281-fa9f-43e9-b733-a370c0a0f100", "username": "QAA", "password": "25765", "session_token": None},
]
