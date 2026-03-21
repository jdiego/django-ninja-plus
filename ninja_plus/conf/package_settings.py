from typing import Any, Dict, List, Optional

from django.conf import settings as django_settings
from django.core.signals import setting_changed
from ninja.pagination import PaginationBase
from ninja.throttling import BaseThrottle
from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ninja_plus.conf.decorator import AllowTypeOfSource
from ninja_plus.interfaces.ordering import OrderingBase
from ninja_plus.interfaces.route_context import RouteContextBase
from ninja_plus.interfaces.searching import SearchingBase
from ninja_plus.lazy import LazyStrImport

_GenericModelValidator = AllowTypeOfSource(
    validator=lambda source, value: (
        isinstance(value, LazyStrImport)
        or isinstance(value, type)
        and issubclass(value, source)
    ),
    error_message=lambda source, value: (
        f"Expected type of {source.__name__}, received: {type(value)}"
    ),
)

PaginationClassHandlerType = Annotated[PaginationBase, _GenericModelValidator]
ThrottlingClassHandlerType = Annotated[BaseThrottle, _GenericModelValidator]
SearchingClassHandlerType = Annotated[SearchingBase, _GenericModelValidator]
OrderingClassHandlerType = Annotated[OrderingBase, _GenericModelValidator]
RouteContextHandlerType = Annotated[RouteContextBase, _GenericModelValidator]

_InjectorModuleValidator = AllowTypeOfSource(
    validator=lambda source, value: value is not None,
    error_message=lambda source, value: (
        f"Expected PaginationBase object, received: {type(value)}"
    ),
)
InjectorModuleHandlerType = Annotated[Any, _InjectorModuleValidator]


class UserDefinedSettingsMapper:
    def __init__(self, data: dict) -> None:
        self.__dict__ = dict(NinjaEXTRA_SETTINGS_DEFAULTS, **data)


NinjaEXTRA_SETTINGS_DEFAULTS = {
    "INJECTOR_MODULES": [],
    "PAGINATION_CLASS": "ninja.pagination.LimitOffsetPagination",
    "THROTTLE_CLASSES": [
        "ninja_plus.throttling.AnonRateThrottle",
        "ninja_plus.throttling.UserRateThrottle",
    ],
    "THROTTLE_RATES": {"user": None, "anon": None},
    "ORDERING_CLASS": "ninja_plus.ordering.Ordering",
    "SEARCHING_CLASS": "ninja_plus.searching.Searching",
    "ROUTE_CONTEXT_CLASS": "ninja_plus.context.RouteContext",
}

USER_SETTINGS = UserDefinedSettingsMapper(
    getattr(django_settings, "ninja_plus", NinjaEXTRA_SETTINGS_DEFAULTS)
)


class NinjaExtraSettings(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    PAGINATION_CLASS: PaginationClassHandlerType = Field(  # type: ignore[assignment]
        "ninja.pagination.LimitOffsetPagination",
    )
    PAGINATION_PER_PAGE: int = Field(100)
    THROTTLE_RATES: Dict[str, Optional[str]] = Field(
        {"user": "1000/day", "anon": "100/day"}
    )
    THROTTLE_CLASSES: List[ThrottlingClassHandlerType] = Field(
        [
            "ninja_plus.throttling.AnonRateThrottle",  # type: ignore[list-item]
            "ninja_plus.throttling.UserRateThrottle",  # type: ignore[list-item]
        ]
    )
    NUM_PROXIES: Optional[int] = None
    INJECTOR_MODULES: List[InjectorModuleHandlerType] = []
    ORDERING_CLASS: OrderingClassHandlerType = Field(  # type: ignore[assignment]
        "ninja_plus.ordering.Ordering",
    )
    SEARCHING_CLASS: SearchingClassHandlerType = Field(  # type: ignore[assignment]
        "ninja_plus.searching.Searching",
    )
    ROUTE_CONTEXT_CLASS: RouteContextHandlerType = Field(  # type: ignore[assignment]
        "ninja_plus.context.RouteContext",
    )


settings = NinjaExtraSettings.model_validate(USER_SETTINGS)


def reload_settings(*args: Any, **kwargs: Any) -> None:  # pragma: no cover
    global settings

    setting, value = kwargs["setting"], kwargs["value"]

    if setting == "ninja_plus":
        settings = NinjaExtraSettings.model_validate(UserDefinedSettingsMapper(value))


setting_changed.connect(reload_settings)  # pragma: no cover
