"""
Functions to check valid IGSN namespaces
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List
import logging

import requests
from lxml import html

from .types import Namespace, Namespaces, Metadata

LOGGER = logging.getLogger()


def get_last_modified(response: requests.Response) -> datetime:
    """
    Get the Last-Modified header info as a datetime object
    """
    return datetime.strptime(
        response.headers["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z"
    )


def download_data(metadata: Optional[Metadata] = None) -> Namespaces:
    "Get the latest data from the given location"
    meta = metadata or Metadata()

    # Download HTML from the webpage
    response = requests.get(meta.webpage)
    if not response.ok:
        response.raise_for_status()

    # Extract table - we assume it's the first one
    document = html.fromstring(response.text)
    table = document.xpath("//table")[0]

    # Do headers first - just to check order and that we've got
    # the right table
    headers = [e.text for e in table.xpath("./thead/tr/th")]
    if headers != ["Prefix", "Allocators", "Created"]:
        raise ValueError(f"Unexpected headers {headers}")

    # Extract rows
    namespaces: List[Namespace] = []
    keys = ("handle_prefix", "owner", "date_created")
    for row in table.xpath("./tbody/tr"):
        row = dict(zip(keys, [e.text for e in row]))
        row.update(
            namespace=row["handle_prefix"].split("/")[1],
            date_created=parse_nasty_dates(row["date_created"]),
        )
        namespaces.append(Namespace(**row))
    return Namespaces(items=namespaces)


def parse_nasty_dates(created: str) -> Optional[str]:
    "Try and parse the nasty date examples into an iso format"
    try:
        return datetime.fromisoformat(created).isoformat()
    except ValueError:
        pass  # probably some other format

    try:
        return datetime.strptime(created, r"%Y-%m-%d %H:%M %Z").isoformat()
    except ValueError:
        return None  # welp ¯\(°_o)/¯
