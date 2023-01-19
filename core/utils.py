from typing import Optional

from django.apps import apps
from django.db.models import Model

from core import const


def swap_string(string: str) -> str:
    """
    Swap string using IMPORT_MAPPING dictionary
    or return original string if not found.

    :param string: String to swap
    """
    return const.IMPORT_MAPPING.get(string, string)


def fix_keys_in_dict(dictionary: dict) -> dict:
    """
    Swap keys in dictionary using swap_string function.

    :param dictionary: Dictionary to fix
    """
    for key in list(dictionary):  # Force copy of keys to prevent RuntimeError
        dictionary[swap_string(key)] = dictionary.pop(key)

    return dictionary


def get_model(model_name: str) -> Optional[Model]:
    """
    Return model class if found, otherwise return None.

    :param model_name: Name of the model
    """
    try:
        return apps.get_model(app_label="core", model_name=model_name)
    except LookupError:
        return None


def create_obj(model, obj_data: dict) -> tuple[Model, bool]:
    """
    Create model object from dictionary. Returns 2-tuple of (object, created).

    :param model: Model class
    :param obj_data: Dictionary with object data
    :raises AttributeError: If model has no attribute with given name
    :raises ValueError: If value is not valid
    :raises IntegrityError: If field's value violates database integrity
    :raises ValidationError: If field's value is not valid
    :raises FieldError: If field name is not valid
    """

    attributes_ids: list = obj_data.pop("attributes_ids", None)
    products_ids: list = obj_data.pop("products_ids", None)

    obj, created = model.objects.update_or_create(
        id=obj_data["id"], defaults=fix_keys_in_dict(obj_data)
    )

    if attributes_ids:
        obj.attributes.set(attributes_ids)
    if products_ids:
        obj.products.set(products_ids)

    return obj, created
