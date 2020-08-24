from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random_page, name = "random"),
    path("new", views.new_page, name = "new"),
    path("search", views.search_pages, name = "search"),
    path("edit/<str:entry>", views.edit_page, name = "edit"),
    path("wiki/<str:entry>", views.entry_check, name = "entry_check")
]
