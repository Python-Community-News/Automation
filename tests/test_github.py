import httpx
import pytest

from src.github import (
    get_issues,
    get_from_github,
    get_content_issues,
    parse_issue_markdown,
)

def test_get_issue_passes_correct_url(
    httpx_mock,
    monkeypatch,
    test_repo,
):
    monkeypatch.setenv("GITHUB_API_TOKEN", "test")
    httpx_mock.add_response(
        url="https://api.github.com/repos/Python-Community-News/Topics/issues/1",
        json={"id": 1},
    )

    with httpx.Client() as _:
        request = get_from_github(test_repo, 1)


def test_get_issues(
    httpx_mock,
    test_repo,
    monkeypatch,
):
    monkeypatch.setenv("GITHUB_API_TOKEN", "test")
    httpx_mock.add_response(
        url="https://api.github.com/repos/Python-Community-News/Topics/issues/1",
        json={
            "id": 1,
            "body": "",
            },
    )

    httpx_mock.add_response(
        url="https://api.github.com/repos/Python-Community-News/Topics/issues/2",
        json={
            "id": 2,
            "body": "",
            },
    )

    with httpx.Client() as _:
        for issue in get_issues([1, 2], Repo=test_repo):
            pass

def test_issues_markdown_parsing(issue_text):
    """Test the issue text is parsed into segments"""
    # The test content will be formatted as test with a new line `\n`
    result_test_content = """Aliquip eiusmod minim excepteur officia **tempor** est incididunt adipisicing elit. Aliqua tempor incididunt magna occaecat esse nulla nostrud. Irure incididunt nulla id eu et. Occaecat quis sit laborum labore nisi minim esse ex ea.
Laboris anim pariatur nisi mollit. Qui nostrud id ipsum quis mollit aliqua est amet tempor nulla. Aute pariatur ullamco qui consequat anim ad nisi ex sit. Quis officia esse incididunt tempor aliqua quis qui est amet. Nisi nostrud sit ea anim voluptate. Est amet mollit consectetur sit et aliquip pariatur nisi enim. Ex sit enim do culpa consectetur irure est duis minim magna do eiusmod est."""
    issue = parse_issue_markdown(issue_text)
    assert issue["issue_name"] == "Test Issue"
    assert "skipped_section" not in issue
    assert issue["textarea_content"] == result_test_content


def test_empty_issues_creates_issues():
    bad_issue = """There's no issues in here"""
    assert get_content_issues(bad_issue, "issue_name") == []


def test_valid_issue_returns_issue_list(test_Episode):
    assert get_content_issues(test_Episode, "issues") == [1,2,3,4]
