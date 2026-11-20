import math
from types import SimpleNamespace
from unittest.mock import AsyncMock

import hikari
import pytest

from forever_scheduler import commands
from forever_scheduler.bot import build
from forever_scheduler.config import Settings

FAKE_TOKEN = "MTIzNDU2Nzg5.fake.token"


def settings(**overrides: object) -> Settings:
    # _env_file=None: tests never read .env. hikari reads the application id from a token's
    # first part (base64 of "123456789"), so the fake has a token's shape.
    return Settings(_env_file=None, discord_token=FAKE_TOKEN, **overrides)  # pyright: ignore[reportCallIssue, reportArgumentType]


@pytest.mark.parametrize(
    ("latency", "reply"),
    [(0.0423, "Pong! 42 ms"), (math.nan, "Pong! (no heartbeat yet)")],
)
def test_latency_reply(latency: float, reply: str) -> None:
    assert commands.latency_reply(latency) == reply


async def test_ping_responds_with_latency() -> None:
    ctx = SimpleNamespace(
        respond=AsyncMock(),
        client=SimpleNamespace(app=SimpleNamespace(heartbeat_latency=0.1)),
    )
    await commands.ping.callback(ctx)  # pyright: ignore[reportArgumentType]
    ctx.respond.assert_awaited_once_with("Pong! 100 ms")


def test_build_registers_commands_without_connecting() -> None:
    bot, client = build(settings())
    assert isinstance(bot, hikari.GatewayBot)
    assert not bot.is_alive
    names = {c.name for c in client.walk_commands(hikari.CommandType.SLASH)}
    assert names == {"ping"}


def test_dev_guild_ids_parse_from_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEV_GUILD_IDS", "[123, 456]")
    assert settings().dev_guild_ids == [123, 456]


def test_token_is_hidden_in_repr() -> None:
    assert FAKE_TOKEN not in repr(settings())
