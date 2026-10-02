# Tests for HW03b - Mocking
# All calls to the GitHub API are mocked with unittest.mock, so the tests never
# call GitHub. They give the same result every time, no matter how many times
# they run or what changes are made to the repos.

import unittest
from unittest.mock import patch, Mock

from github_api import get_repos, count_commits, get_user_info, make_output


def fake_response(status, data=None):
    response = Mock()
    response.status_code = status
    response.json.return_value = data
    return response


class TestGetRepos(unittest.TestCase):

    @patch("github_api.requests.get")
    def testGetRepos(self, mock_get):
        mock_get.return_value = fake_response(200, [{"name": "Triangle567"}, {"name": "Square567"}])
        self.assertEqual(get_repos("John567"), ["Triangle567", "Square567"])

    @patch("github_api.requests.get")
    def testReposUrl(self, mock_get):
        mock_get.return_value = fake_response(200, [])
        get_repos("John567")
        mock_get.assert_called_once_with("https://api.github.com/users/John567/repos")

    @patch("github_api.requests.get")
    def testNoRepos(self, mock_get):
        mock_get.return_value = fake_response(200, [])
        self.assertEqual(get_repos("John567"), [])

    @patch("github_api.requests.get")
    def testUserNotFound(self, mock_get):
        mock_get.return_value = fake_response(404)
        with self.assertRaises(ValueError):
            get_repos("fakeuser123")

    @patch("github_api.requests.get")
    def testRateLimit(self, mock_get):
        mock_get.return_value = fake_response(403)
        with self.assertRaises(ConnectionError):
            get_repos("John567")

    @patch("github_api.requests.get")
    def testServerError(self, mock_get):
        mock_get.return_value = fake_response(500)
        with self.assertRaises(ConnectionError):
            get_repos("John567")

    @patch("github_api.requests.get")
    def testEmptyUserId(self, mock_get):
        with self.assertRaises(ValueError):
            get_repos("")
        mock_get.assert_not_called()

    @patch("github_api.requests.get")
    def testUserIdNotString(self, mock_get):
        with self.assertRaises(ValueError):
            get_repos(567)
        mock_get.assert_not_called()


class TestCountCommits(unittest.TestCase):

    @patch("github_api.requests.get")
    def testCountCommits(self, mock_get):
        mock_get.return_value = fake_response(200, [{"sha": "1"}, {"sha": "2"}, {"sha": "3"}])
        self.assertEqual(count_commits("John567", "Triangle567"), 3)

    @patch("github_api.requests.get")
    def testCommitsUrl(self, mock_get):
        mock_get.return_value = fake_response(200, [])
        count_commits("John567", "Triangle567")
        mock_get.assert_called_once_with("https://api.github.com/repos/John567/Triangle567/commits")

    @patch("github_api.requests.get")
    def testEmptyRepo(self, mock_get):
        mock_get.return_value = fake_response(409)
        self.assertEqual(count_commits("John567", "EmptyRepo"), 0)

    @patch("github_api.requests.get")
    def testRepoNotFound(self, mock_get):
        mock_get.return_value = fake_response(404)
        with self.assertRaises(ValueError):
            count_commits("John567", "NoSuchRepo")


class TestFullProgram(unittest.TestCase):

    @patch("github_api.requests.get")
    def testGetUserInfo(self, mock_get):
        # first call returns the repos, the next calls return the commits for each repo
        mock_get.side_effect = [
            fake_response(200, [{"name": "Triangle567"}, {"name": "Square567"}]),
            fake_response(200, [{"sha": str(i)} for i in range(10)]),
            fake_response(200, [{"sha": str(i)} for i in range(27)]),
        ]
        self.assertEqual(get_user_info("John567"), [("Triangle567", 10), ("Square567", 27)])
        self.assertEqual(mock_get.call_count, 3)

    @patch("github_api.requests.get")
    def testUserWithEmptyRepo(self, mock_get):
        mock_get.side_effect = [
            fake_response(200, [{"name": "Triangle567"}, {"name": "EmptyRepo"}]),
            fake_response(200, [{"sha": "1"}, {"sha": "2"}]),
            fake_response(409),
        ]
        self.assertEqual(get_user_info("John567"), [("Triangle567", 2), ("EmptyRepo", 0)])

    def testOutput(self):
        self.assertEqual(make_output([("Triangle567", 10), ("Square567", 27)]),
                         ["Repo: Triangle567 Number of commits: 10",
                          "Repo: Square567 Number of commits: 27"])


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
