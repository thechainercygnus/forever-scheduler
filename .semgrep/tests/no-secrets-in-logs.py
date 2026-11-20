# Test cases for .semgrep/rules/no-secrets-in-logs.yaml, run with
#   uvx --from semgrep semgrep --test --config .semgrep/rules .semgrep/tests
# "ruleid" marks a line the rule must flag; "ok" one it must not.
# ruff: noqa
# pyright: basic
import logging

logger = logging.getLogger(__name__)


async def leaks(settings, ctx, rest, channel):
    token = settings.discord_token.get_secret_value()
    # ruleid: no-secrets-in-logs
    logger.info("token %s", token)

    # ruleid: no-secrets-in-logs
    logging.warning(f"Bearer {settings.planner_token.get_secret_value()}")

    # ruleid: no-secrets-in-logs
    print(token)

    headers = {"Authorization": f"Bearer {settings.planner_token.get_secret_value()}"}
    # ruleid: no-secrets-in-logs
    logger.error("request headers: %s", headers)

    # ruleid: no-secrets-in-logs
    await ctx.respond(f"my token is {token}")

    # ruleid: no-secrets-in-logs
    await rest.create_message(123, token)

    # ruleid: no-secrets-in-logs
    await channel.send(headers)

    # ruleid: no-secrets-in-logs
    raise ValueError(f"refused token {token}")


async def facts_about_secrets(settings, ctx, client):
    token = settings.discord_token.get_secret_value()
    # ok: no-secrets-in-logs
    logger.debug("bot token is configured: %s", bool(token))

    # ok: no-secrets-in-logs
    logger.info("token length %d", len(token))

    # The settings object hides its secrets in its repr.
    # ok: no-secrets-in-logs
    logger.info("settings: %s", settings)

    planner = settings.planner_token.get_secret_value()
    answer = await client.get("/api/integrations/v1/me", headers={"Authorization": planner})
    # The status of a request that sent a token is a number, not the token.
    # ok: no-secrets-in-logs
    logger.warning("planner answered %s", answer.status_code)

    # The answer itself can still echo what was sent.
    # ruleid: no-secrets-in-logs
    logger.warning("planner answered %s", answer)

    # ok: no-secrets-in-logs
    await ctx.respond("Pong!")

    # ok: no-secrets-in-logs
    raise ValueError("Discord refused the bot token: check DISCORD_TOKEN")
