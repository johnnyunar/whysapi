from django.test import RequestFactory, TestCase, Client
from django.apps import apps
from django.urls import reverse
import json

from core.models import AttributeName, AttributeValue, Product, Attribute
from core.views import ModelListView, ObjectDetailView


class ImportObjectsViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        AttributeName.objects.create(
            name="Attribute Name 1", code="attributename1", display=True
        )
        AttributeName.objects.create(
            name="Attribute Name 2", code="attributename2", display=True
        )
        AttributeValue.objects.create(value="Attribute Value 1")
        AttributeValue.objects.create(value="Attribute Value 2")

        Product.objects.create(
            name="CZK Product Published",
            price=100,
            currency="CZK",
            is_published=True,
        )
        Product.objects.create(
            name="USD Product Published",
            price=100,
            currency="USD",
            is_published=True,
        )
        Product.objects.create(
            name="EUR Product Not Published",
            price=100,
            currency="EUR",
            is_published=False,
        )
        Attribute.objects.create(name_id=1, value_id=1)
        Attribute.objects.create(name_id=2, value_id=2)

    def test_post_handles_json_data_correctly(self):
        data = [
            {
                "Attribute": {
                    "id": 1,
                    "nazev_atributu_id": 1,
                    "hodnota_atributu_id": 1,
                }
            },
        ]
        response = self.client.post(
            reverse("import_objects"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Attribute.objects.get(pk=1).name.pk, 1)
        self.assertEqual(Attribute.objects.get(pk=1).value.pk, 1)

    def test_post_correctly_creates_or_updates_objects(self):
        data = [
            {
                "Attribute": {
                    "id": 1,
                    "nazev_atributu_id": 1,
                    "hodnota_atributu_id": 1,
                }
            },
            {
                "Attribute": {
                    "id": 2,
                    "nazev_atributu_id": 1,
                    "hodnota_atributu_id": 2,
                }
            },
            {
                "Attribute": {
                    "id": 3,
                    "nazev_atributu_id": 2,
                    "hodnota_atributu_id": 1,
                }
            },
        ]
        response = self.client.post(
            reverse("import_objects"),
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(Attribute.objects.count(), 3)

    def test_post_handles_attributes_products_ids_correctly(self):
        data = [
            {
                "Catalog": {
                    "id": 1,
                    "name": "Test Object",
                    "attributes_ids": [1, 2],
                    "products_ids": [2, 3],
                }
            }
        ]
        response = self.client.post(
            reverse("import_objects"),
            data=json.dumps(data),
            content_type="application/json",
        )
        model = apps.get_model("core", "Catalog")
        obj = model.objects.get(id=1)
        self.assertEqual(obj.attributes.count(), 2)
        self.assertEqual(obj.products.count(), 2)

    def test_post_raises_error_on_invalid_id(self):
        data = [
            {
                "Attribute": {
                    "id": "invalid_id",
                    "nazev_atributu_id": 1,
                    "hodnota_atributu_id": 1,
                }
            },
        ]
        response = self.client.post(
            reverse("import_objects"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_post_raises_error_on_invalid_data(self):
        data = [
            {
                "AttributeName": {
                    "id": 3,
                    "nazev": "Attribute Name",
                    "hodnota": "Attribute Value",
                    "display": "Invalid Display Value",
                }
            },
        ]
        response = self.client.post(
            reverse("import_objects"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_post_raises_error_on_invalid_field_name(self):
        data = [
            {
                "AttributeName": {
                    "id": 3,
                    "nazev_atributu_id": 1,
                    "hodnota_atributu_id": 2,
                    "display": True
                }
            },
        ]
        response = self.client.post(
            reverse("import_objects"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_post_raises_error_on_invalid_model_name(self):
        data = [{"invalid_model_name": {"id": 1, "name": "Test Object"}}]
        response = self.client.post(
            reverse("import_objects"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


class ModelListViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.valid_model_name = "AttributeName"
        self.invalid_model_name = "invalid_model"

    def test_get_valid_model(self):
        request = self.factory.get("/")
        view = ModelListView.as_view()
        response = view(request, model_name=self.valid_model_name)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data, [])  # assuming 'valid_model' has no instances

    def test_get_invalid_model(self):
        request = self.factory.get("/")
        view = ModelListView.as_view()
        response = view(request, model_name=self.invalid_model_name)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(
            data,
            {
                "status": "error",
                "error": f"Invalid model name: {self.invalid_model_name}",
            },
        )


class ObjectDetailViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.valid_model_name = "AttributeName"
        self.invalid_model_name = "invalid_model"
        self.valid_pk = 1
        self.invalid_pk = 100

    @classmethod
    def setUpTestData(cls):
        AttributeName.objects.create(
            pk=1, name="Attribute Name 1", code="attributename1", display=True
        )

    def test_get_valid_object(self):
        request = self.factory.get("/")
        view = ObjectDetailView.as_view()
        response = view(
            request, model_name=self.valid_model_name, pk=self.valid_pk
        )
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_model(self):
        request = self.factory.get("/")
        view = ObjectDetailView.as_view()
        response = view(
            request, model_name=self.invalid_model_name, pk=self.valid_pk
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(
            data,
            {
                "status": "error",
                "error": f"Invalid model name: {self.invalid_model_name}",
            },
        )

    def test_get_invalid_object(self):
        request = self.factory.get("/")
        view = ObjectDetailView.as_view()
        response = view(
            request, model_name=self.valid_model_name, pk=self.invalid_pk
        )
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(
            data,
            {
                "status": "error",
                "error": f"Attribute name with ID {self.invalid_pk} does not exist",
            },
        )
