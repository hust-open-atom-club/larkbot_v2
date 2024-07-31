from functools import lru_cache

from pydantic_settings import BaseSettings


@lru_cache()
def get_seetings():
    return Settings()


class Settings(BaseSettings):
    feed_url: str = ""
    lark_template_id: str = "AAq0zlsxIx1wz"
    lark_webhook_url: str = ""
    lark_webhook_secret: str = ""

    class Config:
        env_file = ".env"


settings = get_seetings()
