from collections import namedtuple

import httpx

schedule_email_url: str = "https://api.buttondown.email/v1/scheduled-emails"
Shownotes = namedtuple("Shownotes", "subject content publish_date")


def build_email_from_content(
    shownotes: Shownotes,
    buttondown_api: str,
) -> httpx.Response:
    """
    Parse the shownotes object to build the email
    """
    body = {
        "email_type": "public",
        "body": shownotes.content,
        "subject": shownotes.subject,
        "publish_date": shownotes.publish_date,
    }
    header = {"Authorization": f"Token {buttondown_api}"}
    request = httpx.post(
        schedule_email_url,
        headers=header,
        json=body,
    )
    return request
