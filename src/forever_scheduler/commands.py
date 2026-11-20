"""Slash commands. Each feature adds its own plugin; this one holds the basics."""

import math

import arc

plugin = arc.GatewayPlugin("core")


def latency_reply(heartbeat_latency: float) -> str:
    """The `/ping` answer. Before the first heartbeat, hikari reports NaN."""
    if math.isnan(heartbeat_latency):
        return "Pong! (no heartbeat yet)"
    return f"Pong! {heartbeat_latency * 1000:.0f} ms"


@plugin.include
@arc.slash_command("ping", "Check that the bot is up.")
async def ping(ctx: arc.GatewayContext) -> None:
    await ctx.respond(latency_reply(ctx.client.app.heartbeat_latency))
