from django.urls import path

from mcqapp.views import (
    create_mcq_view,
    delete_mcq_view,
    home_view,
    list_mcq_view,
    take_exam_view,
    update_mcq_view,
)

app_name = "mcqapp"

urlpatterns = [
    path("", home_view, name="home"),
    path("mcq/", list_mcq_view, name="list"),
    path("mcq_create/", create_mcq_view, name="mcq-create"),
    path("mcq_update/<uuid:id>/", update_mcq_view, name="mcq-update"),
    path("mcq_delete/<uuid:id>/", delete_mcq_view, name="mcq-delete"),
    path("take_exam/", take_exam_view, name="take-exam"),
]
