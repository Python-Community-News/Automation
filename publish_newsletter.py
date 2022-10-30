"""Script to be ran by GH Actions to build the archive and schedule the newsletter"""

from http.client import HTTPResponse

import typer
from gh_issues import Issue, Repo

from src import newsletter
from src.engine import engine


def build_newsletter(issue: Issue) -> dict[str, str]:
    """Build the newsletter from a GitHub Issue"""
    template = engine.get_template("newsletter.md")
    content = template.render(issue=issue)

    shownotes = newsletter.Shownotes(
        subject=issue.title,
        content=content,
        publish_date=issue.newsletter_publish,
    )

    return newsletter.build_email_from_content(shownotes)


def main(
    issue_number: int = typer.Argument(
        ..., rich_help_panel="GitHub Information", help="Issue number to publish"
    ),
    github_account: str = typer.Option(
        "...",
        "--github-account",
        "-a",
        envvar="GITHUB_ACCOUNT",
        rich_help_panel="GitHub Information",
        help="The GitHub account to use",
    ),
    github_repo: str = typer.Option(
        "...",
        "--github-repo",
        "-r",
        envvar="GITHUB_REPO",
        rich_help_panel="GitHub Information",
        help="The GitHub repo to use",
    ),
    github_api: str = typer.Option(
        None,
        "--github-api",
        envvar="GITHUB_API_TOKEN",
        rich_help_panel="GitHub Information",
        help="The GitHub API token to use",
    ),
    buttondown_api: str = typer.Option(
        "...",
        "--buttondown-api",
        envvar="BUTTONDOWN_API_TOKEN",
        rich_help_panel="Buttondown Information",
        help="The Buttondown API token to use",
    ),
) -> HTTPResponse:
    """Build the archive and schedule the newsletter"""
    repo = Repo(github_account, github_repo)
    issue = Issue.from_issue_number(repo=repo, issue_id=issue)
    return build_newsletter(issue)


if __name__ == "__main__":
    typer.run(main)
