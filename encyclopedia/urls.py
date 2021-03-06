from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("create", views.create, name="create"),
	path("wiki/<str:title>", views.wiki, name="wiki"),
	path("edit/<str:title>", views.edit, name="edit"),
	path("randomPage", views.randomPage, name="randomPage")
]
