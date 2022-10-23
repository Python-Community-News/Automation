"""Script to be ran by GH Actions to build the archive and schedule the newsletter"""
import pprint
import pathlib
from gh_issues import Repo, Issue
import typer
from dateutil import parser

from src import newsletter
from src.engine import engine


def build_newsletter(issue: Issue) -> dict[str, str]:
    """Build the archive from the issues"""
    template = engine.get_template("newsletter.md")
    content = template.render(issue=issue)

    shownotes = newsletter.Shownotes(
        subject=issue.title,
        content=content,
        publish_date=issue.newsletter_publish,
    )

    return newsletter.build_email_from_content(shownotes)


def main(issue: int):
    """Build the archive and schedule the newsletter"""
    repo = Repo("Python-Community-News", "Topics")
    issue = Issue.from_issue_number(repo=repo, issue_id=issue)
    # build_website(episode)
    build_newsletter(issue)


if __name__ == "__main__":
    typer.run(main)
