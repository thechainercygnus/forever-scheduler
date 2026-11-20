"""Settings, read from the environment or `.env`."""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # The bot's token, from the Discord developer portal. Never log or print it.
    discord_token: SecretStr

    # Servers to register commands in straight away while developing, as a JSON list
    # (`[123, 456]`). Left empty, commands are global, which Discord can take a while to
    # show.
    dev_guild_ids: list[int] = []

    # The Character Planner's address and integration token (character-planner#265).
    # Unused until that API exists.
    planner_url: str | None = None
    planner_token: SecretStr | None = None
