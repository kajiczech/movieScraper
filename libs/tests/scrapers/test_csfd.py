from unittest import skip

from django.test import TestCase

from libs.scrapers.csfd import CsfdScraper


# TODO: We should mock the requests...
class CsfdScraperTest(TestCase):

    def test_get_movie_data(self):
        result = CsfdScraper.get_movie_data("https://www.csfd.cz/film/2294-vykoupeni-z-veznice-shawshank/prehled/")
        self.assertEqual(result.name, 'Vykoupení z věznice Shawshank')
        self.assertEqual(result.year, 1994)
        self.assertEqual(result.actors, ['Tim Robbins', 'Morgan Freeman', 'Bob Gunton', 'William Sadler', 'Clancy Brown',
                                         'Gil Bellows', 'Mark Rolston', 'James Whitmore', 'Jeffrey DeMunn',
                                         'Larry Brandenburg', 'Neil Giuntoli', 'David Proval', 'Jude Ciccolella',
                                         'Paul McCrane', 'Alfonso Freeman', 'Ned Bellamy', 'James Babson',
                                         'Renee Blaine','Frank Medrano','Don McManus', 'Brian Libby', 'Dion Anderson',
                                         'Joseph Ragno','Sergio Kato','Morgan Lund', 'Brian Brophy', 'V.J. Foster',
                                         'Brian Delate', 'Bill Bolender', 'Neil Summers', 'Dorothy Silver', 'Ken Magee'
                                         ]
                         )

    def test_get_movie_no_more_actors(self):
        self.maxDiff = None

        result = CsfdScraper.get_movie_data("https://www.csfd.cz/film/10103-cesta-do-praveku/prehled/")
        self.assertEqual(result.actors, ['Vladimír Bejval', 'Petr Herrmann', 'Josef Lukáš', 'Zdeněk Husták', 'Bedřich Šetena'])

    def test_get_top_movie_links(self):
        result = CsfdScraper.get_top_movie_links(300)
        self.assertEqual(len(result), 300)
        self.assertEqual(result[0], "https://www.csfd.cz/film/2294-vykoupeni-z-veznice-shawshank/")
        self.assertEqual(result[1], "https://www.csfd.cz/film/10135-forrest-gump/")
        self.assertEqual(result[299], "https://www.csfd.cz/film/26204-jestli-se-rozzlobime-budeme-zli/")

    @skip
    def testget_top_movie_links_max(self):
        result = CsfdScraper.get_top_movie_links(1000)
        self.assertEqual(len(result), 1000)
        self.assertEqual(result[0], "https://www.csfd.cz/film/2294-vykoupeni-z-veznice-shawshank/")
        self.assertEqual(result[1], "https://www.csfd.cz/film/10135-forrest-gump/")
        self.assertEqual(result[999], "https://www.csfd.cz/film/743603-mistnost-sebevrahu-hater/")

    def test_get_top_movie_links_too_big_count(self):
        self.assertRaises(AssertionError, CsfdScraper.get_top_movie_links, CsfdScraper.MAX_SIZE + 1)
