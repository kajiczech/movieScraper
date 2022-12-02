from django.test import TestCase
from django.urls import reverse

from apps.movies.models import Movie, Actor


# This should be done using some fixture or recipe...
class SetupMixin:
    def setUp(self):
        self.movie1 = Movie.objects.create(name='LORD of the rings', unicode_name='lord of the rings', year=2022)
        self.movie2 = Movie.objects.create(name='Input OŘD', unicode_name='input ord', year=2022)
        self.movie3 = Movie.objects.create(name='Matrix revolutions', unicode_name='matrix revolutions', year=2022)
        self.actor1 = Actor.objects.create(name='LórdDicaprio', unicode_name='lorddicaprio')
        self.actor2 = Actor.objects.create(name='Karel Čech', unicode_name='karel cech')
        self.actor3 = Actor.objects.create(name='No Name', unicode_name='no name')
        self.movie1.actors.add(self.actor1, self.actor2)


class SearchFormViewTest(SetupMixin, TestCase):

    def test_search_landing(self):
        response = self.client.get(reverse('movies:search-landing'))
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.client.get(reverse('movies:search', kwargs={'search': 'óřď'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.movie1.name)
        self.assertContains(response, self.movie2.name)
        self.assertNotContains(response, self.movie3.name)
        self.assertContains(response, self.actor1.name)
        self.assertNotContains(response, self.actor2.name)

    def test_search_empty(self):
        response = self.client.get(reverse('movies:search', kwargs={'search': 'non-existent'}))
        self.assertEqual(response.status_code, 200)


class MovieViewTest(SetupMixin, TestCase):

    def test_get(self):
        response = self.client.get(reverse('movies:movie-detail', kwargs={'pk': self.movie1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.actor1.name)
        self.assertContains(response, self.actor2.name)
        self.assertNotContains(response, self.actor3.name)


class ActorViewTest(SetupMixin, TestCase):

    def test_get(self):
        response = self.client.get(reverse('movies:actor-detail', kwargs={'pk': self.actor1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.actor1.name)
        self.assertContains(response, self.movie1.name)
        self.assertNotContains(response, self.actor3.name)
        self.assertNotContains(response, self.movie2.name)

