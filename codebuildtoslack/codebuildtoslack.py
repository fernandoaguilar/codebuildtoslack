# -*- coding: utf-8 -*-
import click
import requests
import os

"""Main module."""


def main():
    # if codebuild environment
    # parse codebuild data
    is_codebuild = "CODEBUILD_CI" in os.environ
    if not is_codebuild:
        click.echo("Not in an AWS Codebuild Environment")
        return

    payload = build_codebuild_payload()
    send_slack_message(payload)


def build_codebuild_payload():
    build_number = os.getenv("CODEBUILD_BUILD_NUMBER")
    build_id = os.getenv("CODEBUILD_BUILD_ID")
    project_name = build_id.split(":")[0]
    start_time_stamp = os.getenv("CODEBUILD_START_TIME")
    aws_reqion = os.getenv("AWS_DEFAULT_REGION")
    branch_name = os.getenv("CODEBUILD_WEBHOOK_TRIGGER").split("/")[-1]
    git_repo = os.getenv("CODEBUILD_SOURCE_REPO_URL").replace(".git", "")
    source_version = os.getenv("CODEBUILD_SOURCE_VERSION")
    codebuild_url = os.getenv("CODEBUILD_BUILD_URL")

    commit_url = f"{git_repo}/commit/{source_version}"
    status = "Failed"
    color = "#CC0000"
    if os.getenv("CODEBUILD_BUILD_SUCCEEDING") == "1":
        status = "Succeeded"
        color = "#0cab27"

    text = f"*{project_name}*\nBuild <{codebuild_url}|#{build_number}> *{status}*"
    context_text = f"*Branch:* {branch_name}\n*Commit:* <{commit_url}|{source_version[:6]}>\n*Build Time:* 4 minutes 30 seconds "

    payload = {
        "attachments": [
            {
                "color": color,
                "blocks": [
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": text},
                        "accessory": {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "View Logs"},
                            "url": codebuild_url,
                        },
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": context_text
                            }
                        ],
                    },
                ],
            }
        ]
    }

    return payload


def send_slack_message(payload):
    url = (
        "https://hooks.slack.com/services/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"
    )
    requests.post(url, json=payload)


def test_slack_message():
    url = (
        "https://hooks.slack.com/services/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"
    )
    payload = {
        "fallback": "Required text summary of the attachment that is shown by clients that understand attachments but choose not to show them.",
        "text": "Optional text that should appear within the attachment",
        "pretext": "Optional text that should appear above the formatted data",
        "color": "#36a64f",  # Can either be one of 'good', 'warning', 'danger', or any hex color code
        "fields": [
            {
                "title": "Required Field Title",  # The title may not contain markup and will be escaped for you
                "value": "Text value of the field. May contain standard message markup and must be escaped as normal. May be multi-line.",
                "short": False,  # Optional flag indicating whether the `value` is short enough to be displayed side-by-side with other values
            }
        ],
    }
    requests.post(url, json=payload)
