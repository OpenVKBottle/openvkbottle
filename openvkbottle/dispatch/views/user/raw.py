import dataclasses
from typing import TYPE_CHECKING, Any

from openvkbottle_types.events import UserEventType

from openvkbottle.dispatch.return_manager.user import UserMessageReturnHandler
from openvkbottle.dispatch.views.abc.raw import ABCRawEventView, BaseHandlerBasement

if TYPE_CHECKING:
    from openvkbottle_types.events.user_events import BaseUserEvent

    from openvkbottle.dispatch.handlers import ABCHandler
    from openvkbottle.exception_factory.error_handler import ABCErrorHandler


@dataclasses.dataclass(frozen=True)
class UserHandlerBasement(BaseHandlerBasement):
    dataclass: type["BaseUserEvent"]
    handler: "ABCHandler"


class RawUserEventView(ABCRawEventView[list[Any], UserHandlerBasement]):
    handlers: dict[UserEventType, list[UserHandlerBasement]]

    def __init__(self, error_handler: "ABCErrorHandler | None" = None) -> None:
        super().__init__(error_handler)
        self.handlers = {}
        self.handler_return_manager = UserMessageReturnHandler()

    def get_handler_basements(self, event: list[Any]) -> list[UserHandlerBasement]:
        return self.handlers[UserEventType(self.get_event_type(event))]

    def get_event_model(
        self,
        handler_basement: UserHandlerBasement,
        event: list[Any],
    ) -> "BaseUserEvent":
        return handler_basement.dataclass.parse(event[1:])

    @staticmethod
    def get_event_type(event: list[Any]) -> int:
        return event[0]

    async def process_event(self, event: list[Any]) -> bool:
        try:
            event_type = UserEventType(self.get_event_type(event))
        except ValueError:
            event_type = UserEventType.UNDEFINED_EVENT

        return event_type in self.handlers


__all__ = ("RawUserEventView", "UserHandlerBasement")
