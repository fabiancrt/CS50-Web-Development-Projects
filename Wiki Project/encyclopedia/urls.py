from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    #the url path i made according to the specs
    path("wiki/<str:title>", views.entry, name="entry"),
    #now the search url!
    path("search", views.search, name="search"),
    #here is the url for new page creations
    path("new_page", views.new_page, name="new_page"),
    #the url edit page
    path("wiki/<str:title>/edit", views.edit_page, name="edit_page"),
    #url to random page
    path("random_page", views.random_page, name="random_page"),
]
