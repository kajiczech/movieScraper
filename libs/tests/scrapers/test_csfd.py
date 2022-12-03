from unittest import skip

from django.test import TestCase

from libs.scrapers.csfd import CsfdScraper


# TODO: We should mock the requests...
class CsfdScraperTest(TestCase):

    def test_get_movie_data(self):
        result = CsfdScraper.get_movie_data("https://www.csfd.cz/film/2294-vykoupeni-z-veznice-shawshank/prehled/")
        self.assertEqual(result.name, 'Vykoupení z věznice Shawshank')
        self.assertEqual(result.actors, ['Tim Robbins', 'Morgan Freeman', 'Bob Gunton', 'William Sadler', 'Clancy Brown',
                                         'Gil Bellows', 'Mark Rolston', 'James Whitmore', 'Jeffrey DeMunn'])
        self.assertEqual(result.year, 1994)

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
        self.assertRaises(AssertionError, CsfdScraper.get_top_movie_links, CsfdScraper.MAX_SIZE+1)

