from django.core.management.base import BaseCommand
from django.db import transaction

from apps.movies.models import Actor, Movie
from libs.scrapers.csfd import CsfdScraper


class Command(BaseCommand):
    help = 'Load/Refresh --movie_count of top CSFD movies into our database'

    def add_arguments(self, parser):
        parser.add_argument('--movie_count', type=int, default=300)

    @transaction.atomic
    def handle(self, *args, **options):
        for movie_data in CsfdScraper.get_top_movies(options['movie_count']):
            movie, _ = Movie.objects.get_or_create(name=movie_data.name)
            for actor_name in movie_data.actors:
                actor, _ = Actor.objects.get_or_create(name=actor_name)
                actor.movies.add(movie)





