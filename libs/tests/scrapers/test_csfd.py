import datetime
from unittest import skip

from django.test import TestCase

from libs.scrapers.csfd import CsfdScraper


# TODO: We should mock the requests...
class CsfdScraperTest(TestCase):

    def test_get_movie_data(self):
        self.maxDiff = None
        result = CsfdScraper.get_movie_data("https://www.csfd.cz/film/2294-vykoupeni-z-veznice-shawshank/prehled/")
        self.assertEqual(result.name, 'Vykoupení z věznice Shawshank')
        self.assertEqual(result.year, 1994)
        self.assertEqual(len(result.actor_links), 32)
        self.assertEqual(result.actor_links[0], 'https://www.csfd.cz/tvurce/103-tim-robbins/')
        self.assertEqual(result.actor_links[31], 'https://www.csfd.cz/tvurce/770475-ken-magee/')

    def test_get_movie_no_more_actors(self):
        self.maxDiff = None

        result = CsfdScraper.get_movie_data("https://www.csfd.cz/film/10103-cesta-do-praveku/prehled/")
        self.assertEqual(result.actor_links, [
            'https://www.csfd.cz/tvurce/1623-vladimir-bejval/',
            'https://www.csfd.cz/tvurce/1625-petr-herrmann/',
            'https://www.csfd.cz/tvurce/1627-josef-lukas/',
            'https://www.csfd.cz/tvurce/1626-zdenek-hustak/',
            'https://www.csfd.cz/tvurce/31845-bedrich-setena/'
          ])

    def test_get_top_movie_links(self):
        result = CsfdScraper.get_top_movie_links(300)
        self.assertEqual(len(result), 300)
        self.assertEqual(result[0], "https://www.csfd.cz/film/2294-vykoupeni-z-veznice-shawshank/")
        self.assertEqual(result[1], "https://www.csfd.cz/film/10135-forrest-gump/")
        self.assertEqual(result[299], "https://www.csfd.cz/film/10099-baron-prasil/")

    @skip
    def testget_top_movie_links_max(self):
        result = CsfdScraper.get_top_movie_links(1000)
        self.assertEqual(len(result), 1000)
        self.assertEqual(result[0], "https://www.csfd.cz/film/2294-vykoupeni-z-veznice-shawshank/")
        self.assertEqual(result[1], "https://www.csfd.cz/film/10135-forrest-gump/")
        self.assertEqual(result[999], "https://www.csfd.cz/film/743603-mistnost-sebevrahu-hater/")

    def test_get_top_movie_links_too_big_count(self):
        self.assertRaises(AssertionError, CsfdScraper.get_top_movie_links, CsfdScraper.MAX_SIZE + 1)

    def test_get_actor_data(self):
        actor_data = CsfdScraper.get_actor_data('https://www.csfd.cz/tvurce/1623-vladimir-bejval/')
        self.assertEqual(actor_data.name, 'Vladimír Bejval')
        self.assertEqual(actor_data.date_of_birth, datetime.date(1942, 12, 31))
        self.assertEqual(actor_data.city_of_birth, 'Praha')

    def test_get_actor_data_no_bio(self):
        actor_data = CsfdScraper.get_actor_data('https://www.csfd.cz/tvurce/55721-renee-blaine/diskuze/')
        self.assertEqual(actor_data.name, 'Renee Blaine')
        self.assertEqual(actor_data.date_of_birth, None)
        self.assertEqual(actor_data.city_of_birth, None)

    def test_get_actor_data_no_city(self):
        actor_data = CsfdScraper.get_actor_data('https://www.csfd.cz/tvurce/418947-bill-bolender/biografie/')
        self.assertEqual(actor_data.name, 'Bill Bolender')
        self.assertEqual(actor_data.date_of_birth, datetime.date(1940, 11, 14))
        self.assertEqual(actor_data.city_of_birth, None)

    def test_get_actor_no_date(self):
        actor_data = CsfdScraper.get_actor_data('https://www.csfd.cz/tvurce/331876-rebecca-klingler/biografie/')
        self.assertEqual(actor_data.name, 'Rebecca Klingler')
        self.assertEqual(actor_data.date_of_birth, None)
        self.assertEqual(actor_data.city_of_birth, 'Kokomo')

    def test_get_actor_only_year(self):
        actor_data = CsfdScraper.get_actor_data('https://www.csfd.cz/tvurce/15188-brett-rice/galerie/')
        self.assertEqual(actor_data.name, 'Brett Rice')
        self.assertEqual(actor_data.date_of_birth, datetime.date(1954, 1, 1))
        self.assertEqual(actor_data.city_of_birth, None)
