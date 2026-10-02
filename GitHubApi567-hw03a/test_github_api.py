# Tests for HW03a
# I used mock so the tests don't call the real GitHub API (rate limit + results change over time)

import unittest
from unittest.mock import patch, Mock

from github_api import get_repos, count_commits, get_user_info, make_output


def fake_response(status, data=None):
    response = Mock()
    response.status_code = status
    response.json.return_value = data
    return response


class TestGitHubApi(unittest.TestCase):

    @patch("github_api.requests.get")
    def testGetRepos(self, mock_get):
        mock_get.return_value = fake_response(200, [{"name": "Triangle567"}, {"name": "Square567"}])
        self.assertEqual(get_repos("John567"), ["Triangle567", "Square567"])

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

    def testEmptyUserId(self):
        with self.assertRaises(ValueError):
            get_repos("")

    def testUserIdNotString(self):
        with self.assertRaises(ValueError):
            get_repos(567)

    @patch("github_api.requests.get")
    def testCountCommits(self, mock_get):
        mock_get.return_value = fake_response(200, [{"sha": "1"}, {"sha": "2"}, {"sha": "3"}])
        self.assertEqual(count_commits("John567", "Triangle567"), 3)

    @patch("github_api.requests.get")
    def testEmptyRepo(self, mock_get):
        mock_get.return_value = fake_response(409)
        self.assertEqual(count_commits("John567", "EmptyRepo"), 0)

    @patch("github_api.count_commits")
    @patch("github_api.get_repos")
    def testGetUserInfo(self, mock_repos, mock_commits):
        mock_repos.return_value = ["Triangle567", "Square567"]
        mock_commits.side_effect = [10, 27]
        self.assertEqual(get_user_info("John567"), [("Triangle567", 10), ("Square567", 27)])

    def testOutput(self):
        self.assertEqual(make_output([("Triangle567", 10), ("Square567", 27)]),
                         ["Repo: Triangle567 Number of commits: 10",
                          "Repo: Square567 Number of commits: 27"])


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
