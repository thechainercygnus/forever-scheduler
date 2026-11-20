"""The bot: a hikari gateway bot with an arc command client."""

import arc
import hikari

from forever_scheduler import commands
from forever_scheduler.config import Settings


def build(settings: Settings) -> tuple[hikari.GatewayBot, arc.GatewayClient]:
    """The bot and its command client, ready to run. Nothing connects until `bot.run()`."""
    bot = hikari.GatewayBot(
        settings.discord_token.get_secret_value(),
        intents=hikari.Intents.GUILDS,
        banner=None,
    )
    guilds = settings.dev_guild_ids or hikari.UNDEFINED
    client = arc.GatewayClient(bot, default_enabled_guilds=guilds)
    client.add_plugin(commands.plugin)
    return bot, client


def main() -> None:
    bot, _ = build(Settings())  # pyright: ignore[reportCallIssue]  # the token comes from the environment
    bot.run()
