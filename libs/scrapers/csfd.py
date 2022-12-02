import dataclasses
import logging
from typing import List

import requests
from bs4 import BeautifulSoup

# Need to use these headers to avoid 429 error - too many requests on CSFD
BROWSER_LIKE_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


@dataclasses.dataclass
class MovieData:
    name: str
    actors: List[str]  # Can be extended to another author model


class CsfdScraper:
    movie_list_url = 'https://www.csfd.cz/zebricky/filmy/nejlepsi/?showMore={page}'
    movie_link_pre = 'https://www.csfd.cz/'
    page_size = 100

    @classmethod
    def get_top_movies(cls, count: int) -> List[MovieData]:
        """
        Returns movies from CSFD top movies page along with actors who played there.

        We can find out the links by looking for class 'film-title-name' and then using its href to redirect
        """
        movie_models = []
        page = 0

        # To speed things up, we could run this in parallel
        while len(movie_models) < count:
            response = requests.get(cls.movie_list_url.format(page=page), headers=BROWSER_LIKE_HEADERS)

            list_soup = BeautifulSoup(response.text, 'html.parser')
            movies = list_soup.find_all('a', attrs={"class": "film-title-name"})
            for movie_link in movies:
                movie_data = cls.get_movie_data(cls.movie_link_pre + movie_link.get('href'))
                movie_models.append(movie_data)
                if len(movie_models) >= count:
                    break
            page += cls.page_size

        return movie_models


    @classmethod
    def get_movie_data(cls, link: str) -> MovieData:
        movie_page_response = requests.get(link, headers=BROWSER_LIKE_HEADERS)
        movie_soup = BeautifulSoup(movie_page_response.text, 'html.parser')
        acting_element = movie_soup.find('h4', string="Hrají: ").parent
        name = movie_soup.find('h1').text.strip()
        actor_names = [actor.text for actor in acting_element.find_all('a', recursive=False)]
        return MovieData(name, actors=actor_names)
