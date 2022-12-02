
from django.contrib import admin
from django.urls import path, include

from apps.movies.views import SearchFormView, MovieView, ActorView

app_name = 'movies'
urlpatterns = [
    path('search/', SearchFormView.as_view(), name='search-landing'),
    path('search/<str:search>/', SearchFormView.as_view(), name='search'),
    path('movie/<uuid:pk>/', MovieView.as_view(), name='movie-detail'),
    path('actor/<uuid:pk>/', ActorView.as_view(), name='actor-detail'),
]


