import typing as t

from ninja_plus.constants import API_CONTROLLER_INSTANCE
from ninja_plus.reflect import reflect

if t.TYPE_CHECKING:  # pragma: no cover
    from .base import APIController, ControllerBase


def get_api_controller(
    controller_class: t.Type["ControllerBase"],
) -> t.Optional["APIController"]:
    return t.cast(
        "APIController", reflect.get_metadata(API_CONTROLLER_INSTANCE, controller_class)
    )
