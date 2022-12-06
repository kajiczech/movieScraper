from django.core.management.base import BaseCommand
from django.db import transaction
from text_unidecode import unidecode

from apps.movies.models import Actor, Movie
from libs.scrapers.csfd import CsfdScraper


class Command(BaseCommand):
    help = 'Load/Refresh --movie_count of top CSFD movies into our database'

    def add_arguments(self, parser):
        parser.add_argument('--movie_count', type=int, default=300, help=f"How many movies we want to fetch - maximum is {CsfdScraper.MAX_SIZE}")
        parser.add_argument('--offset', type=int, default=0, help='From what movie we should start fetching - 1')

    def handle(self, *args, **options):
        assert options['movie_count'] <= CsfdScraper.MAX_SIZE
        assert options['movie_count'] > options['offset']

        movie_links = CsfdScraper.get_top_movie_links(options['movie_count'])[options['offset']:]
        # To speed things up, we could run this in parallel
        for i, movie_link in enumerate(movie_links):
            with transaction.atomic():
                movie_data = CsfdScraper.get_movie_data(movie_link)
                movie, _ = Movie.objects.get_or_create(
                    name=movie_data.name,
                    unicode_name=unidecode(movie_data.name).lower(),
                    year=movie_data.year
                )
                for actor_link in movie_data.actor_links:
                    actor_data = CsfdScraper.get_actor_data(actor_link)
                    actor, _ = Actor.objects.get_or_create(
                        name=actor_data.name,
                        unicode_name=unidecode(actor_data.name).lower(),
                        city_of_birth=actor_data.city_of_birth,
                        date_of_birth=actor_data.date_of_birth)

                    actor.movies.add(movie)
            print(f'{i+1}.loaded: {movie_data}')
        print(f"Currently {Movie.objects.count()} movies in db")
        print("Done.")





