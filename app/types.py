from __future__ import annotations

import json
from typing import Optional, Dict, List, Union, TypeVar
from functools import cached_property  # type: ignore
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field, HttpUrl
from fastapi.responses import JSONResponse


class Metadata(BaseModel):

    "Metadata to check namespace data"

    webpage: HttpUrl = Field("https://igsn.github.io/registered/")
    last_updated: Optional[datetime] = None
    metadata_file: Path = Path("./igsn_namespace_meta.json")
    data_file: Path = Path("./igsn_namespace.json")


class Namespace(BaseModel):

    "Store information about an IGSN namespace"

    namespace: str = Field(
        ...,
        description="The namespace name (same as the IGSN prefix)",
        regex="[A-Z0-9]+",
        example="AU",
    )
    owner: str = Field(
        ...,
        description="The Allocating Agent which governs this namespace",
        example="GEOAUS",
    )
    handle_prefix: str = Field(
        ...,
        description="The prefix for the fully-resolved handle",
        regex="10273/[A-Z0-9]+",
        example="10273/AU",
    )
    date_created: Optional[str] = Field(
        None,
        description="The date that the namespace was created, in ISO format",
        example="2015-02-12T08:23:28+01:00",
    )


class Namespaces:

    "Store info about all namespaces"

    def __init__(self, items: List[Namespace]):
        self.items = items

    def json(self):
        "Serialize to JSON"
        return json.dumps([ns.json() for ns in self.items])

    @cached_property
    def namespaces(self) -> Dict[str, Namespace]:
        "Index by namespace"
        return {ns.namespace.upper(): ns for ns in self.items}

    @cached_property
    def agents(self) -> Dict[str, Agent]:
        "Index by agent"
        # Construct by_agent index
        index: Dict[str, Agent] = {}
        for ns in self.items:
            try:
                index[ns.owner.upper()].namespaces.append(ns)
            except KeyError:
                # Make a new Agent instance with this namespace
                index[ns.owner.upper()] = Agent(name=ns.owner, namespaces=[ns])
        return index

    def by_agent(self, agent: str) -> Optional[Agent]:
        "Search by agent"
        return self.agents.get(agent.upper(), None)

    def by_namespace(self, namespace: str) -> Optional[Namespace]:
        "Search by namespace"
        return self.namespaces.get(namespace.upper(), None)


class Agent(BaseModel):

    "Stores information about an IGSN Allocating Agent"

    name: str = Field(
        ...,
        title="Allocating agent",
        description="The name of the allocating agent",
        example="GEOAUS",
    )
    namespaces: List[Namespace]


# A return type for app errors
T = TypeVar("T")
HTTPResponse = Union[T, JSONResponse]


# A class for error messages
class HTTPErrorMessage(BaseModel):
    detail: str
