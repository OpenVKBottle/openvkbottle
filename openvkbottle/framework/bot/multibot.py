from collections.abc import Iterable
from typing import TYPE_CHECKING, Type

from openvkbottle.http import SingleAiohttpClient
from openvkbottle.modules import logger
from openvkbottle.polling import BotPolling
from openvkbottle.tools._runner import run as _run

if TYPE_CHECKING:
    from openvkbottle.api import ABCAPI
    from openvkbottle.polling import ABCPolling

    from .bot import Bot


def run_multibot(
    bot: "Bot",
    apis: Iterable["ABCAPI"],
    polling_type: Type["ABCPolling"] = BotPolling,
):
    """Add run_polling with polling constructed from derived apis
    :param bot: Bot main instance (api is not required)
    :param apis: Iterable of apis
    :param polling_type: polling type to be ran
    """

    tasks = []
    for i, api_instance in enumerate(apis):
        logger.debug("Connecting API (index: {})", i)
        polling = polling_type().construct(api_instance, bot.error_handler)
        if isinstance(polling, BotPolling):
            polling.skip_old_events = bot.skip_old_events
        api_instance.http_client = SingleAiohttpClient()
        tasks.append(bot.run_polling(custom_polling=polling))

    _run(
        *bot.startup_tasks,
        *tasks,
        on_startup=bot.on_startup,
        on_shutdown=bot.on_shutdown,
    )
