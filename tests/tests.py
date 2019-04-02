import unittest
from unittest.mock import patch

from tf_workers import get_worker

from tests import test_data as data
from tfw_myworker.parsers import GitHubParser
from tfw_myworker.parsers import PasteBinParser


class TestParsersResponse(unittest.TestCase):
    """Test cases for parsers."""

    def test_parsers(self):  # pylint: disable=R0201
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
                patch.object(GitHubParser, '_get_post_page_content') as mock_github_posts, \
                patch.object(GitHubParser, '_get_files_content_page') as mock_github_post:
            mock_pastebin_posts.return_value = data.PASTEBIN_POST_LIST_RESPONSE
            mock_pastebin_post.return_value = data.PASTEBIN_POST_RESPONSE
            mock_github_posts.return_value = data.GITHUB_POST_LIST_RESPONSE
            mock_github_post.return_value = data.GITHUB_POST_RESPONSE
            resp = worker_obj.run()
            print(resp.data)
            self.assertEqual(len(resp.data), 5)
