import json
from typing import Optional

from django.core.exceptions import ValidationError, FieldError
from django.db import IntegrityError
from django.db.models import Model
from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from core.utils import swap_string, get_model, fix_keys_in_dict, create_obj


def import_data(body: list) -> JsonResponse:
    """
    Import model objects from JSON data.
    """
    for obj_dict in body:
        # Get model name from the first key in the dictionary
        model_name = swap_string(next(iter(obj_dict)))
        model = get_model(model_name)
        if not model:
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

        try:
            create_obj(model, obj_data)
        except (
            AttributeError,
            ValueError,
            IntegrityError,
            ValidationError,
            FieldError,
        ) as e:
            return JsonResponse(
                {
                    "status": "error",
                    "error": f"Invalid data for {model_name}: {e}",
                },
                status=400,
            )

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
        model = get_model(model_name)
        if not model:
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

        model = get_model(model_name)
        if not model:
            return JsonResponse(
                {
                    "status": "error",
                    "error": f"Invalid model name: {model_name}",
                },
                status=400,
            )

        try:
            obj = model.objects.get(pk=pk)
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
