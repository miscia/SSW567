# HW03a - GitHub API
# Takes a GitHub user ID and returns each repo with its number of commits

import requests


def get_data(url):
    # all the API calls go through here so it's easy to mock in the tests
    response = requests.get(url)

    if response.status_code == 404:
        raise ValueError("user or repo not found")
    if response.status_code == 409:
        # empty repo (no commits)
        return []
    if response.status_code == 403:
        raise ConnectionError("rate limit reached, wait and try again")
    if response.status_code != 200:
        raise ConnectionError("error " + str(response.status_code))

    return response.json()


def get_repos(user_id):
    if type(user_id) != str or user_id == "":
        raise ValueError("invalid user ID")

    repos = get_data("https://api.github.com/users/" + user_id + "/repos")
    names = []
    for repo in repos:
        names.append(repo["name"])
    return names


def count_commits(user_id, repo):
    commits = get_data("https://api.github.com/repos/" + user_id + "/" + repo + "/commits")
    return len(commits)


def get_user_info(user_id):
    result = []
    for repo in get_repos(user_id):
        result.append((repo, count_commits(user_id, repo)))
    return result


def make_output(result):
    lines = []
    for repo, commits in result:
        lines.append("Repo: " + repo + " Number of commits: " + str(commits))
    return lines


if __name__ == "__main__":
    user_id = input("GitHub user ID: ")
    for line in make_output(get_user_info(user_id)):
        print(line)
