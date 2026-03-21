![Test](https://github.com/jdiego/django-ninja-plus/workflows/Test/badge.svg)
[![PyPI version](https://badge.fury.io/py/django-ninja-plus.svg)](https://badge.fury.io/py/django-ninja-plus)
[![PyPI](https://img.shields.io/pypi/v/django-ninja-plus.svg)](https://pypi.org/project/django-ninja-plus/)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-ninja-plus.svg)](https://pypi.org/project/django-ninja-plus/)
[![Django Versions](https://img.shields.io/pypi/djversions/django-ninja-plus.svg)](https://pypi.org/project/django-ninja-plus/)
[![Codecov](https://img.shields.io/codecov/c/gh/jdiego/django-ninja-plus)](https://codecov.io/gh/jdiego/django-ninja-plus)
[![Downloads](https://static.pepy.tech/badge/django-ninja-plus)](https://pepy.tech/project/django-ninja-plus)

# Django Ninja Plus

> ⚠️ This project is a fork of django-ninja-extra, originally created by Ezeudoh Tochukwu.
> It continues development with an independent roadmap and improvements while preserving compatibility where possible.

Django Ninja Plus is a modern, extensible toolkit for building structured, scalable APIs with Django Ninja.
It builds on the foundations of django-ninja-extra and introduces a more maintainable, extensible, and future-proof architecture.

This project aims to evolve the original ideas with improvements in typing, extensibility, and integration with modern tooling.


## Features

### Core Features (Inherited from Django Ninja)
- ⚡ **High Performance**: Built on Pydantic for lightning-fast validation
- 🔄 **Async Support**: First-class support for async/await operations
- 📝 **Type Safety**: Comprehensive type hints for better development experience
- 🎯 **Django Integration**: Seamless integration with Django's ecosystem
- 📚 **OpenAPI Support**: Automatic API documentation with Swagger/ReDoc
- 🔒 **API Throttling**: Rate limiting for your API

### Extra Features
- 🏗️ **Class-Based Controllers**: 
  - Organize related endpoints in controller classes
  - Inherit common functionality
  - Share dependencies across endpoints

- 🔒 **Advanced Permission System (Similar to Django Rest Framework)**:
  - Controller-level permissions
  - Route-level permission overrides
  - Custom permission classes

- 💉 **Dependency Injection**:
  - Built-in support for [Injector](https://injector.readthedocs.io/en/latest/)
  - Compatible with [django_injector](https://github.com/blubber/django_injector)
  - Automatic dependency resolution

- 🔧 **Service Layer**:
  - Injectable services for business logic
  - Better separation of concerns
  - Reusable components

## Requirements

- Python >= 3.12
- Django >= 4.2
- Pydantic >= 2.x
- Django-Ninja >= 1.x


## Installation

1. Install the package:
```bash
uv add django-ninja-plus
```

2. Add to INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...,
    'ninja_plus',
]
```

## Quick Start Guide

### 1. Basic API Setup

Create `api.py` in your Django project:

```python
from ninja_plus import NinjaExtraAPI, api_controller, http_get

api = NinjaExtraAPI()

# Function-based endpoint example
@api.get("/hello", tags=['Basic'])
def hello(request, name: str = "World"):
    return {"message": f"Hello, {name}!"}

# Class-based controller example
@api_controller('/math', tags=['Math'])
class MathController:
    @http_get('/add')
    def add(self, a: int, b: int):
        """Add two numbers"""
        return {"result": a + b}

    @http_get('/multiply')
    def multiply(self, a: int, b: int):
        """Multiply two numbers"""
        return {"result": a * b}

# Register your controllers
api.register_controllers(MathController)
```

### 2. URL Configuration

In `urls.py`:
```python
from django.urls import path
from .api import api

urlpatterns = [
    path("api/", api.urls),  # This will mount your API at /api/
]
```

## Advanced Features

### Authentication and Permissions

```python
from ninja_plus import api_controller, http_get
from ninja_plus.permissions import IsAuthenticated, PermissionBase

# Custom permission
class IsAdmin(PermissionBase):
    def has_permission(self, context):
        return context.request.user.is_staff

@api_controller('/admin', tags=['Admin'], permissions=[IsAuthenticated, IsAdmin])
class AdminController:
    @http_get('/stats')
    def get_stats(self):
        return {"status": "admin only data"}
    
    @http_get('/public', permissions=[])  # Override to make public
    def public_stats(self):
        return {"status": "public data"}
```

### Dependency Injection with Services

```python
from injector import inject
from ninja_plus import api_controller, http_get


# Service class
class UserService:
    def get_user_details(self, user_id: int):
        return {"user_id": user_id, "status": "active"}


# Controller with dependency injection
@api_controller('/users', tags=['Users'])
class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @http_get('/{user_id}')
    def get_user(self, user_id: int):
        return self.user_service.get_user_details(user_id)
```

## API Documentation

Access your API's interactive documentation at `/api/docs`:

![Swagger UI](docs/images/ui_swagger_preview_readme.gif)


## Contributing

We welcome contributions! Here's how you can help:

1. Clone this repository
2. Create a feature branch
3. Write your changes
4. Submit a pull request

Please ensure your code follows our coding standards and includes appropriate tests.

## Development Setup

Use `uv` to create the environment and install all local development dependencies:

```bash
uv sync --group dev
uv run pre-commit install -f
```

Common commands:

```bash
uv run pytest
uv run ruff check ninja_plus tests
uv run mypy ninja_plus
uv run mkdocs serve
```

## Origin and Credits

This project is based on django-ninja-extra, originally created by Ezeudoh Tochukwu.

All original copyright and license terms are preserved under the MIT License.

## License

This project is licensed under the MIT License - see the LICENSE file for details.


## Why this fork exists

- Continue development of django-ninja-extra
- Improve typing and maintainability
- Provide better integration with modern Python tooling (uv, typing, OpenAPI)
- Enable long-term evolution of the framework


## Support the Project

- ⭐ Star the repository
- 🐛 Report issues
- 📖 Contribute to documentation
- 🤝 Submit pull requests
