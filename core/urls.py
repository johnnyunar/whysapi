from django.urls import path

from core import views

urlpatterns = [
    path("import/", views.ImportObjectsView.as_view(), name="import_objects"),
    path(
        "detail/<str:model_name>/",
        views.ModelListView.as_view(),
        name="model_list",
    ),
    path(
        "detail/<str:model_name>/<int:pk>/",
        views.ObjectDetailView.as_view(),
        name="object_detail",
    ),
]
