import warnings
from typing import TYPE_CHECKING, Any

from openvkbottle.api import API
from openvkbottle.callback import BotCallback
from openvkbottle.dispatch import BuiltinStateDispenser, Router
from openvkbottle.exception_factory import ErrorHandler
from openvkbottle.framework.base import BaseFramework
from openvkbottle.framework.labeler import BotLabeler
from openvkbottle.modules import logger
from openvkbottle.polling import BotPolling
from openvkbottle.tools.event_deduplicator.memory import MemoryEventDeduplicator

if TYPE_CHECKING:
    from openvkbottle.api import ABCAPI, Token
    from openvkbottle.callback import ABCCallback
    from openvkbottle.dispatch import ABCRouter, ABCStateDispenser
    from openvkbottle.exception_factory import ABCErrorHandler
    from openvkbottle.framework.labeler import ABCLabeler
    from openvkbottle.polling import ABCPolling
    from openvkbottle.tools import ABCEventDeduplicator, LoopWrapper


class Bot(BaseFramework):
    labeler: "ABCLabeler"
    error_handler: "ABCErrorHandler"
    state_dispenser: "ABCStateDispenser"
    event_deduplicator: "ABCEventDeduplicator | None"
    on_startup: list[Any]
    on_shutdown: list[Any]
    startup_tasks: list[Any]
    _loop_wrapper: "LoopWrapper | None"

    def __init__(
        self,
        token: "Token | None" = None,
        api: "ABCAPI | None" = None,
        polling: "ABCPolling | None" = None,
        callback: "ABCCallback | None" = None,
        loop_wrapper: "LoopWrapper | None" = None,
        router: "ABCRouter | None" = None,
        labeler: "ABCLabeler | None" = None,
        state_dispenser: "ABCStateDispenser | None" = None,
        error_handler: "ABCErrorHandler | None" = None,
        task_each_event: Any = None,
        skip_old_events: bool = True,
        *,
        dual_mode: bool = False,
        event_deduplicator: "ABCEventDeduplicator | None" = None,
    ) -> None:
        self.api: API = api or API(token)  # type: ignore
        self.error_handler = error_handler or ErrorHandler()
        self._loop_wrapper = loop_wrapper
        self.on_startup = []
        self.on_shutdown = []
        self.startup_tasks = []
        self.labeler = labeler or BotLabeler(error_handler=error_handler)
        self.state_dispenser = state_dispenser or BuiltinStateDispenser()
        self.skip_old_events = skip_old_events
        self.dual_mode = dual_mode
        self.event_deduplicator = (
            event_deduplicator
            if event_deduplicator is not None
            else MemoryEventDeduplicator()
            if dual_mode is True
            else None
        )

        if polling is not None and isinstance(polling, BotPolling):
            polling.skip_old_events = skip_old_events

        self._polling = polling or BotPolling(
            self.api,
            error_handler=error_handler,
            skip_old_events=skip_old_events,
        )
        self._callback = callback or BotCallback(error_handler=error_handler)
        self._router = router or Router()

        if task_each_event is not None:
            logger.warning("task_each_event is deprecated and will be removed in future versions")

    @property
    def loop_wrapper(self) -> "LoopWrapper":
        if self._loop_wrapper is None:
            from openvkbottle.tools.loop_wrapper import _DEPRECATION_MESSAGE, LoopWrapper

            warnings.warn(_DEPRECATION_MESSAGE, DeprecationWarning, stacklevel=2)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                self._loop_wrapper = LoopWrapper()

        return self._loop_wrapper

    @loop_wrapper.setter
    def loop_wrapper(self, value: "LoopWrapper") -> None:
        self._loop_wrapper = value

    @property
    def callback(self) -> "ABCCallback":
        if self._callback is None:
            msg = "To work with this methods, you need to create a BotCallback class and pass it as a parameter to the Bot class"
            raise ValueError(msg)
        return self._callback.construct(self.api, self.error_handler)

    @property
    def polling(self) -> "ABCPolling":
        polling = self._polling.construct(self.api, self.error_handler)
        if isinstance(polling, BotPolling):
            polling.skip_old_events = self.skip_old_events
        return polling

    @property
    def router(self) -> "ABCRouter":
        return self._router.construct(
            views=self.labeler.views(),
            state_dispenser=self.state_dispenser,
            error_handler=self.error_handler,
        )

    @router.setter
    def router(self, new_router: "ABCRouter") -> None:
        self._router = new_router

    @property
    def on(self) -> "ABCLabeler":
        return self.labeler

    async def setup_webhook(self) -> tuple[str, str]:
        """:return: confirmation_code, secret_key"""

        await self.callback.setup_group_id()

        confirmation_code: str = await self.callback.get_callback_confirmation_code()
        secret_key: str = self.callback.get_secret_key()

        server_id = await self.callback.find_server_id()
        if server_id is not None:
            await self.callback.set_callback_settings(server_id, {"message_new": True})
            await self.callback.edit_callback_server(server_id)
        else:
            server_id = await self.callback.add_callback_server()
            await self.callback.set_callback_settings(server_id, {"message_new": True})

        return confirmation_code, secret_key

    async def process_event(self, event: dict[str, Any], api: "ABCAPI | None" = None) -> None:
        if self.dual_mode is False or self.event_deduplicator is None:
            await super().process_event(event, api)
            return

        if await self.event_deduplicator.claim(event) is False:
            logger.debug("Skipping duplicate event: {!r}", event)
            return

        await super().process_event(event, api)


__all__ = ("Bot",)
