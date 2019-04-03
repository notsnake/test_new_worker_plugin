import unittest
from unittest.mock import patch

from tf_workers import get_worker

from tests import test_data as data
from tfw_myworker.exceptions import AuthenticationException
from tfw_myworker.parsers import GitHubParser
from tfw_myworker.parsers import PasteBinParser


class TestParsersResponse(unittest.TestCase):
    """Test cases for parsers."""

    def test_parsers(self):
        Worker = get_worker('myworker')
        worker_obj = Worker(
            number_of_pates_gists=3,
            match_patterns=['.* ?@domain.com', '*-mydomain.com', 'pass*', 'data', 'import', 'func', 'function',
                            'defined', 'define', 'def'],
            github_username='',
            github_password='',
            pastebin_username='',
            pastebin_password=''

        )
        with patch.object(PasteBinParser, '_get_pastes_page_content') as mock_pastebin_posts, \
                patch.object(PasteBinParser, '_get_paste_page_content') as mock_pastebin_post, \
                patch.object(GitHubParser, '_get_post_page_list') as mock_github_posts, \
                patch.object(GitHubParser, '_get_files_content_page') as mock_github_post:
            mock_pastebin_posts.return_value = data.PASTEBIN_POST_LIST_RESPONSE
            mock_pastebin_post.return_value = data.PASTEBIN_POST_RESPONSE
            mock_github_posts.return_value = data.GITHUB_POST_LIST_RESPONSE
            mock_github_post.return_value = data.GITHUB_POST_RESPONSE
            resp = worker_obj.run()
            # print(resp.data)
            self.assertEqual(len(resp.data), 5)

    def test_parsers_with_invalid_auth(self):
        Worker = get_worker('myworker')
        worker_obj = Worker(
            number_of_pates_gists=3,
            match_patterns=['.* ?@domain.com', '*-mydomain.com', 'pass*', 'data', 'import', 'func', 'function',
                            'defined', 'define', 'def'],
            github_username='test',
            github_password='test',
            pastebin_username='',
            pastebin_password=''

        )
        with self.assertRaises(AuthenticationException):
            resp = worker_obj.run()
            # print(resp)

    def test_parsers_with_real_data(self):
        Worker = get_worker('myworker')
        worker_obj = Worker(
            number_of_pates_gists=1,
            match_patterns=['.* ?@domain.com', '*-mydomain.com', 'pass*', 'data', 'import', 'func', 'function',
                            'defined', 'define', 'def'],
            github_username='',
            github_password='',
            pastebin_username='',
            pastebin_password=''

        )
        resp = worker_obj.run()

    def test_parsers_with_pages(self):
        Worker = get_worker('myworker')
        worker_obj = Worker(
            number_of_pates_gists=3,
            match_patterns=['.* ?@domain.com', '*-mydomain.com', 'pass*', 'data', 'import', 'func', 'function',
                            'defined', 'define', 'def'],
            github_username='',
            github_password='',
            pastebin_username='',
            pastebin_password=''

        )
        with patch.object(PasteBinParser, '_get_pastes_page_content') as mock_pastebin_posts, \
                patch.object(PasteBinParser, '_get_paste_page_content') as mock_pastebin_post, \
                patch.object(GitHubParser, '_get_post_page_list') as mock_github_posts, \
                patch.object(GitHubParser, '_get_files_content_page') as mock_github_post, \
                patch.object(GitHubParser, 'COUNT_POSTS_MAX', 1):
            mock_pastebin_posts.return_value = data.PASTEBIN_POST_LIST_RESPONSE
            mock_pastebin_post.return_value = data.PASTEBIN_POST_RESPONSE
            mock_github_posts.return_value = data.GITHUB_ONE_POST_IN_LIST_RESPONSE
            mock_github_post.return_value = data.GITHUB_POST_RESPONSE
            resp = worker_obj.run()
            self.assertEqual(len(resp.data), 5)
