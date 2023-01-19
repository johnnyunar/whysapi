from typing import Optional

from django.apps import apps
from django.db.models import Model

from core import const


def swap_string(string: str) -> str:
    """
    Swap string using IMPORT_MAPPING dictionary
    or return original string if not found.
    """
    return const.IMPORT_MAPPING.get(string, string)


def fix_keys_in_dict(dictionary: dict) -> dict:
    """
    Swap keys in dictionary using swap_string function.
    """
    for key in list(dictionary):  # Force copy of keys to prevent RuntimeError
        dictionary[swap_string(key)] = dictionary.pop(key)

    return dictionary


def get_model(model_name: str) -> Optional[Model]:
    """
    Return model class if found, otherwise return None.
    """
    try:
        return apps.get_model(app_label="core", model_name=model_name)
    except LookupError:
        return None
