import dataclasses
import os
import re
from collections import defaultdict, namedtuple
from typing import Any, Generator, Sequence

import httpx
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode


def get_content_issues(
    body: dict[str, Any],
    issues_tag: str,
) -> list[int]:
    """
    Returns Issues Passed in sections of the issue body
    """
    issues = getattr(body, issues_tag, "")
    return [int(n) for n in re.findall(r"\d+", issues)]


def parse_issue_markdown(text) -> dict[str, str]:
    """Use markdownit to split at section headings"""
    md = MarkdownIt("zero", {"maxNesting": 1})
    md.enable(["heading", "paragraph"])
    tokens = md.parse(text)
    node = SyntaxTreeNode(tokens)
    issue_object = defaultdict(list)
    for n in node.children:
        if n.type == "heading":
            issue_key = n.children[0].content.lower().replace(" ", "_")
        elif content := n.children[0].content == "_No response_":
            continue
        else:
            issue_object[issue_key].append(n.children[0].content)

    return {key: "\n".join(value) for key, value in issue_object.items()}


@dataclasses.dataclass
class Repo:
    owner: str
    repo: str

    @property
    def url(self):
        return f"https://api.github.com/repos/{self.owner}/{self.repo}"


def get_from_github(Repo: Repo, issue_id: int) -> dict[str, str]:
    """
    Returns the issue with the given id.
    The issue_id must be a valid integer.
    """

    url = (
        f"https://api.github.com/repos/{Repo.owner}/{Repo.repo}/issues/{str(issue_id)}"
    )
    headers = {
        "Authorization": f"Bearer {os.environ['GITHUB_API_TOKEN']}",
    }
    request = httpx.get(url, headers=headers)

    if request.status_code not in [200, 201]:
        raise ConnectionRefusedError(f"Unable to connect: {request.json()}")

    return request.json()


Issue = namedtuple("Issue", "metadata body")


def get_issues(issues: Sequence, Repo: Repo) -> Generator[Issue, None, None]:
    """Gets issues from the section"""
    for issue in issues:
        issue_content = get_from_github(Repo, issue)
        body = parse_issue_markdown(issue_content["body"])
        i = Issue(metadata=issue_content, body=body)
        yield i


class Episode:
    def __init__(self, episode_id: int, issue_fields: list, Repo: Repo):
        self.episode_id = episode_id
        self.raw = get_from_github(issue_id=self.episode_id, Repo=Repo)
        self.body = parse_issue_markdown(self.raw["body"])

        for key, value in self.body.items():
            setattr(self, key, value)

        for field in issue_fields:
            setattr(
                self,
                field,
                list(
                    get_issues(issues=get_content_issues(self.body, field), Repo=Repo)
                ),
            )

    @property
    def title(self) -> str:
        return self.raw["title"]

    @property
    def created_at(self) -> str:
        return self.raw["created_at"]
