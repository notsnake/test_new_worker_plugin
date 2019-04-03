"""
Module for searching github and pastebin posts by regular expressions.
"""
import logging

import requests
from lxml import html
from requests.auth import HTTPBasicAuth
from requests.compat import urljoin
from requests.exceptions import ConnectionError

from tfw_myworker.exceptions import AuthenticationException, NotAvailableException

log = logging.getLogger(__name__)


class BaseParser:
    """
    Base class for parsers.
    """

    BASE_URL = 'https://api.github.com'  # as only an example
    POST_URL = '/gists/'  # as only an example
    POST_LIST_URL = '/gists/public'   # as only an example
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json; charset=UTF-8",
        "DNT": "1",
        "Pragma": "no-cache",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/71.0.3578.98 Safari/537.36",
    }

    def __init__(self, posts_number, match_patterns, username=None, password=None):
        """Init parser.

        :param posts_number: count recent posts
        :param match_patterns: regular expressions for find
        :param username: user name for access if it exists
        :param password:  user password for access if it exists
        """

        self.posts_number = posts_number
        self.match_patterns = match_patterns
        self.auth = HTTPBasicAuth(username, password) if username and password else None

    def _get_post_list_url(self):
        """Get url for post list.

        :return: post list url
        """
        return urljoin(self.BASE_URL, self.POST_LIST_URL)

    def _get_post_url(self, post_id):
        """Get url for post detail.

        :param post_id: post id for page
        :return: detail page url for parsing
        """

        post_url = '{}{}'.format(self.POST_URL, post_id)
        return urljoin(self.BASE_URL, post_url)

    def _make_request(self, url, params=None, to_json=True):
        """Make network query.

        :param url: query url
        :param params: query GET params
        :param to_json: is response a json
        :return: request response
        """
        try:
            response = requests.get(url, params=params, headers=self.headers, auth=self.auth)
        except ConnectionError:
            log.critical('Service unavailable')
            raise NotAvailableException('Service unavailable')

        if to_json:
            response = response.json()
            if isinstance(response, dict) and response.get('message'):
                message = response.get('message')
                log.critical(message)
                raise AuthenticationException(message)
        return response

    def _get_matches_in_text(self, content):
        """Look for matches in content text.

        :param content: text for searching
        :return: found patterns in content text
        """

        results = set()
        if content:
            for pattern in self.match_patterns.keys():
                result = pattern.search(content)
                if result:
                    results.update(self.match_patterns[pattern])
        return results

    def _add_data_to_response(self, desc_matches, url, page_matches, response):
        """Add description and page text matches to response if they were found.

        :param desc_matches: matches in description
        :param url:  post url
        :param page_matches: patches in detail page content
        :param response: page response
        """

        if desc_matches:
            response.append({
                'url': url,
                'matches': desc_matches
            })

        if page_matches:
            response.append({
                'url': url,
                'matches': page_matches
            })


class GitHubParser(BaseParser):
    """Parser for github pages."""
    BASE_URL = 'https://api.github.com'
    POST_URL = '/gists/'
    POST_LIST_URL = '/gists/public'
    COUNT_POSTS_MAX = 100

    def _get_files_content_page(self, item_id):
        """Get data files from post page.

        :param item_id: detail page id
        :return: content of files in detail post page
        """

        url = self._get_post_url(item_id)
        response = self._make_request(url)
        files = response.get('files') if response and response.get('files') else {}
        return files

    def _get_matches_on_page(self, item_id):
        """Find user matches in detail post page.

        :param item_id: detail page id
        :return: unique found patterns in content text for all files in detail page
        """
        """"""
        results = set()
        files = self._get_files_content_page(item_id)
        for file in files.values():
            content = file.get('content')
            found_patterns = self._get_matches_in_text(content)
            results.update(found_patterns)
        return results

    def _get_post_page_list(self, url, page, count):
        """Get post page list from github server.

        :param url: post list page url
        :param page: current page number
        :param count: count posts on page
        :return: list of found detail pages
        """
        params = {'page': page, 'per_page': count}
        items = self._make_request(url, params)
        return items

    def _get_all_pages_matches(self):
        """Return page matches from all pages.

        :return: all matches in all pages
        """
        url = self._get_post_list_url()
        page = 1
        count_posts = self.posts_number if self.posts_number <= self.COUNT_POSTS_MAX else self.COUNT_POSTS_MAX
        total_posts = 0
        response = []
        while True:
            if self.posts_number - total_posts < self.COUNT_POSTS_MAX:
                count_posts = self.posts_number - total_posts

            items = self._get_post_page_list(url, page, count_posts) or []
            response.extend(self._get_matches_from_one_page(items))
            total_posts += len(items)
            if not items or total_posts >= self.posts_number:
                break
            page += 1

        return response

    def _get_matches_from_one_page(self, items):
        """Process page with post list and get matches from onle one page.

        :param items: found detail post page objects
        :return: url with pattern matches for response
        """
        response = []
        if items:
            for item in items:
                item_id = item.get('id')
                item_desc = item.get('description')
                url = item.get('html_url')

                desc_matches = self._get_matches_in_text(item_desc)
                page_matches = self._get_matches_on_page(item_id)
                self._add_data_to_response(desc_matches, page_matches, url, response)
        return response

    def parse(self):
        """Start parsing.

        :return: found matches with urls
        """

        new_response = []
        if self.match_patterns:
            new_response = self._get_all_pages_matches()
        return new_response


class PasteBinParser(BaseParser):
    """Parser for working with pastebin."""
    BASE_URL = 'https://pastebin.com'
    POST_URL = '/raw'
    POST_LIST_URL = '/archive'
    COUNT_POSTS_MAX = 50

    def _get_pastes_page_content(self):
        """Get content of page with posts.

        :return: content of post page list
        """
        url = self._get_post_list_url()
        content = self._make_request(url, to_json=False)
        return content.text

    def _get_paste_page_content(self, url):
        """Get content of one post.

        :param url: detail post page url
        :return: content of detail post page url
        """
        paste_raw_url = self._get_post_url(url)
        paste_content = self._make_request(paste_raw_url, to_json=False)
        return paste_content.text

    def _get_items_for_parsing(self):
        """Return posts for parsing.

        :return: list of parsed object with link and description
        """
        count_posts = self.posts_number if 0 < self.posts_number < self.COUNT_POSTS_MAX else self.COUNT_POSTS_MAX
        pastes_page_content = self._get_pastes_page_content()
        tree = html.fromstring(pastes_page_content)
        items = tree.xpath('//table[@class="maintable"]/tr/td[1]/a')
        return items[:count_posts] or []

    def parse(self):
        """Start parsing.

        :return: found matches with urls
        """
        log.info('We can parse free only 50 latest posts')
        items = self._get_items_for_parsing()
        response = []
        for item in items:
            paste_desc = item.text
            paste_url = item.get('href')
            paste_site_url = urljoin(self.BASE_URL, paste_url)
            paste_content = self._get_paste_page_content(paste_url)

            desc_matches = self._get_matches_in_text(paste_desc)
            page_matches = self._get_matches_in_text(paste_content)
            self._add_data_to_response(desc_matches, page_matches, paste_site_url, response)
        return response
