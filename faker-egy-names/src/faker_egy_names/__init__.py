"""Faker provider for grounded Egyptian names (wraps egy-names)."""

from __future__ import annotations

from .provider import EgyptianNamesProvider, Provider, egyptian_faker

__version__ = "0.1.0"
__author__ = "Abdullah Afify"
__company__ = "Afify"
__license__ = "MIT"

__all__ = [
    "EgyptianNamesProvider",
    "Provider",
    "egyptian_faker",
    "__version__",
]
