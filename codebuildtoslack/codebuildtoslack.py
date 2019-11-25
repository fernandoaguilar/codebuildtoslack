# -*- coding: utf-8 -*-
import click
import requests
import os
from datetime import datetime
from . import utils

"""Main module."""


def main():
    is_codebuild = "CODEBUILD_CI" in os.environ
    if not is_codebuild:
        click.echo("Not in an AWS Codebuild Environment", err=True)
        return

    payload = build_codebuild_payload()
    send_slack_message(payload)
    click.echo('Slack message sent')


def build_codebuild_payload():
    build_number = os.getenv("CODEBUILD_BUILD_NUMBER")
    build_id = os.getenv("CODEBUILD_BUILD_ID")
    project_name = build_id.split(":")[0]
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

    build_time_text = calculate_build_time_text()
    context_text = f"*Branch:* {branch_name}\n*Commit:* <{commit_url}|{source_version[:6]}>\n*Build Time:* {build_time_text}"

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
                        "elements": [{"type": "mrkdwn", "text": context_text}],
                    },
                ],
            }
        ]
    }

    return payload


def calculate_build_time_text():
    start_time_stamp = float(os.getenv("CODEBUILD_START_TIME")) / 1000
    start_dt_object = datetime.fromtimestamp(start_time_stamp)
    delta = datetime.utcnow() - start_dt_object
    return utils.seconds_to_text(delta.seconds)


def send_slack_message(payload):
    url = os.getenv("SLACK_URL")
    if not url:
        click.echo("No Slack url provided", err=True)
        return
    requests.post(url, json=payload)
