import datetime
import random
import typing

import pytest

from src.github import Episode, Repo, parse_issue_markdown


@pytest.fixture(scope="session")
def date():
    return datetime.datetime.today()


@pytest.fixture(scope="session")
def time():
    return datetime.time(
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
    )


@pytest.fixture(scope="session")
def shownotes_text():
    return """---
subject: Test Newsletter
---

This is some text for the newsletter.
"""


@pytest.fixture(scope="session")
def newsletter_body():
    return {
        "email_type": "public",
        "body": "This is some text for the newsletter.",
        "subject": "Test Newsletter",
    }


@pytest.fixture(scope="session")
def issue_text():
    return """### Issue Name

Test Issue

### Skipped Section

_No response_

### Issues
Issues Covered: #1, #2, #3, #4

### TextArea Content

Aliquip eiusmod minim excepteur officia **tempor** est incididunt adipisicing elit. Aliqua tempor incididunt magna occaecat esse nulla nostrud. Irure incididunt nulla id eu et. Occaecat quis sit laborum labore nisi minim esse ex ea.

Laboris anim pariatur nisi mollit. Qui nostrud id ipsum quis mollit aliqua est amet tempor nulla. Aute pariatur ullamco qui consequat anim ad nisi ex sit. Quis officia esse incididunt tempor aliqua quis qui est amet. Nisi nostrud sit ea anim voluptate. Est amet mollit consectetur sit et aliquip pariatur nisi enim. Ex sit enim do culpa consectetur irure est duis minim magna do eiusmod est.
"""


class CustomEpisode(Episode):
    raw: dict = {
        "title": "Test Episode",
        "created_at": "2022-01-01T00:00:00Z",
    }

    def __init__(self, issue_text: str, issue_fields: typing.Sequence[str]):
        self.body = parse_issue_markdown(issue_text)
        for key, value in self.body.items():
            setattr(self, key, value)


@pytest.fixture(scope="session")
def test_Episode(issue_text):
    return CustomEpisode(issue_text, ["issues"])


@pytest.fixture(scope="session")
def test_repo():
    return Repo("Python-Community-News", "Topics")
