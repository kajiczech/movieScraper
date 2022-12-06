import dataclasses
import datetime
import logging
from typing import List

import requests
from bs4 import BeautifulSoup, element

# Need to use these headers to avoid 429 error - too many requests on CSFD
BROWSER_LIKE_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2172.95 Safari/537.36'}


@dataclasses.dataclass
class MovieData:
    name: str
    year: int
    actor_links: List[str]


@dataclasses.dataclass
class ActorData:
    name: str
    date_of_birth: datetime.date | None
    city_of_birth: str | None


class CsfdScraper:
    base_url = 'https://www.csfd.cz'
    movie_list_url = 'https://www.csfd.cz/zebricky/filmy/nejlepsi/?from={page}'
    page_size = 100
    actor_header_text = "Hrají: "
    MAX_SIZE = 1000  # There are only 1000 top films on csfd now
    movie_link_class = "film-title-name"
    movie_year_class = "origin"
    more_actors_class = "more-member-1"

    class EmptyPageError(Exception):
        pass

    @classmethod
    def get_page(cls, link) -> BeautifulSoup:
        response = requests.get(f"{link}", headers=BROWSER_LIKE_HEADERS)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    @classmethod
    def get_top_movie_links(cls, count: int) -> List[str]:
        """
        Returns links to CSFD top movies.

        We can find out the links by looking for class 'film-title-name' and then using its href to redirect
        :param: count integer value up to cls.MAX_SIZE
        """
        assert count <= cls.MAX_SIZE, f"Count can be only up to {cls.MAX_SIZE}"

        movie_urls = []
        page_offset = 0

        while len(movie_urls) < count:
            list_soup = cls.get_page(cls.movie_list_url.format(page=page_offset))
            movies = list_soup.find_all('a', attrs={"class": cls.movie_link_class})

            if not movies:
                raise cls.EmptyPageError

            for movie_link in movies:
                movie_urls.append(cls.base_url + movie_link.get('href'))
                if len(movie_urls) >= count:
                    break

            page_offset += cls.page_size

        return movie_urls

    @classmethod
    def get_movie_data(cls, link: str) -> MovieData:
        movie_soup = cls.get_page(link)
        acting_element = movie_soup.find('h4', string=cls.actor_header_text).parent

        name = movie_soup.find('h1').text.strip()

        actor_links = cls._get_actor_links(acting_element)
        if more_acting_element := acting_element.find(attrs={"class": cls.more_actors_class}):
            actor_links += cls._get_actor_links(more_acting_element)

        year = int(movie_soup.find('div', attrs={"class": cls.movie_year_class}).find('span').text.replace(', ', ''))

        return MovieData(name=name, year=year, actor_links=actor_links)

    @classmethod
    def get_actor_data(cls, link: str) -> ActorData:
        actor_soup = cls.get_page(link)
        name_element = actor_soup.find('h1')

        name = name_element.text.strip()

        date_of_birth, city = cls._get_birth_and_city(name_element)
        return ActorData(name=name, date_of_birth=date_of_birth, city_of_birth=city)

    @classmethod
    def _get_actor_links(cls, acting_element: element) -> List[str]:
        return [cls.base_url + actor.get('href') for actor in acting_element.find_all('a', recursive=False)]

    @classmethod
    def _get_birth_and_city(cls, name_element: element) -> tuple[datetime.date | None, str | None]:
        name_subtext_lines = name_element.next_sibling.next_sibling.text.strip().split('\n')

        if not name_subtext_lines[0]:  # There can be actors without bio
            return None, None

        city = None
        date_of_birth = None

        if len(name_subtext_lines) <= 2:
            if name_subtext_lines[0].startswith('nar.'):
                birth_line = name_subtext_lines[0]
                city_line = None
            else:
                birth_line = None
                city_line = name_subtext_lines[0]
        else:
            birth_line = name_subtext_lines[0]
            city_line = name_subtext_lines[2]

        if birth_line:
            try:
                date_of_birth = datetime.datetime.strptime(birth_line.split(' ')[1], "%d.%m.%Y").date()
            except ValueError:
                date_of_birth = datetime.datetime.strptime(birth_line.split(' ')[1], "%Y").date()

        if city_line:
            city = city_line.strip().split(',')[0]

        return date_of_birth, city
