from django.test import TestCase

from libs.scrapers.csfd import CsfdScraper


# TODO: We should mock the requests...
class CsfdScraperTest(TestCase):

    def test_get_movie_data(self):
        result = CsfdScraper.get_movie_data("https://www.csfd.cz/film/2294-vykoupeni-z-veznice-shawshank/prehled/")
        self.assertEqual(result.name, 'Vykoupení z věznice Shawshank')
        self.assertEqual(result.actors, ['Tim Robbins', 'Morgan Freeman', 'Bob Gunton', 'William Sadler', 'Clancy Brown',
                                         'Gil Bellows', 'Mark Rolston', 'James Whitmore', 'Jeffrey DeMunn'])

    def test_get_top_movie_links(self):
        result = CsfdScraper.get_top_movie_links(250)
        self.assertEqual(len(result), 250)
        self.assertEqual(result[0], "https://www.csfd.cz/film/2294-vykoupeni-z-veznice-shawshank/")
        self.assertEqual(result[1], "https://www.csfd.cz/film/10135-forrest-gump/")

    def test_get_top_movie_links_too_big_count(self):
        self.assertRaises(AssertionError, CsfdScraper.get_top_movie_links, CsfdScraper.MAX_SIZE+1)

