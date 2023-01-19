import json

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

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


def import_data(body: list) -> JsonResponse:
    for obj_dict in body:
        # Get model name from the first key in the dictionary
        model_name = swap_string(next(iter(obj_dict)))
        try:
            model: Model = apps.get_model(
                app_label="core", model_name=model_name
            )
        except LookupError:
            return JsonResponse(
                {
                    "status": "error",
                    "error": f"Invalid model name: {model_name}",
                },
                status=400,
            )
        obj_data: dict = next(iter(obj_dict.values()))

        if not obj_data.get("id"):
            return JsonResponse(
                {
                    "status": "error",
                    "error": f"Missing ID for {model_name}",
                },
                status=400,
            )

        attributes_ids: list = obj_data.pop("attributes_ids", None)
        products_ids: list = obj_data.pop("products_ids", None)

        try:
            obj, _ = model.objects.update_or_create(
                id=obj_data["id"], defaults=fix_keys_in_dict(obj_data)
            )
        except (ValueError, IntegrityError, ValidationError) as e:
            return JsonResponse(
                {
                    "status": "error",
                    "error": f"Invalid data for {model_name}: {e}",
                },
                status=400,
            )

        if attributes_ids:
            obj.attributes.set(attributes_ids)
        if products_ids:
            obj.products.set(products_ids)

    return JsonResponse({"status": "success"})


@method_decorator(csrf_exempt, name="dispatch")
class ImportObjectsView(View):
    """
    View for importing objects from JSON.
    """

    def post(self, *args, **kwargs):
        """
        Import objects from JSON.
        """
        try:
            body = json.loads(self.request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "error": "Invalid JSON"}, status=400
            )

        return import_data(body)


class ModelListView(View):
    """
    View for listing objects for a given model.
    """

    def get(self, *args, **kwargs):
        """
        List objects for a given model.
        """
        model_name = self.kwargs["model_name"]
        try:
            model: Model = apps.get_model(
                app_label="core", model_name=model_name
            )
        except LookupError:
            return JsonResponse(
                {
                    "status": "error",
                    "error": f"Invalid model name: {model_name}",
                },
                status=400,
            )
        return JsonResponse(list(model.objects.values()), safe=False)


class ObjectDetailView(View):
    """
    View providing detail of a given object.
    """

    def get(self, *args, **kwargs):
        """
        Return detail of a given object.
        """
        model_name = self.kwargs["model_name"]
        pk = self.kwargs["pk"]

        try:
            model: Model = apps.get_model(
                app_label="core", model_name=model_name
            )
        except LookupError:
            return JsonResponse(
                {
                    "status": "error",
                    "error": f"Invalid model name: {model_name}",
                },
                status=400,
            )

        try:
            obj = model.objects.get(id=pk)
        except model.DoesNotExist:
            return JsonResponse(
                {
                    "status": "error",
                    "error": f"{model._meta.verbose_name.capitalize()} "
                    f"with ID {pk} does not exist",
                },
                status=404,
            )

        return JsonResponse(model_to_dict(obj))
