# Test task for developer evaluation #
Take in a list of python regular expression strings and then search the recent pastebin
(https://pastebin.com/) and gists (https://gist.github.com) for matches. If any of the
pastebin/gist entry title or content matches any of the regular expressions; the url of
the gist/pastebin and the matched regular expression item should be returned by the
worker code.

It is upto the developer to select if there is an API provided by the above sources that
can be used or to scrape the data directly off from their sites.
Number of recent gists/pastes to fetch and process should also be provided by the
user and defined as a worker setting within the worker plugin code. See
new_worker_plugin_template/tfw_myworker/myworker.py for details.

### Running the code:
Since the worker code is in a specific format it can’t just be called from the shell for
testing. The code needs to run using the tf_workers package. Sample execution code:
```
from tf_workers import get_worker
Worker = get_worker('myworker')
worker_obj = Worker(
number_of_pates_gists=1000,
match_patterns=[‘.*?@domain.com’, ‘*-mydomain.com’, ‘pass*’]
)
resp = worker_obj.run()
print(resp)
WorkerResponse(response_code=SUCCESS, error_message='', location='None',
data=[
{‘url’: ‘https://pastebin.com/Jup6T0ii’, ‘matches’: [‘pass*’]},
{‘url’:
‘https://gist.github.com/simplement-e/51e7a42814faaafb7dc12c84db709534’,
‘matches’: [‘.*?@domain.com’, ‘*-mydomain.com’]}
])
```
Please note that you will need to pass different values for the match_patterns list
based on recent available pastes/gists to get matching results. The code above is just and example.

### MODULE REQUIREMENTS
#### Inputs
* match_patterns (list) – A list of regular expression patterns. If either of these
matches the paste/gist content then the paste/gist url needs to be returned by the
worker plugin
* number_of_pates_gists (int) – The number of latest gists/pastes to process.
#### Outputs
* WorkerResponse object with data containing all matching paste/gist urls and the
patterns that matched the paste/gist title or content.
### Guidelines:
* The task needs to be developed as a class of specific format.
* The class needs to be a sub-class of tf_workers.Worker class.
* A sample worker plugin code template is provided with this document
(new_worker_plugin_template).
#### Code Standard Guidelines:
* All code needs to be in python3 and be able to run on the latest python 3.x
versions (3.5, 3.6 or 3.7).
* Code should follow python style guidelines specified by PEP-8.
* The purpose of this task is to ascertain the skills of prospective developers so
using already available open source code is not allowed. You are allowed to use
python standard libraries or third party libraries like python-requests but any
specific library for scraping pastebin or gists is not allowed.
* Please make sure that your code has comprehensive test coverage. Only providing
unit tests for test cases is good enough. However test cases themselves should not
make the code do any network communication. All network traffic should be
mocked by using python's mock module. Test cases should include all reasonable
failure cases and various usage scenarios of the code.
* Preferred method of development is to maintain a separate python 3.5, 3.6 or 3.7
virtualenv.
* All code needs to be PEP8 compliant. PEP8 compliance can be enabled within all
popular code editors and IDEs.
* Using linters (pyflakes, pylint) is also encouraged.