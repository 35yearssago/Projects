from django.urls import path
from myproject.web import views

urlpatterns = [
    path("", views.index_page, name="index page"),

    path("dashboard/", views.dashboard_page, name="dashboard page"),
    path("create/", views.fruit_create_page, name="fruit create page"),
    path("<int:id>/details/", views.fruit_detail_page, name="fruit details page"),
    path("<int:id>/edit/", views.fruit_edit_page, name="fruit edit page"),
    path("<int:id>/delete/", views.fruit_delete_page, name="fruit delete page"),

    path("profile/create/", views.profile_create_page, name="profile create page"),
    path("profile/details/", views.profile_details_page, name="profile details page"),
    path("profile/edit/", views.profile_edit_page, name="profile edit page"),
    path("profile/delete/", views.profile_delete_page, name="profile delete page"),
]
