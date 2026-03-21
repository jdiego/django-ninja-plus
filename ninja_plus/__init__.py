"""Django Ninja Extra - Class Based Utility and more for Django Ninja(Fast Django REST framework)"""

__version__ = "0.31.2"

import django

from ninja_plus.controllers import (
    ControllerBase,
    ModelAsyncEndpointFactory,
    ModelConfig,
    ModelControllerBase,
    ModelControllerBuilder,
    ModelEndpointFactory,
    ModelPagination,
    ModelSchemaConfig,
    ModelService,
    ModelServiceBase,
    api_controller,
    http_delete,
    http_generic,
    http_get,
    http_patch,
    http_post,
    http_put,
)
from ninja_plus.controllers.route import route
from ninja_plus.dependency_resolver import get_injector, service_resolver
from ninja_plus.main import NinjaExtraAPI
from ninja_plus.pagination import paginate
from ninja_plus.router import Router
from ninja_plus.throttling import throttle

if django.VERSION < (3, 2):  # pragma: no cover
    default_app_config = "ninja_plus.apps.NinjaExtraConfig"


__all__ = [
    "ControllerBase",
    "api_controller",
    "NinjaExtraAPI",
    "route",
    "http_patch",
    "http_get",
    "http_put",
    "http_post",
    "http_delete",
    "http_generic",
    "permissions",
    "exceptions",
    "status",
    "shortcuts",
    "get_injector",
    "service_resolver",
    "lazy",
    "Router",
    "throttle",
    "paginate",
    "ModelControllerBase",
    "ModelConfig",
    "ModelService",
    "ModelSchemaConfig",
    "ModelControllerBuilder",
    "ModelPagination",
    "ModelServiceBase",
    "ModelControllerBase",
    "ModelEndpointFactory",
    "ModelAsyncEndpointFactory",
]
