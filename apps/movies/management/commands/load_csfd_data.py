from django.core.management.base import BaseCommand
from django.db import transaction
from text_unidecode import unidecode

from apps.movies.models import Actor, Movie
from libs.scrapers.csfd import CsfdScraper


class Command(BaseCommand):
    help = 'Load/Refresh --movie_count of top CSFD movies into our database'

    def add_arguments(self, parser):
        parser.add_argument('--movie_count', type=int, default=300, help=f"How many movies we want to fetch - maximum is {CsfdScraper.MAX_SIZE}")

    def handle(self, *args, **options):
        assert options['movie_count'] <= CsfdScraper.MAX_SIZE

        for movie_link in CsfdScraper.get_top_movie_links(options['movie_count']):
            with transaction.atomic():
                movie_data = CsfdScraper.get_movie_data(movie_link)
                movie, _ = Movie.objects.get_or_create(name=movie_data.name, unicode_name=unidecode(movie_data.name).lower())
                for actor_name in movie_data.actors:
                    actor, _ = Actor.objects.get_or_create(name=actor_name, unicode_name=unidecode(actor_name).lower())
                    actor.movies.add(movie)
            print(f'loaded: {movie_data}')

        print("Done.")





