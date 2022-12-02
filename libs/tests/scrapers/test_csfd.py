from django.test import TestCase

from libs.scrapers.csfd import CsfdScraper


# TODO: We should mock the requests...
class CsfdScraperTest(TestCase):

    def test_get_movie_data(self):
        result = CsfdScraper.get_movie_data("https://www.csfd.cz/film/2294-vykoupeni-z-veznice-shawshank/prehled/")
        self.assertEqual(result.name, 'Vykoupení z věznice Shawshank')
        self.assertEqual(result.actors, ['Tim Robbins', 'Morgan Freeman', 'Bob Gunton', 'William Sadler', 'Clancy Brown',
                                         'Gil Bellows', 'Mark Rolston', 'James Whitmore', 'Jeffrey DeMunn'])

    def test_get_top_movies(self):
        result = CsfdScraper.get_top_movies(2)
        self.assertEqual(result[0].name, 'Vykoupení z věznice Shawshank')
        self.assertEqual(result[0].actors, ['Tim Robbins', 'Morgan Freeman', 'Bob Gunton', 'William Sadler', 'Clancy Brown',
                                         'Gil Bellows', 'Mark Rolston', 'James Whitmore', 'Jeffrey DeMunn'])

        self.assertEqual(result[1].name, 'Forrest Gump')
        self.assertEqual(result[1].actors, ['Tom Hanks', 'Robin Wright', 'Gary Sinise', 'Mykelti Williamson', 'Sally Field',
                                            'Haley Joel Osment', 'Peter Dobson', 'Siobhan Fallon Hogan', 'Hanna Hall', 'Brett Rice'])

        self.assertEqual(len(result), 2)
