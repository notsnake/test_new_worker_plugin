"""
Module Introduction.

Any module level documentation comes here.
"""

import re
import logging
from tf_workers import (  # pylint: disable=E0611
    Worker, SettingProperty, WorkerResponse, ResponseCodes as RC
)
from tf_workers.config import ApplicationConfig  # pylint: disable=E

from tfw_myworker.parsers import GitHubParser
from tfw_myworker.parsers import PasteBinParser

config = ApplicationConfig.get_config()

log = logging.getLogger(__name__)


class MyWorker(Worker):
    """
    MyWorker.

    Description and list of parameters. For example:

    :param domain_or_ip:
        Required - The domain or IP Address to perform whois and IPWhois on
    """

    name = 'myworker'
    resource_requirements = 'LOW'
    requires = [
        # any additional python modules come here
    ]
    os_requires = [
        # Any additional OS (Linux-Ubuntu) packages come here
    ]

    def _init_settings(self):
        """Initialize worker settings."""
        super()._init_settings()
        # Add any arguments/properties required by the worker here.
        self.settings.add(SettingProperty(
            name='number_of_pates_gists', data_type=int,
            description='number_of_pates_gists'))

        self.settings.add(SettingProperty(
            name='match_patterns', data_type=list,
            description='match_patterns'))

        self.settings.add(SettingProperty(
            name='github_username', data_type=str,
            description='github_username'))

        self.settings.add(SettingProperty(
            name='github_password', data_type=str,
            description='github_password'))

        self.settings.add(SettingProperty(
            name='pastebin_username', data_type=str,
            description='pastebin_username'))

        self.settings.add(SettingProperty(
            name='pastebin_password', data_type=str,
            description='pastebin_password'))

        # Note: These are inputs to the worker. If you want any information
        # passed to the worker it must be added to self.settings

    def _check_and_get_match_patterns(self):
        expressions = {}
        for pattern in self.settings.match_patterns.value:
            try:
                expr = re.compile(pattern)
            except re.error:
                message = 'pattern: {} is wrong'.format(pattern)
                log.error(message)
                expr = None
            if expr:
                expressions[expr] = pattern
        return expressions

    def __init__(self, **kwargs):
        """Create worker object."""
        super().__init__(kwargs)

    def run(self):
        """Call this method to run the WHOIS worker."""
        super().run()
        self.response = WorkerResponse()
        self.response.response_code = RC.SUCCESS
        match_patterns = self._check_and_get_match_patterns()
        github_parser = GitHubParser(posts_number=self.settings.number_of_pates_gists.value,
                              match_patterns=match_patterns,
                              username=self.settings.github_username.value,
                              password=self.settings.github_password.value,)
        pastebin_parser = PasteBinParser(posts_number=self.settings.number_of_pates_gists.value,
                                match_patterns=match_patterns,
                                username=self.settings.pastebin_username.value,
                                password=self.settings.pastebin_password.value,)
        parsers = [github_parser, pastebin_parser]
        data = []
        for parser in parsers:
            data.extend(parser.parse())
        self.response.data = data


        # TODO: Actual worker code comes here for performing worker task and
        # populating self.response.data with the result.
        # If you have defined any input settings in _init_settings() those
        # are accessible here using self.settings.setting_name.value

        return self.response
