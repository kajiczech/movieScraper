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
    movie_link_prefix = 'https://www.csfd.cz'
    page_size = 100
    actor_header_text = "Hrají: "
    MAX_SIZE = 1000  # There are only 1000 top films on csfd now

    @classmethod
    def get_top_movie_links(cls, count: int) -> List[str]:
        """
        Returns links to CSFD top movies.

        We can find out the links by looking for class 'film-title-name' and then using its href to redirect
        :param: count integer value up to cls.MAX_SIZE
        """
        assert count <= cls.MAX_SIZE, f"Count can be only up to {cls.MAX_SIZE}"

        movie_urls = []
        page = 0

        # To speed things up, we could run this in parallel
        while len(movie_urls) < count:
            response = requests.get(cls.movie_list_url.format(page=page), headers=BROWSER_LIKE_HEADERS)

            list_soup = BeautifulSoup(response.text, 'html.parser')
            movies = list_soup.find_all('a', attrs={"class": "film-title-name"})
            for movie_link in movies:
                movie_urls.append(cls.movie_link_prefix + movie_link.get('href'))
                if len(movie_urls) >= count:
                    break
            page += cls.page_size

        return movie_urls

    @classmethod
    def get_movie_data(cls, link: str) -> MovieData:
        movie_page_response = requests.get(link, headers=BROWSER_LIKE_HEADERS)
        movie_soup = BeautifulSoup(movie_page_response.text, 'html.parser')
        acting_element = movie_soup.find('h4', string=cls.actor_header_text).parent
        name = movie_soup.find('h1').text.strip()
        actor_names = [actor.text for actor in acting_element.find_all('a', recursive=False)]
        return MovieData(name, actors=actor_names)
